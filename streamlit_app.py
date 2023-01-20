import streamlit as st

st.title('My Parents New Healthy Diner')

st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas as pa
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

import requests
fv_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

fv_normalized = pa.json_normalize(fv_response.json())
st.dataframe(fv_normalized)

import snowflake.connector

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
st.text("The fruit load list is: ")
st.text(my_data_rows)



