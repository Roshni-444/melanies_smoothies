# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the Fruits you want in your Custom Smoothie!
  """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The Name on your smoothie will be", name_on_order)
cnx=st.connection("snowflake")
session = cnx.session()

# Get fruit options (Snowpark DataFrame)
my_dataframe = session.table('smoothies.public.fruit_options').select(
    col('FRUIT_NAME'), col('SEARCH_ON')
)

# Convert Snowpark DataFrame → Pandas DataFrame (so we can use .loc)
pd_df = my_dataframe.to_pandas()

# Show dataframe for debugging
st.dataframe(pd_df)
# st.stop()   # Uncomment if you want to pause execution here

# Let user pick ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'].tolist(),
    max_selections=5
)
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        # Look up the "search_on" value from your dataframe
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

        # Show fruit heading
        st.subheader(f"{fruit_chosen} Nutrition Information")

        # Call Fruityvice API with the search value
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on.rstrip('s')}")

        # Display API response as a dataframe
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    # Debug print of concatenated ingredients
    # st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" +name_on_order+ """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



        



        
name_on_order = st.text_input("Name on Smoothie:")
st.write("The Name on your smoothie will be", name_on_order)
cnx= st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect('choose upto 5 ingredients:' ,my_dataframe,max_selections=5)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string =''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" +name_on_order+ """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
        
