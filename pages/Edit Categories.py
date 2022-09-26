import streamlit as st
from main import get_categories, change_category, delete_category,\
                 categories_list, add_category, get_table

if 'deleted' not in st.session_state:
    st.session_state.deleted = False
if 'created' not in st.session_state:
    st.session_state.created = False

if st.session_state.deleted:
    st.error(f'Deleted Category: {st.session_state.deleted}')
    st.session_state.deleted = False

st.header('Edit Categories')

with st.form(key='new_category_form',
             clear_on_submit=True):
    new_category = st.text_input(label='New Category',
                                 key='new_category')
    submitted = st.form_submit_button(label='Create Category')
    
    if submitted:
        if new_category.title() in categories_list():
            st.error('Category already exists')
        if new_category == '':
            st.error('Enter category name')
        else:
            add_category(new_category.title())
            st.session_state.created = new_category.title()

if st.session_state.created:
    st.success(f'Category Created: {st.session_state.created}')

df = get_categories()
df = df[df.category_name != 'None'].sort_values(by='category_name')

table = get_table()

st.markdown('***')

st.info('Deleting a category will set those item\'s category to \'None\'')

for idx, row in df.iterrows():
    with st.expander(row.category_name):
        st.write('Items in category:')
        category_items = table[table.category_name == row.category_name].item_name.values
        st.caption(', '.join(category_items))
        key = row.id + '_input'
        st.text_input(label='Input new category name:',
                      value=row.category_name,
                      key=key,
                      on_change=change_category,
                      args=(row.id, key, row.category_name))
        st.markdown('***')
        deleted = st.button(label=f'Delete {row.category_name}')
        
        if deleted:
            delete_category(row.id, row.category_name)
            st.session_state.deleted = row.category_name
            st.experimental_rerun()
