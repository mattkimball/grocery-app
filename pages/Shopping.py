import streamlit as st
from main import add_item, get_table, update_list, get_items, add_to_list

st.header('Shopping List')

with st.expander('Add Items to List'):
    col1, col2 = st.columns(2)
    
    with col1:
        table = get_table()
        items_on_list = table[table.on_list == False].item_name.values
        st.selectbox(label='Add Exisitng Items',
                     options=items_on_list,
                     key='item_to_add')
        st.button(label='Add Existing Item',
                  on_click=add_to_list,
                  args=(st.session_state.item_to_add,))
    with col2:
        new_item = st.text_input(label='Add New Item').title()
        
        submitted = st.button(label='Add New Item')
        if submitted:
            if new_item == '':
                st.error('Enter item name')
            elif new_item in get_items():
                add_to_list(new_item)
            else:
                add_item(new_item, 'None', 'Out')
                add_to_list(new_item)
            st.experimental_rerun()

st.markdown('***')

table = get_table()

if table.on_list.any() == False:
    st.info('Nothing on the list!')
else:
    for idx, row in table[table.on_list == True].iterrows():
        st.checkbox(label=f'{row.item_name} [{row.status}]',
                    key=row['id'] + '_added')

    st.markdown('***')
    
    st.button(label='Submit Purchases',
              on_click=update_list)