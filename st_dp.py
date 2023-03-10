"""
author: f.romadhana@gmail.com

"""

#import necessary libraries
import yaml
import pytz
import time
import pandas as pd
from PIL import Image
import streamlit as st
from time import sleep
from datetime import datetime
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth


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
        padding-bottom: 2rem;
    }} </style> """, unsafe_allow_html=True)

#hide streamlit menu and footer
hide_menu_style = """
          <style>
          #MainMenu {visibility: hidden; }
          footer {visibility: hidden;}
          </style>
          """
st.markdown(hide_menu_style, unsafe_allow_html=True)
 
# ---USER AUTHENTICATION--- #
with open('user.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state["authentication_status"] is False:
    st.error('Username & Password tidak terdaftar!')
if st.session_state["authentication_status"] is None:
    st.warning('Mohon isi Username & Password yang sudah diberikan!')

with open('user.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)


#if login success, display form so page
if st.session_state["authentication_status"]:
  #caching 
  @st.cache_data
  def process_for_index(index: int) -> int:
      sleep(0.5)
      return 2 * index + 1
  
  #sidebar
  authenticator.logout("Logout", "sidebar")
  st.sidebar.title(f"Hi, {name}!")

  #datetime now
  timenow = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%d-%m-%Y %H:%M:%S")
  time.sleep(1)
  
  #display streamlit form
  st.subheader("Penjualan Cash Hari Ini 💵")
  with st.form(key= "so_sell", clear_on_submit=True):
    #sisa stock kemarin
    col1, col2 = st.columns(2)
    st.write('''<style>
        [data-testid="column"] {
            width: calc(35% - 1rem) !important;
            flex: 1 1 calc(35% - 1rem) !important;
            min-width: calc(35% - 1rem) !important;
        }
        </style>''', unsafe_allow_html=True)
    
    with col1:
        ppj1 = st.selectbox("Produk", ('','Lapis', 'Bolu', 'Brokat', 'Bropang', 'Pie 6', 'Pie 8', 'Balok'))
        ppj2 = st.selectbox("p2", ('','Lapis', 'Bolu', 'Brokat', 'Bropang', 'Pie 6', 'Pie 8', 'Balok'), label_visibility="collapsed")
        ppj3 = st.selectbox("p3", ('','Lapis', 'Bolu', 'Brokat', 'Bropang', 'Pie 6', 'Pie 8', 'Balok'), label_visibility="collapsed")
        ppj4 = st.selectbox("p4", ('','Lapis', 'Bolu', 'Brokat', 'Bropang', 'Pie 6', 'Pie 8', 'Balok'), label_visibility="collapsed")
        ppj5 = st.selectbox("p5", ('','Lapis', 'Bolu', 'Brokat', 'Bropang', 'Pie 6', 'Pie 8', 'Balok'), label_visibility="collapsed")
        ppj6 = st.selectbox("p6", ('','Lapis', 'Bolu', 'Brokat', 'Bropang', 'Pie 6', 'Pie 8', 'Balok'), label_visibility="collapsed")      
        
    with col2:
        npj1 = st.number_input('Jumlah', step=1)
        npj2 = st.number_input('n2', label_visibility="collapsed", step=1)
        npj3 = st.number_input('n3', label_visibility="collapsed", step=1)
        npj4 = st.number_input('n4', label_visibility="collapsed", step=1)
        npj5 = st.number_input('n5', label_visibility="collapsed", step=1)
        npj6 = st.number_input('n6', label_visibility="collapsed", step=1)

    #submit button
    submitted = st.form_submit_button(label="**SUBMIT**", use_container_width=True, type="primary")
    if submitted:
        #sum all number
        sum_npj = npj1 + npj2 + npj3 + npj4 + npj5 + npj6
        #create dataframe
        df3 = pd.DataFrame({"Produk": [ppj1, ppj2, ppj3, ppj4, ppj5, ppj6], 
                            "Jumlah": [npj1, npj2, npj3, npj4, npj5, npj6]})
        #CSS to inject contained in a string
        hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
        #inject CSS with markdown
        hide = st.markdown(hide_table_row_index, unsafe_allow_html=True)
        container = st.container()
        container.write(":orange[Penjualan Cash]")
        st.table(df3)

        #show related information    
        st.write("Drop Point: {}".format(name))
        st.write("Tanggal/Jam : {}".format(timenow))
        st.write("Total Penjualan Cash : {}".format(sum_npj), "box")
            
    else:
        st.warning('Isi sesuai jumlah penjualan hari ini', icon="⚠️")
        st.stop()