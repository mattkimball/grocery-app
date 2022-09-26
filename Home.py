import streamlit as st
from datetime import datetime
from main import statuses, categories_list, add_item, get_table, update_record


def display_status(status):
    '''writes the status using streamlits built-in colored-containers

    Args:
        status (str): name of status
    '''
    if status == 'Good':
        st.success('Good')
    elif status == 'Low':
        st.warning('Low')
    elif status == 'Out':
        st.error('Out')


if 'new_item' not in st.session_state:
    st.session_state.new_item = False

categories = categories_list()

st.header('Item View')

col1, col2 = st.columns(2)

with col1:
    st.text_input(label='Search for item', key='text_input')
    st.checkbox(label='Hide Details/Edit', key='hide_details')
    st.checkbox(label='Only Show On List', key='show_list')
with col2:
    st.multiselect(label='Sort by Status',
                   options=statuses,
                   key='status_input')
    st.multiselect(label='Sort by Category',
                   options=categories,
                   key='category_input')

table = get_table()
table = table[table.item_name.str.contains(st.session_state.text_input,
                                           case=False)]

if st.session_state.show_list:
    table = table[table.on_list == True]

if st.session_state.status_input:
    table = table[table.status.isin(st.session_state.status_input)]

if st.session_state.category_input:
    table = table[table.category_name.isin(st.session_state.category_input)]

with st.expander('Add item'):
    with st.form('Add Item', clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            item_name = st.text_input(label='Item Name')
        with col2:
            category_name = st.selectbox(label='Category',
                                         options=categories)
        with col3:
            item_status = st.selectbox(label='Status',
                                       options=statuses)
        
        on_list = st.checkbox(label='Add to List')

        submitted = st.form_submit_button(label='Add Item')
        if submitted:
            add_item(item_name, category_name, item_status, on_list)
            st.session_state.new_item = item_name
            st.experimental_rerun()

if st.session_state.new_item:
    st.success(f'Created item: {st.session_state.new_item}')
    st.session_state.new_item = False

st.markdown('***')

if table.empty:
    st.info('No items found')

for idx, row in table.iterrows():
    col1, col2, col3 = st.columns([3, 1, 4])
    
    with col1:
        st.subheader(row.item_name)
    with col2:
        st.caption('Add to List')
        key = row.id + '_on_list'
        st.checkbox(label='',
                    value=row.on_list,
                    key=key,
                    on_change=update_record,
                    args=(row.id, 'on_list', key, st.secrets.item_table))
    with col3:
        display_status(row.status)
    
    if not st.session_state.hide_details:
        col1, col2, col3 = st.columns([1, 2, 3])

        with col1:
            st.caption('Last Purchased')
            if type(row.last_purchased) == str:
                dt = datetime.strptime(row.last_purchased, '%Y-%m-%d')
                st.write(datetime.strftime(dt,'%b %d, %Y'))
            else:
                st.write('n/a')
        with col2:
            key = row.id + '_category'
            st.selectbox(label='Category',
                         options=categories,
                         index=categories.index(row.category_name),
                         key=key)
        with col3:
            key = row.id + '_status'

            st.radio(label='Change Status',
                     options=statuses,
                     key=key,
                     horizontal=True,
                     index=statuses.index(row.status),
                     on_change=update_record,
                     args=(row.id, 'status', key, st.secrets.item_table))
    
    st.markdown('***')

