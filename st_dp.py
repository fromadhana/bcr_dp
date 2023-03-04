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
  def main_page():
      st.header("Sisa Stock Kemarin ⏪️")
      with st.form(key= "so_before", clear_on_submit=True):
        #sisa stock kemarin
        col1, col2, col3 = st.columns(3)
        st.write('''<style>
            [data-testid="column"] {
                width: calc(33.3333% - 1rem) !important;
                flex: 1 1 calc(33.3333% - 1rem) !important;
                min-width: calc(33% - 1rem) !important;
            }
            </style>''', unsafe_allow_html=True)
        with col1:
            pss1 = st.selectbox("Produk", ('','LTK', 'BSK', 'BRP', 'BRS', 'PI6', 'PI8'))
            pss2 = st.selectbox("p2", ('','LTK', 'BSK', 'BRP', 'BRS', 'PI6', 'PI8'), label_visibility="collapsed")
            pss3 = st.selectbox("p3", ('','LTK', 'BSK', 'BRP', 'BRS', 'PI6', 'PI8'), label_visibility="collapsed")
            pss4 = st.selectbox("p4", ('','LTK', 'BSK', 'BRP', 'BRS', 'PI6', 'PI8'), label_visibility="collapsed")
            pss5 = st.selectbox("p5", ('','LTK', 'BSK', 'BRP', 'BRS', 'PI6', 'PI8'), label_visibility="collapsed")
            pss6 = st.selectbox("p6", ('','LTK', 'BSK', 'BRP', 'BRS', 'PI6', 'PI8'), label_visibility="collapsed")      

        with col2:
            nss1 = st.number_input('Jumlah', step=1)
            nss2 = st.number_input('n2', label_visibility="collapsed", step=1)
            nss3 = st.number_input('n3', label_visibility="collapsed", step=1)
            nss4 = st.number_input('n4', label_visibility="collapsed", step=1)
            nss5 = st.number_input('n5', label_visibility="collapsed", step=1)
            nss6 = st.number_input('n6', label_visibility="collapsed", step=1)
          
        with col3:
            tss1 = st.text_input('Expired')
            tss2 = st.text_input('t2', label_visibility="collapsed")
            tss3 = st.text_input('t3', label_visibility="collapsed")
            tss4 = st.text_input('t4', label_visibility="collapsed")
            tss5 = st.text_input('t5', label_visibility="collapsed")
            tss6 = st.text_input('t6', label_visibility="collapsed")

        #submit button
        submitted = st.form_submit_button(label="**SUBMIT**", use_container_width=True, type="primary")
        if submitted:
          #sum all number
          sum_nss = nss1 + nss2 + nss3 + nss4 + nss5 + nss6
          #create dataframe
          df1 = pd.DataFrame({"Produk": [pss1, pss2, pss3, pss4, pss5, pss6], 
                              "Jumlah Stock": [nss1, nss2, nss3, nss4, nss5, nss6], 
                              "Tanggal Expired": [tss1, tss2, tss3, tss4, tss5, tss6]})
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
          container.write(":orange[Jumlah Sisa Stock Kemarin]")
          st.table(df1)
          #show related information
          st.markdown("""
                      <style>
                      [data-testid=column]:nth-of-type(4) [data-testid=stVerticalBlock]{
                          gap: 0rem;
                      }
                      </style>
                      """,unsafe_allow_html=True)
          st.write("Drop Point: {}".format(name))
          st.write("Tanggal/Jam : {}".format(timenow))
          st.write("Total Sisa Stock Kemarin : {}".format(sum_nss))

        else:
          st.warning('Isi sesuai jumlah stock yang ada di drop point', icon="⚠️")
          st.stop()
    
  def page2():
      st.header("Stock Masuk Hari Ini")
      with st.form(key= "so_today", clear_on_submit=True):
       
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

        else:
          st.warning('Isi sesuai jumlah stock yang ada di drop point', icon="⚠️")
          st.stop()
      
  page_names_to_funcs = {
     "Sisa Stock Sebelumnya": main_page,
     "Stock Masuk Hari ini": page2,
  }

  selected_page = st.sidebar.selectbox("Pilih Halaman", page_names_to_funcs.keys())
  page_names_to_funcs[selected_page]()