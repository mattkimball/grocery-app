# grocery-app
A grocery management app for tracking items, making shopping lists, and creating meal templates. Created for fun as a way to practice python, databases, and api calls.

## App Overview
- Written in python
- Database is stored and accessed through an [Airtable](https://airtable.com/) base
- Python library and hosting service: [Streamlit](https://streamlit.io/)


### Features
- Keep list of grocery or other shopping items
- Update the status and category of items
- Add items to a shopping list and track purchases
- Create meal templates with existing items and add instructions
- Edit and delete items, categories, and meals within the app

# Setup
This app makes use of several Airtable tables under the same base. Once set up, add your user api key, base id, and table ids to a secrets file on Streamlit.

## Airtable Setup
The four tables and their columns
- Items
  - item_name (single line text)
  - status (single select: Good, Low, Out)
  - on_list (checkbox)
  - last_purchased (date)
  - category_name (single line text)
- Categories
  - category_name (single line text)
- Purchases
  - item_name (single line text)
  - date_purchased (date)
- Meals
  - meal_name (single line text)
  - ingredients (long text)
  - instructions (long text)

## Secrets File
Onces the tables are created, access the api keys through [Airtable's Rest API](https://airtable.com/api).

Add a folder named `.streamlit` to the root directory of the app and created a file named `secrets.toml`. Then update the file with the following key-value pairs with the ids for your Airtable account:
```
base_id = ''
api_key = ''

item_table = ''
category_table = ''
purchases_table = ''
meals_table = ''
```
This will allow you to run the app offline. The file does not have to be committed to Git for the app to run: if you build the app through Streamlit (using their [app sharing service](https://share.streamlit.io/), copy the contents of `secrets.toml` in the apps settings and ignore it in Git commits.

The values are accessed by Streamlit in the `st.secrets` values in the code.

## Future
Some features I plan on adding:
- A way to categorize meals by mealtime and prep/cook time
- A meal suggesting page that looks at available items
- Expiration dates, freeze by dates, frozen on dates, the like
- Adding to a meal shopping list that will prompt items to buy from those meals

## That's it
Thanks for stopping by :wave:
