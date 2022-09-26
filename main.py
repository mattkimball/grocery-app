import pytz
import streamlit as st
import pandas as pd
from airtable import airtable
from datetime import datetime

# connect to airtable
try:
    at = airtable.Airtable(base_id=st.secrets.base_id,
                           api_key=st.secrets.api_key)
except:
    st.error('error connecting to airtable')

# list of tables, api keys stored in streamlit's secrets file
item_table = st.secrets.item_table
category_table = st.secrets.category_table
meals_table = st.secrets.meals_table
purchases_table = st.secrets.purchases_table

# list of statuses for items
statuses = ['Good', 'Low', 'Out']


## READ FUNCTIONS


def get_table():
    '''returns table of items data

    Returns:
        pandas.DataFrame: DataFrame object
    '''
    df = pd.DataFrame(at.get(table_name=item_table)['records'])
    
    new_df = pd.DataFrame(list(df.fields.values))
    
    # airtable does not store 'false' for checkbox inputs
    # prevents errors if no items are on list
    if 'on_list' not in new_df.columns:
        new_df['on_list'] = False
    else:
        new_df['on_list'].fillna(False, inplace=True)
    
    new_df['id'] = df['id']
    
    merged_df = pd.merge(df, new_df)
    merged_df.sort_values(by=['item_name'], inplace=True)
    
    return merged_df[['id', 'item_name', 'status', 'on_list', 'last_purchased',
                      'category_name']]


def get_items():
    '''returns the names of items as a list

    Returns:
        numpy.Array: array of item names
    '''
    df = get_table()
    
    return df.item_name.values


def get_categories():
    '''returns a table of category data

    Returns:
        pandas.DataFrame: DataFrame object of category data
    '''
    df = pd.DataFrame(at.get(table_name=category_table)['records'])
    
    new_df = pd.DataFrame(list(df.fields.values))
    new_df['id'] = df['id']
    
    merged_df = pd.merge(df, new_df)
    
    return merged_df[['id', 'category_name']]


def categories_list():
    '''returns category names as a list

    Returns:
        list: list of category names
    '''
    df = get_categories()
    
    return df.sort_values(by=['category_name']).category_name.tolist()


def get_meals():
    '''returns a table of meal data

    Returns:
        pandas.DataFrame: DataFrame object of meal data
    '''
    df = pd.DataFrame(at.get(table_name=meals_table)['records'])
    new_df = pd.DataFrame(list(df.fields.values))

    # prevents error if no instructions have been added
    if 'instructions' not in new_df.columns:
        new_df['instructions'] = ''
    
    new_df['id'] = df['id']
    
    merged_df = pd.merge(df, new_df)
    merged_df.sort_values(by=['meal_name'], inplace=True)
    
    return merged_df[['id', 'meal_name', 'ingredients', 'instructions']]


def get_purchases():
    '''returns a table of purchase data

    Returns:
        pandas.DataFrame: DataFrame object of purchase data
    '''
    df = pd.DataFrame(at.get(table_name=purchases_table)['records'])
    
    new_df = pd.DataFrame(list(df.fields.values))
    new_df['id'] = df['id']
    
    merged_df = pd.merge(df, new_df)
    merged_df.sort_values(by=['item_name'], inplace=True)
    
    return merged_df[['id', 'item_name', 'date_purchased']]


## CREATE FUNCTIONS


def add_item(item_name, category_name, status, on_list):
    '''adds an time record to the items table

    Args:
        item_name (str): name of item
        category_name (str): mane of category
        status (str): status indication
        on_list (bool): if item is on shopping list
    '''
    if item_name == '' or status == '':
        st.error('Invalid Input')
    else:
        at.create(table_name=item_table,
                  data={'item_name': item_name,
                        'category': category_name,
                        'status': status,
                        'on_list': on_list})


def add_category(category_name):
    '''adds a category to the category table

    Args:
        category_name (str): category name
    '''
    at.create(table_name=category_table,
              data={'category_name': category_name})


def create_meal(meal_name, ingredients, instructions):
    '''adds a meal to the meal table

    Args:
        meal_name (str): name of meal
        ingredients (list): list of ingredients (on item table)
        instructions (str): desctiption of instructions
    '''
    at.create(table_name=meals_table,
              data={'meal_name': meal_name,
                    'ingredients': ', '.join(ingredients),
                    'instructions': instructions})


## UPDATE FUNCTIONS


def update_record(record_id, column, key, table_name):
    '''updates a record on airtable

    Args:
        record_id (str): airtable primary key
        column (str): column of record being updated
        key (str): session state key containing new value
        table_name (str): airtable api key for table
    '''
    at.update(table_name=table_name,
              record_id=record_id,
              data={column: st.session_state[key]})


def add_to_list(item_name):
    '''adds item to shopping list by updating item record

    Args:
        item_name (str): name of item
    '''
    table = get_table()
    id = table.loc[table.item_name == item_name].id.values[0]
    at.update(table_name=item_table,
              record_id=id,
              data={'on_list': True})


def change_category(id, key, category_name):
    '''updates category name in category table and updates all items in that
    category

    Args:
        id (str): airtable id of category
        key (str): session state key that points to new value
        category_name (str): old value for category name
    '''
    update_record(record_id=id,
                  column='category_name',
                  key=key,
                  table_name=st.secrets.category_table)
    df = get_table()
    for idx, row in df[df.category == category_name].iterrows():
        update_record(record_id=row.id,
                      column='category_name',
                      key=key,
                      table_name=st.secrets.category_table)


def update_list():
    '''removes purchased items from shopping list, updates those items to the
    purchases table, and changes their status to Good
    '''
    table = get_table()
    
    for idx, row in table[table.on_list == True].iterrows():
        key = row.id + '_added'
        
        if st.session_state[key]:
            loc_dt = datetime.now(tz=pytz.timezone("EST"))
            date_stamp = loc_dt.strftime('%Y-%m-%d')
            
            # update Groceries table
            at.update(table_name=item_table,
                      record_id=row.id,
                      data={'on_list': not st.session_state[key],
                            'last_purchased': date_stamp,
                            'status': 'Good'})
            
            # add purchase to Purchases table
            at.create(table_name=purchases_table,
                      data={'item_name': row.item_name,
                            'date_purchased': date_stamp})


def update_meal(id, meal_name, ingredients, instructions):
    '''updates a meal record

    Args:
        id (str): airtable id of meal record
        meal (str): name of meal
        ingredients (list): list of ingredients (on item table)
        instructions (str): description of instructions
    '''
    at.update(table_name=meals_table,
              record_id=id,
              data={'meal_name': meal_name,
                    'ingredients': ', '.join(ingredients),
                    'instructions': instructions})


## DELETE FUNCTIONS


def delete_item(id, table_name):
    '''removeds a record from a table

    Args:
        id (str): airtable id for item
        table_name (str): api key for table
    '''
    at.delete(table_name=table_name,
              record_id=id)


def delete_category(id, category_name):
    '''removes a category from the categories table and changes the category of
    items in that category to None

    Args:
        id (str): airtable id for category
        category (str): name of category
    '''
    delete_item(id=id, table_name=st.secrets.category_table)
    df = get_table()
    df = df[df.category_name == category_name]
    for idx, row in df.iterrows():
        at.update(table_name=item_table,
                  record_id=row.id,
                  data={'category_name': 'None'})


def main():
    pass


if __name__ == '__main__':
    main()