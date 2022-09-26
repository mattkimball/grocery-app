import streamlit as st
from main import get_table, delete_item

st.header('Delete an item')
st.text_input(label='Search for item',
              key='text_input')

st.markdown('***')

table = get_table()
table = table[table.item_name.str.contains(st.session_state.text_input,
                                           case=False)]

for idx, row in table.iterrows():
    col1, col2, col3 = st.columns([1, 1, 5])
    
    with col1:
        st.caption(' ')
        st.markdown(f'##### {row.item_name}')
    
    with col2:
        st.caption(' ')
        st.button(label='Delete',
                    key=row.id + '_delete',
                    on_click=delete_item,
                    args=(row.id, st.secrets.item_table))
    
    st.markdown('***')