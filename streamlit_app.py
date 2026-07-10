#Python is famously finicky about indentation. In some ways it makes code simpler, but in other ways it can be frustrating. When using Streamlit in Snowflake, you can use either a tab character or four spaces to create rows at the same indentation level. It will look the same, and SiS will not complain. However, when you later copy your code out and paste it into Streamlit OG, those differences can come back to haunt you. To avoid this issue, choose four spaces for each indentation level instead of tabs.

# Import python packages, these are always first in code
import streamlit as st
import os
import requests

#load get active session command, without this get_active_session will not run
#from snowflake.snowpark.context import get_active_session --only required in Snowflake not github
# ONLY IN WAREHOUSE RUNTIMES
#added cnx line for Github
cnx = st.connection ("snowflake")
# session = get_active_session() #amended to cnx as per below for Github
session = cnx.session ()
session.sql("SELECT 1").collect()

#To use a Snowpark column function named `col`, we need to import it into our app. We’ll place the import statement close to where we plan to use it. This makes it easier for beginners to understand why it was imported and how it is used. In a later lab, we’ll move it up with other import statements to demonstrate better code organization.
from snowflake.snowpark.functions import col

# Write directly to the app
#Create title
st.title(f" :cup_with_straw: Customize your Smoothie! :cup_with_straw: ")
#Create sub header
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)
#Text input as per https://docs.streamlit.io/develop/api-reference/widgets/st.text_input
#Default will add import streamlit as st when coping. This is only required once at top of query
#this will not accept special characters yet
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be", name_on_order)

#default will add import streamlit as st when copying from https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox. This is not required a 2nd time as already show in line 2 above
#option = st.selectbox(
#    "What is your favourite fruit?",
#    ("Banana","Strawberries", "Peaches"),
#)

# Show option selected in st.selectbox defined as option above
# st.write("Your favourite fruit option is:", option)

#Load Snowflake table into app. This will only work if app has been deployed to Snowflake. https://discuss.streamlit.io/t/nameerror-name-get-active-session-is-not-defined/79970/2. This also requires the from statement under #load get active session (above) from statement as referenced here: https://docs.snowflake.com/en/developer-guide/streamlit/app-development/secrets-and-configuration
#To show entire table remove the .select(col) after the session.table table name. Otherwise the select.col can be used after the session.table to show a specific column from a Snowflake table
#session = get_active_session() #turned off as this is overwritten cnx session above
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#below is only required for displaying table within app itself
#st.dataframe(data=my_dataframe, use_container_width=True)

# Multi select option as defined in https://docs.streamlit.io/develop/api-reference/widgets/st.multiselect. Also includes select all by default. My_dataframe picks up the above definition as defined by a Snowflake table column
#ingredients is a variable and the data type is a list
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    #limits the number of options that can be selected in multi select
    max_selections=5
)

#adding 'if' means do everything after if when not null
# st.write displays the list as a row by row table based on user selection
# st.text displays the list as one row with '' seperators
if ingredients_list:
    #must have 4 spaces before command otherwise indent error. This indent ensures it is part of the IF block
    #st.write(ingredients_list) 
    #must have 4 spaces before commend otherwise indent error
    #st.text(ingredients_list) 
    
    #To convert a list to a string we need to create a varaible and make sure Python treats it as a string
    #This must also be indented by 4 spaces before command otherwise indent error
    #no space in between characters
    ingredients_string = '' 

    #This must be indented by 4 spaces before command otherwise indent error
    # Below means for each fruit_chosen in ingredients_list multiselect box do everything below that is indented
    #Although we did not define a fruit_chosen variable Python understands that whatever is placed in that position is a counter for items in the list
    #for creates a loop to review each row until there are no more rows available
    for fruit_chosen in ingredients_list:
        #indent to contain with for command
        #+= means add this to what is already in the variable. Each time the for loop is repeated a new fruit name is appended to the existing string
        #+ ' ' adds space character after each fruit chosen i.e. each for loop
        ingredients_string += fruit_chosen + ' '

    #This should be part of the IF block but not the FOR Loop
    #st.write (ingredients_string)

    #This must in IF block command i.e. indented
    #Insert Statement
    #Copy the text created in the app preview on the right (Not the code below) into a Snowflake query to check it works as expected.
    #add comma between columns as required to match Snowflake table for insert
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """','"""+name_on_order+ """')"""
    #Below will only work if there are entries in app such as selection box otherwise no query will show
    #Displays the SQL statement for insert into. See worksheet for this
    #Used to check insert is going to work correctly
    #st.write(my_insert_stmt)
    
    #allows for stopping of run so we can troubleshoot specifc parts of the code before it publishes to a database table in Snowflake
    #st.stop ()
    #insert button as per https://docs.streamlit.io/develop/api-reference/widgets/st.button
    #inserts text after Submit Order button clicked
    #use + between free text to add variables as needed
    time_to_insert = st.button ('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order, icon="✅")

smoothiefroot_response = requests.get("(https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response).json())

        
