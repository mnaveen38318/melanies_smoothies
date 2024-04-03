# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits that you want in your custome smoothie
    """
)

name_on_smoothie = st.text_input('Name on Smoothie :')
st.write('The Name on Smoothie will be ', name_on_smoothie)

session = get_active_session()
my_df = session.table('smoothies.public.fruit_options').select(col('fruit_name'))
#st.dataframe(data=my_df, use_container_width=True)
ingrediets_list = st.multiselect('Choose up to 5 ingredients'
                                 , my_df
                                ,max_selections = 5)

if ingrediets_list:
    ingrediemts_str = ''
    for f_choosen in ingrediets_list:
        ingrediemts_str+=f_choosen +' '
    inser_stm = """insert into smoothies.public.orders (ingredients,name_on_order)
                    values('"""+ingrediemts_str+"""','"""+name_on_smoothie+"""')"""
    submit_bt = st.button('Submit')
    if submit_bt:
        session.sql(inser_stm).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    
