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
if authentication_status ==True:
  #caching 
  @st.cache_data
  def process_for_index(index: int) -> int:
      sleep(0.5)
      return 2 * index + 1
  
  #sidebar
  authenticator.logout("Logout", "sidebar")
  st.sidebar.title(f"Hi, {name}!")

  #subheader
  st.subheader("**Form Stock Opname Drop Point** 🏠")
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

  #datetime now
  timenow = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%d-%m-%Y %H:%M:%S")
  time.sleep(1)

  
  #display streamlit form
  def run_first_tab():
    with tab1:
      st.header("Sisa Stock Sebelumnya")
      with st.form(key= "so_before", clear_on_submit=True):
        so_sm = st.selectbox('**Sesi Siang/Malam?**', ('SIANG', 'MALAM'))
        
        #sisa stock sebelumnya
        st.caption('**Sisa stock sebelumnya** ⏪️' )
        col1, col2, col3 = st.columns(3)
        st.write('''<style>
          [data-testid="column"] {
              width: calc(33.3333% - 1rem) !important;
              flex: 1 1 calc(33.3333% - 1rem) !important;
              min-width: calc(33% - 1rem) !important;
          }
          </style>''', unsafe_allow_html=True)
        with col1:
          pss1 = st.selectbox("Produk", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'))
          pss2 = st.selectbox("p2", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")
          pss3 = st.selectbox("p3", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")
          pss4 = st.selectbox("p4", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")
          pss5 = st.selectbox("p5", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")
          pss6 = st.selectbox("p6", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")      

        with col2:
          nss1 = st.text_input('Jumlah')
          nss2 = st.text_input('n2', label_visibility="collapsed")
          nss3 = st.text_input('n3', label_visibility="collapsed")
          nss4 = st.text_input('n4', label_visibility="collapsed")
          nss5 = st.text_input('n5', label_visibility="collapsed")
          nss6 = st.text_input('n6', label_visibility="collapsed")
        
        with col3:
          tss1 = st.text_input('Expired')
          tss2 = st.text_input('t2', label_visibility="collapsed")
          tss3 = st.text_input('t3', label_visibility="collapsed")
          tss4 = st.text_input('t4', label_visibility="collapsed")
          tss5 = st.text_input('t5', label_visibility="collapsed")
          tss6 = st.text_input('t6', label_visibility="collapsed")

        #submit button
        submitted = st.form_submit_button(label="**SUBMIT**", use_container_width=True)
        if submitted:
          #show related information
          st.write("Tanggal/Jam : {}".format(timenow))
          st.write("Stock Opname : {}".format(so_sm))

        else:
          st.warning('Isi sesuai jumlah stock yang ada di drop point', icon="⚠️")
          st.stop()
    return None
  
  def run_second_tab():
    with tab2:
      st.header("Stock Masuk Hari Ini")
      with st.form(key= "so_today", clear_on_submit=True):
        so_sm = st.selectbox('**Sesi Siang/Malam?**', ('SIANG', 'MALAM'))
        
        #stock masuk hari ini
        st.caption('**Stock Masuk Hari Ini** ⤵️' )
        col6, col7, col8 = st.columns(3)
        st.write('''<style>
          [data-testid="column"] {
              width: calc(33.3333% - 1rem) !important;
              flex: 1 1 calc(33.3333% - 1rem) !important;
              min-width: calc(33% - 1rem) !important;
          }
          </style>''', unsafe_allow_html=True)
        with col6:
          pmh1 = st.selectbox("Produk", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'))
          pmh2 = st.selectbox("p2", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")
          pmh3 = st.selectbox("p3", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")
          pmh4 = st.selectbox("p4", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")
          pmh5 = st.selectbox("p5", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")
          pmh6 = st.selectbox("p6", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")      

        with col7:
          nmh1 = st.text_input('Jumlah')
          nmh2 = st.text_input('n2', label_visibility="collapsed")
          nmh3 = st.text_input('n3', label_visibility="collapsed")
          nmh4 = st.text_input('n4', label_visibility="collapsed")
          nmh5 = st.text_input('n5', label_visibility="collapsed")
          nmh6 = st.text_input('n6', label_visibility="collapsed")
        
        with col8:
          tmh1 = st.text_input('Expired')
          tmh2 = st.text_input('t2', label_visibility="collapsed")
          tmh3 = st.text_input('t3', label_visibility="collapsed")
          tmh4 = st.text_input('t4', label_visibility="collapsed")
          tmh5 = st.text_input('t5', label_visibility="collapsed")
          tmh6 = st.text_input('t6', label_visibility="collapsed")

        #submit button
        submitted = st.form_submit_button(label="**SUBMIT**", use_container_width=True)
        if submitted:
          #show related information
          st.write("Tanggal/Jam : {}".format(timenow))
          st.write("Stock Opname : {}".format(so_sm))

        else:
          st.warning('Isi sesuai jumlah stock yang ada di drop point', icon="⚠️")
          st.stop()
    return None
  
  def run_third_tab():
    with tab3: 
      st.header("Penjualan Hari Ini")
      with st.form(key= "so_endday", clear_on_submit=True):
        so_sm = st.selectbox('**Sesi Siang/Malam?**', ('SIANG', 'MALAM'))
        
        #Penjualan Hari Ini
        st.caption('**Penjualan Hari Ini** ⤴️' )
        col9, col10, col11 = st.columns(3)
        st.write('''<style>
          [data-testid="column"] {
              width: calc(33.3333% - 1rem) !important;
              flex: 1 1 calc(33.3333% - 1rem) !important;
              min-width: calc(33% - 1rem) !important;
          }
          </style>''', unsafe_allow_html=True)
        with col9:
          pph1 = st.selectbox("Produk", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'))
          pph2 = st.selectbox("p2", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")
          pph3 = st.selectbox("p3", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")
          pph4 = st.selectbox("p4", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")
          pph5 = st.selectbox("p5", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")
          pph6 = st.selectbox("p6", ('','LTK', 'BSK', 'BPK', 'BSK', 'PI6', 'PI8'), label_visibility="collapsed")      

        with col10:
          nph1 = st.text_input('Jumlah')
          nph2 = st.text_input('n2', label_visibility="collapsed")
          nph3 = st.text_input('n3', label_visibility="collapsed")
          nph4 = st.text_input('n4', label_visibility="collapsed")
          nph5 = st.text_input('n5', label_visibility="collapsed")
          nph6 = st.text_input('n6', label_visibility="collapsed")
        
        with col11:
          tph1 = st.text_input('Expired')
          tph2 = st.text_input('t2', label_visibility="collapsed")
          tph3 = st.text_input('t3', label_visibility="collapsed")
          tph4 = st.text_input('t4', label_visibility="collapsed")
          tph5 = st.text_input('t5', label_visibility="collapsed")
          tph6 = st.text_input('t6', label_visibility="collapsed")

        #submit button
        submitted = st.form_submit_button(label="**SUBMIT**", use_container_width=True)
        if submitted:
          #show related information
          st.write("Tanggal/Jam : {}".format(timenow))
          st.write("Stock Opname : {}".format(so_sm))

        else:
          st.warning('Isi sesuai jumlah stock yang ada di drop point', icon="⚠️")
          st.stop()
    return None
  tab1, tab2, tab3 = st.tabs(["Sisa Stock Sebelumnya", "Stock Masuk Hari Ini", "Penjualan Hari Ini"])
  run_first_tab()
  run_second_tab()
  run_third_tab()