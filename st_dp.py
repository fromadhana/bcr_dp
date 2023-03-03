"""
author: f.romadhana@gmail.com

"""

#import necessary libraries
import pytz
import time
import pandas as pd
import db_deta as db
from PIL import Image
import streamlit as st
from time import sleep
from datetime import datetime
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
 
# ---USER AUTHENTICATION---
users = db.fetch_all_user()
username = [user["key"] for user in users]
names = [user["name"] for user in users]
hashed_password =[user["password"] for user in users]
authenticator = stauth.Authenticate(names, username, hashed_password, 
                                    "form_so", "sodp", cookie_expiry_days=30)
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
  st.error("Username & Password tidak terdaftar!")
if authentication_status == None:
  st.warning("Mohon isi Username & Password yang sudah diberikan!")

#if login success, display form so page
if authentication_status:
  #caching 
  @st.cache_data
  def process_for_index(index: int) -> int:
      sleep(0.5)
      return 2 * index + 1
  
  #sidebar
  authenticator.logout("Logout", "sidebar")
  st.sidebar.title(f"Hi, {name}!")

  #banner information
  url = "https://i.ibb.co/y0PvNK7/dp-mobile-7.png"
  st.image(url, use_column_width=True)
  #hide fullscreen image
  hide_img_fs = '''
  <style>
  button[title="View fullscreen"]{
      visibility: hidden;}
  </style>
  '''
  st.markdown(hide_img_fs, unsafe_allow_html=True)

  #subheader
  st.caption("**FORM STOCK OPNAME DROP POINT** 🏠")

  #display streamlit form
  with st.form(key= "form_so", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
      #datetime now
      tp = st.date_input(label="**Tanggal Hari ini**")
      timenow = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%d-%m-%Y %H:%M:%S")
      time.sleep(1)

    with col2:
      #selectbox for stock opname session
      so_sm = st.selectbox('**Sesi Siang/Malam?**', ('SIANG', 'MALAM'))
    
    #sisa stock sebelumnya
    col3, col4, col5 = st.columns(3)
    st.markdown("**Sisa Stock Sebelumnya** ⏪️")
    with col3:
      st.write('''<style>
      [data-testid="column"] {
          width: calc(45% - 1rem) !important;
          flex: 1 1 calc(33.3333% - 1rem) !important;
          min-width: calc(45% - 1rem) !important;
      }
      </style>''', unsafe_allow_html=True)
      p1 = st.selectbox("Produk", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'))
      p2 = st.selectbox("p2", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")
      p3 = st.selectbox("p3", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")
      p4 = st.selectbox("p4", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")
      p5 = st.selectbox("p5", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")
      p6 = st.selectbox("p6", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")      

    with col4:
      st.write('''<style>
      [data-testid="column"] {
          width: calc(33.3333% - 1rem) !important;
          flex: 1 1 calc(33.3333% - 1rem) !important;
          min-width: calc(33% - 1rem) !important;
      }
      </style>''', unsafe_allow_html=True)
      n1 = st.text_input('Jumlah')
      n2 = st.text_input('n2', label_visibility="collapsed")
      n3 = st.text_input('n3', label_visibility="collapsed")
      n4 = st.text_input('n4', label_visibility="collapsed")
      n5 = st.text_input('n5', label_visibility="collapsed")
      n6 = st.text_input('n6', label_visibility="collapsed")
    
    with col5:
      st.write('''<style>
      [data-testid="column"] {
          width: calc(33.3333% - 1rem) !important;
          flex: 1 1 calc(33.3333% - 1rem) !important;
          min-width: calc(33% - 1rem) !important;
      }
      </style>''', unsafe_allow_html=True)
      t1 = st.text_input('Expired')
      t2 = st.text_input('t2', label_visibility="collapsed")
      t3 = st.text_input('t3', label_visibility="collapsed")
      t4 = st.text_input('t4', label_visibility="collapsed")
      t5 = st.text_input('t5', label_visibility="collapsed")
      t6 = st.text_input('t6', label_visibility="collapsed")

    #submit button
    submitted = st.form_submit_button(label="**SUBMIT**", use_container_width=True, type='primary')
    if submitted:
      #show related information
      st.write("Tanggal/Jam : {}".format(timenow))
      st.write("Stock Opname : {}".format(so_sm))

    else:
      st.warning('Isi sesuai jumlah stock yang ada di drop point', icon="⚠️")
      st.stop()