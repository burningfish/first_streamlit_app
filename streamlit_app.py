import streamlit as st
import pandas as pa
import requests
import snowflake.connector
from urllib.error import URLError

st.title('My Parents New Healthy Diner')

st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pa.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')  # set index as Fruit (name)

# Pick list so users can pick what fruits they want
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on screen
st.dataframe(fruits_to_show)

# New section to display fruityvice api response
st.header("Fruityvice Fruit Advice!")
fruit_choice = st.text_input('What fruit would you like information about?', 'Kiwi')
st.write('The user entered', fruit_choice)


fv_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

fv_normalized = pa.json_normalize(fv_response.json())
st.dataframe(fv_normalized)


my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list order by fruit_name")
my_data_rows = my_cur.fetchall()

st.header("The fruit load list is: ")
st.dataframe(my_data_rows)

# Allow users to add to the fruit list
fruit_to_add = st.text_input('Add a new fruit')
st.write('Thanks for adding ', fruit_to_add)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
