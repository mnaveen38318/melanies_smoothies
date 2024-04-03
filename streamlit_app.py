# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits that you want in your custome smoothie
    """
)

name_on_smoothie = st.text_input("Name on Smoothie :")
st.write("The Name on Smoothie will be ", name_on_smoothie)

session = st.connection("snowflake").session()
my_df = session.table("smoothies.public.fruit_options").select(col("fruit_name"),col("search_on"))
#st.dataframe(data=my_df, use_container_width=True)
#st.stop()
pd_df = my_df.to_pandas()
st.dataframe(pd_df)
st.stop()

#st.dataframe(data=my_df, use_container_width=True)
ingrediets_list = st.multiselect("Choose up to 5 ingredients"
                                 , pd_df
                                ,max_selections = 5)

if ingrediets_list:
    ingrediemts_str = ''
    for f_choosen in ingrediets_list:
        ingrediemts_str+=f_choosen +' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == f_choosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', f_choosen,' is ', search_on, '.')
        
        st.subheader(f_choosen+' Nutritin Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+f_choosen)
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
        
    inser_stm = """insert into smoothies.public.orders (ingredients,name_on_order)
                    values('"""+ingrediemts_str+"""','"""+name_on_smoothie+"""')"""
    submit_bt = st.button('Submit')
    if submit_bt:
        session.sql(inser_stm).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


    
