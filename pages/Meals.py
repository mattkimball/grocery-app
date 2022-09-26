import streamlit as st
from main import get_meals, get_items, update_meal, create_meal

meals = get_meals()

st.header('Meals')
col1, col2 = st.columns(2)
with col1:
    st.text_input(label='Search for meal',
                  key='meal_input')
    st.checkbox(label='Edit meals',
                key='edit_meals')
with col2:
    st.multiselect(label='Search by ingredient',
                   options=get_items(),
                   key='ingredient_input')

if st.session_state.meal_input:
    meals = meals[meals.meal_name.str.contains(st.session_state.meal_input,
                                               case=False)]

if st.session_state.ingredient_input:
    for ingredient in st.session_state.ingredient_input:
        meals = meals[meals.ingredients.str.contains(ingredient,
                                                     case=False)]

with st.expander('Create New Meal'):
    with st.form(key='new_meal', clear_on_submit=True):
        meal_name = st.text_input('Meal Name').title()
        instructions = st.text_area('Instructions', height=129)
        ingredients = st.multiselect(label='Ingredients', options=get_items())
        
        submitted = st.form_submit_button('Create Meal')
        if submitted:
            create_meal(meal_name=meal_name,
                        ingredients=ingredients,
                        instructions=instructions)
            st.experimental_rerun()

st.markdown('***')

if len(meals) == 0:
    st.info('No meals found')
else:
    for idx, row in meals.iterrows():
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(row.meal_name)
            st.caption(row.ingredients)
        with col2:
            with st.expander('Instructions'):
                st.caption(row.instructions)
        if st.session_state.edit_meals:
            with st.expander(f'Edit {row.meal_name}'):
                with st.form(key=row.id + '_edit_form'):
                    new_name = st.text_input(label='Meal Name',
                                             value=row.meal_name)
                    new_instructions = st.text_area(label='Instructions',
                                                    value=row.instructions,
                                                    key=row.id + '_instructions',
                                                    height=129)
                    
                    cur_ingredients = row.ingredients.split(', ')
                    new_ingredients = st.multiselect(label='Ingredients',
                                                     options=get_items(),
                                                     default=cur_ingredients)
                    
                    submitted = st.form_submit_button('Submit Changes')
                    if submitted:
                        if new_name.strip() != '' and new_ingredients != []:
                            update_meal(id=row.id,
                                        meal_name=new_name,
                                        ingredients=new_ingredients,
                                        instructions=new_instructions)
                            st.success(f'Updated {new_name}')
                            
        st.markdown('***')