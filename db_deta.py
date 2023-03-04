"""
author: f.romadhana@gmail.com

"""
from deta import Deta 
import streamlit as st


#initialize with a project key
DETA_KEY = st.secrets["deta_key"]
deta = Deta(DETA_KEY)

#connect deta database
db = deta.Base("bcr_dp")

def insert_user(username, name, password):
    """Returns the user on a succesful user creation, otherwise raises an error"""
    return db.put({"key": username, "name": name, "password": password})

