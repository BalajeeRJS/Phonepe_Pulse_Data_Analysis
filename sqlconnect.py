import mysql.connector
import streamlit as st

@st.cache_resource
def db_connection():
  mydb = mysql.connector.connect(host=st.secrets['AWS_endpoint'],
                                 user=st.secrets['AWS_username'],
                                 password=st.secrets['AWS_pwd'],
                                 database=st.secrets['AWS_db'])
  print("I am connecting")
  return mydb

