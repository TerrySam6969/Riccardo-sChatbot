import streamlit as st
from langchain_helper import Reply
from streamlit_option_menu import option_menu
from multiapp import MultiApp
from apps import database,home

app = MultiApp()

app.add_app("Home", home.app)
app.add_app("Database", database.app)

app.run()