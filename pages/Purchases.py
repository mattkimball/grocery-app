import streamlit as st
from main import get_purchases, get_items

purchases = get_purchases()

st.header('Purchases')
item_filter = st.multiselect(label='Filter items',
                             options=get_items())

if item_filter:
    purchases = purchases[purchases.item_name.isin(item_filter)]

st.markdown('***')

for date in purchases.date_purchased.unique():
    st.subheader(date)
    item_list = purchases[purchases.date_purchased == date].item_name.values
    for item in item_list:
        st.caption(item)