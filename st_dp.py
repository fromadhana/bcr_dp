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

if authentication_status == False:
  st.error("Username & Password tidak terdaftar!")
if authentication_status == None:
  st.warning("Mohon isi Username & Password yang sudah diberikan!")

with open('user.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)

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

  #datetime now
  timenow = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%d-%m-%Y %H:%M:%S")
  time.sleep(1)
  
  #display streamlit form
  def main_page():
      st.subheader("Sisa Stock Kemarin ⏪️")
      with st.form(key= "so_yesterday", clear_on_submit=True):
        #sisa stock kemarin
        col1, col2, col3 = st.columns(3)
        st.write('''<style>
            [data-testid="column"] {
                width: calc(33.3333% - 1rem) !important;
                flex: 1 1 calc(33.3333% - 1rem) !important;
                min-width: calc(33% - 1rem) !important;
            }
            </style>''', unsafe_allow_html=True)
        st.markdown("""
                          <style>
                              button.step-up {display: none;}
                              button.step-down {display: none;}
                              div[data-baseweb] {border-radius: 4px;}
                          </style>""",
                        unsafe_allow_html=True)
        with col1:
            pss1 = st.selectbox("Produk", ('','Lapis', 'Bolu', 'Bropang', 'Brokat', 'Pie 6', 'Pie 8', "Balok"))
            pss2 = st.selectbox("p2", ('','Lapis', 'Bolu', 'Bropang', 'Brokat', 'Pie 6', 'Pie 8', "Balok"), label_visibility="collapsed")
            pss3 = st.selectbox("p3", ('','Lapis', 'Bolu', 'Bropang', 'Brokat', 'Pie 6', 'Pie 8', "Balok"), label_visibility="collapsed")
            pss4 = st.selectbox("p4", ('','Lapis', 'Bolu', 'Bropang', 'Brokat', 'Pie 6', 'Pie 8', "Balok"), label_visibility="collapsed")
            pss5 = st.selectbox("p5", ('','Lapis', 'Bolu', 'Bropang', 'Brokat', 'Pie 6', 'Pie 8', "Balok"), label_visibility="collapsed")
            pss6 = st.selectbox("p6", ('','Lapis', 'Bolu', 'Bropang', 'Brokat', 'Pie 6', 'Pie 8', "Balok"), label_visibility="collapsed")      

        with col2:
            nss1 = st.number_input('Jumlah', min_value=0, step=1)
            nss2 = st.number_input('n2', min_value=0, label_visibility="collapsed", step=1)
            nss3 = st.number_input('n3', min_value=0, label_visibility="collapsed", step=1)
            nss4 = st.number_input('n4', min_value=0, label_visibility="collapsed", step=1)
            nss5 = st.number_input('n5', min_value=0, label_visibility="collapsed", step=1)
            nss6 = st.number_input('n6', min_value=0, label_visibility="collapsed", step=1)
          
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
          col3 = st.columns(1)
          with col3:
              st.markdown("""
                          <style>
                          [data-testid=column]:nth-of-type(3) [data-testid=stVerticalBlock]{
                              gap: 0rem;
                          }
                          </style>
                          """,unsafe_allow_html=True)
              st.write("Drop Point: {}".format(name))
              st.write("Tanggal/Jam : {}".format(timenow))
              st.write("Total Sisa Stock Kemarin : {}".format(sum_nss), "box")
             
        else:
          st.warning('Isi sesuai jumlah stock yang ada di drop point', icon="⚠️")
          st.stop()
    
  def page2():
      st.subheader("Stock Masuk Hari Ini ⤵️")
      with st.form(key= "so_today", clear_on_submit=True):
        #sisa stock kemarin
        col1, col2, col3 = st.columns(3)
        st.write('''<style>
            [data-testid="column"] {
                width: calc(33.3333% - 1rem) !important;
                flex: 1 1 calc(33.3333% - 1rem) !important;
                min-width: calc(33% - 1rem) !important;
            }
            </style>''', unsafe_allow_html=True)
        st.markdown("""
                          <style>
                              button.step-up {display: none;}
                              button.step-down {display: none;}
                              div[data-baseweb] {border-radius: 4px;}
                          </style>""",
                        unsafe_allow_html=True)
        with col1:
            pst1 = st.selectbox("Produk", ('','LTK', 'BSK', 'BRP', 'BRS', 'PI6', 'PI8'))
            pst2 = st.selectbox("p2", ('','LTK', 'BSK', 'BRP', 'BRS', 'PI6', 'PI8'), label_visibility="collapsed")
            pst3 = st.selectbox("p3", ('','LTK', 'BSK', 'BRP', 'BRS', 'PI6', 'PI8'), label_visibility="collapsed")
            pst4 = st.selectbox("p4", ('','LTK', 'BSK', 'BRP', 'BRS', 'PI6', 'PI8'), label_visibility="collapsed")
            pst5 = st.selectbox("p5", ('','LTK', 'BSK', 'BRP', 'BRS', 'PI6', 'PI8'), label_visibility="collapsed")
            pst6 = st.selectbox("p6", ('','LTK', 'BSK', 'BRP', 'BRS', 'PI6', 'PI8'), label_visibility="collapsed")      

        with col2:
            nst1 = st.number_input('Jumlah', step=1)
            nst2 = st.number_input('n2', label_visibility="collapsed", step=1)
            nst3 = st.number_input('n3', label_visibility="collapsed", step=1)
            nst4 = st.number_input('n4', label_visibility="collapsed", step=1)
            nst5 = st.number_input('n5', label_visibility="collapsed", step=1)
            nst6 = st.number_input('n6', label_visibility="collapsed", step=1)
          
        with col3:
            tst1 = st.text_input('Expired')
            tst2 = st.text_input('t2', label_visibility="collapsed")
            tst3 = st.text_input('t3', label_visibility="collapsed")
            tst4 = st.text_input('t4', label_visibility="collapsed")
            tst5 = st.text_input('t5', label_visibility="collapsed")
            tst6 = st.text_input('t6', label_visibility="collapsed")

        #submit button
        submitted = st.form_submit_button(label="**SUBMIT**", use_container_width=True, type="primary")
        if submitted:
          #sum all number
          sum_nst = nst1 + nst2 + nst3 + nst4 + nst5 + nst6
          #create dataframe
          df2 = pd.DataFrame({"Produk": [pst1, pst2, pst3, pst4, pst5, pst6], 
                              "Jumlah Stock": [nst1, nst2, nst3, nst4, nst5, nst6], 
                              "Tanggal Expired": [tst1, tst2, tst3, tst4, tst5, tst6]})
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
          container.write(":orange[Jumlah Stock Masuk]")
          st.table(df2)
          #show related information
          col3 = st.columns(1)
          with col3:
              st.markdown("""
                          <style>
                          [data-testid=column]:nth-of-type(3) [data-testid=stVerticalBlock]{
                              gap: 0rem;
                          }
                          </style>
                          """,unsafe_allow_html=True)
              st.write("Drop Point: {}".format(name))
              st.write("Tanggal/Jam : {}".format(timenow))
              st.write("Total Stock Masuk : {}".format(sum_nst), "box")
             
        else:
          st.warning('Isi sesuai jumlah stock yang ada di drop point', icon="⚠️")
          st.stop()
      
      
  def page3():
      st.subheader("Penjualan Hari Ini 💵")
      with st.form(key= "so_sell", clear_on_submit=True):
        #sisa stock kemarin
        col1, col2, col3 = st.columns(3)
        st.write('''<style>
            [data-testid="column"] {
                width: calc(33.3333% - 1rem) !important;
                flex: 1 1 calc(33.3333% - 1rem) !important;
                min-width: calc(33% - 1rem) !important;
            }
            </style>''', unsafe_allow_html=True)
        st.markdown("""
                          <style>
                              button.step-up {display: none;}
                              button.step-down {display: none;}
                              div[data-baseweb] {border-radius: 4px;}
                          </style>""",
                        unsafe_allow_html=True)
        with col1:
            ppj1 = st.selectbox("Produk", ('','LTK', 'BSK', 'BRP', 'BRS', 'PI6', 'PI8'))
            ppj2 = st.selectbox("p2", ('','LTK', 'BSK', 'BRP', 'BRS', 'PI6', 'PI8'), label_visibility="collapsed")
            ppj3 = st.selectbox("p3", ('','LTK', 'BSK', 'BRP', 'BRS', 'PI6', 'PI8'), label_visibility="collapsed")
            ppj4 = st.selectbox("p4", ('','LTK', 'BSK', 'BRP', 'BRS', 'PI6', 'PI8'), label_visibility="collapsed")
            ppj5 = st.selectbox("p5", ('','LTK', 'BSK', 'BRP', 'BRS', 'PI6', 'PI8'), label_visibility="collapsed")
            ppj6 = st.selectbox("p6", ('','LTK', 'BSK', 'BRP', 'BRS', 'PI6', 'PI8'), label_visibility="collapsed")      

        with col2:
            opj1 = st.selectbox("Cash/OL", ('','Cash','Gojek', 'Grab', 'Shopee', 'AirAsia'))
            opj2 = st.selectbox("o2", ('','Cash','Gojek', 'Grab', 'Shopee', 'AirAsia'), label_visibility="collapsed")
            opj3 = st.selectbox("o3", ('','Cash','Gojek', 'Grab', 'Shopee', 'AirAsia'), label_visibility="collapsed")
            opj4 = st.selectbox("o4", ('','Cash','Gojek', 'Grab', 'Shopee', 'AirAsia'), label_visibility="collapsed")
            opj5 = st.selectbox("o5", ('','Cash','Gojek', 'Grab', 'Shopee', 'AirAsia'), label_visibility="collapsed")
            opj6 = st.selectbox("o6", ('','Cash','Gojek', 'Grab', 'Shopee', 'AirAsia'), label_visibility="collapsed")
          
        with col3:
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
                              "Cash/Online": [opj1, opj2, opj3, opj4, opj5, opj6],
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
          container.write(":orange[Jumlah Stock Masuk]")
          st.table(df3)
          #show related information
          col3 = st.columns(1)
          with col3:
              st.markdown("""
                          <style>
                          [data-testid=column]:nth-of-type(3) [data-testid=stVerticalBlock]{
                              gap: 0rem;
                          }
                          </style>
                          """,unsafe_allow_html=True)
              st.write("Drop Point: {}".format(name))
              st.write("Tanggal/Jam : {}".format(timenow))
              st.write("Total Stock Masuk : {}".format(sum_npj), "box")
             
        else:
          st.warning('Isi sesuai jumlah stock yang ada di drop point', icon="⚠️")
          st.stop()




  page_names_to_funcs = {
     "Sisa Stock Sebelumnya": main_page,
     "Stock Masuk Hari Ini": page2,
     "Penjualan Hari Ini": page3
  }

  selected_page = st.sidebar.selectbox("Pilih Halaman", page_names_to_funcs.keys())
  page_names_to_funcs[selected_page]()