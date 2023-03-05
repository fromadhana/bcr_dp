"""
author: f.romadhana@gmail.com

"""

#import necessary libraries
import yaml
import streamlit as st
from time import sleep
from datetime import datetime
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth


with open('user.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
hashed_passwords = stauth.Hasher(['abc', 'def']).generate()

try:
    if authenticator.register_user('Register user', preauthorization=False):
        st.success('User registered successfully')
except Exception as e:
    st.error(e)

with open('user.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)