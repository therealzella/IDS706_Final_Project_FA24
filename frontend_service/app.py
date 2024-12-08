import random
import time
import streamlit as st
from streamlit_option_menu import option_menu
from frontend_service.configs import CONTENT_COL_CONFIG
from frontend_service.app_pages.home import show_home_page
from frontend_service.app_pages.function import show_function_page

# --- PAGE CONFIG AND NAV SESSION STATE---
st.set_page_config(page_title="Review Analyzer", layout="wide")

if 'menu_option' not in st.session_state:
    st.session_state['menu_option'] = 'Home'

menu_options = [
    {"label": "Home", "icon": "house"},
    {"label": "Try", "icon": "rocket"}
]

top_menu = option_menu(None, [option["label"] for option in menu_options], 
                      icons=[option["icon"] for option in menu_options], 
                      menu_icon="cast", default_index=0, orientation="horizontal")

def show_page_footers():
    _, center, _ = st.columns(CONTENT_COL_CONFIG)
    with center:
        st.markdown("© 2024 Review Analyzer")

if top_menu == "Home": 
    show_home_page()
elif top_menu == "Try": 
    show_function_page()

show_page_footers()