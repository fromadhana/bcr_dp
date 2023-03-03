"""
author: f.romadhana@gmail.com

"""

#import necessary libraries
import pytz
import time
import pandas as pd
from PIL import Image
import streamlit as st
from time import sleep
from datetime import datetime

#set page configuration
st.set_page_config(
  page_title="Form SO Drop Point",
  page_icon="🏠",
  layout="wide")

#set padding page
st.markdown(f""" <style>
      .block-container{{
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 0rem;
    }} </style> """, unsafe_allow_html=True)

#hide streamlit menu and footer
hide_menu_style = """
          <style>
          #MainMenu {visibility: hidden; }
          footer {visibility: hidden;}
          </style>
          """
st.markdown(hide_menu_style, unsafe_allow_html=True)

#caching 
@st.cache_data
def process_for_index(index: int) -> int:
    sleep(0.5)
    return 2 * index + 1

#banner information
url = "https://i.ibb.co/M5VyxXS/dp-mobile-3.png"
st.image(url, use_column_width=True)
#hide fullscreen image
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''
st.markdown(hide_img_fs, unsafe_allow_html=True)

#display streamlit form
with st.form(key= "form_so", clear_on_submit=True):
   col1, col2 = st.columns(2)
   with col1:
     #datetime now
     st.markdown("""
    <style>
    [data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{
        gap: 0rem;
    }
    </style>
    """,unsafe_allow_html=True)
     tp = st.date_input(label="**Tanggal Stock Opname** 📅")
     timenow = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%d-%m-%Y %H:%M:%S")
     time.sleep(1)

   with col2:
     #selectbox for stock opname session
     st.markdown("""
    <style>
    [data-testid=column]:nth-of-type(2) [data-testid=stVerticalBlock]{
        gap: 0rem;
    }
    </style>
    """,unsafe_allow_html=True)
     so_sm = st.selectbox('**Stock Opname Siang/Malam**?🌞🌙', ('SIANG', 'MALAM'))
     
   #submit button
   submitted = st.form_submit_button(label="**SUBMIT**", use_container_width=True, type='primary')
   if submitted:
    #show related information
    st.write("Tanggal/Jam : {}".format(timenow))
    st.write("Stock Opname : {}".format(so_sm))

   else:
    st.warning('Isi sesuai jumlah stock yang ada di drop point', icon="⚠️")
    st.stop()