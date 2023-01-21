import streamlit as st
import pandas as pa
import requests
import snowflake.connector
from urllib.error import URLError

st.title('My Parents New Healthy Diner')

#### static menu
st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞Avocado Toast')

#### smoothie builder
st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pa.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')  # set index as Fruit (name)

# Pick list so users can pick what fruits they want
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on screen
st.dataframe(fruits_to_show)

#### Show selected fruit info from Fruityvice
# Create fruityvice request/response function
def get_fruityvice_data(this_fruit_choice):
    fv_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # clean up json response and output on screen
    fv_normalized = pa.json_normalize(fv_response.json())
    return fv_normalized

# New section to display fruityvice api response
st.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  
  if not fruit_choice:
    st.error("Please enter a fruit to get information.")
  else:
    fv_fruit_details = get_fruityvice_data(fruit_choice)
    st.dataframe(fv_fruit_details)

except URLError as e:
  st.error()
    
#### Snowflake section - show fruit list and allow users to add
st.header("The fruit load list is: ")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list order by fruit_name")
        return my_cur.fetchall()
    
# Add a button to load the fruit
if st.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    st.dataframe(my_data_rows)

st.stop() # while debugging
    
# Allow users to add to the fruit list
def insert_snowflake_fruit(new_fruit):
    with my_cnx.cursor as my_cur
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
    return "Thanks for adding " + new_fruit

fruit_to_add = st.text_input('What fruit would you like to add?')
if st.button('Add a fruit'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    insert_response_text = insert_snowflake_fruit(fruit_to_add)
    st.text(insert_response_text)

