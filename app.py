import streamlit as st
from streamlit_option_menu import option_menu

from pages.home import show_home
from pages.login import show_login
from pages.signup import show_signup
from pages.profile import show_profile
from pages.dashboard import show_dashboard

st.set_page_config(
    page_title="WealthLens AI",
    page_icon="💰",
    layout="wide"
)

hide_streamlit = """
<style>
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}
</style>
"""

st.markdown(hide_streamlit, unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

pages = ["Home", "Login", "Sign Up"]

if st.session_state.logged_in:
    pages.extend(["Profile", "Dashboard"])

icons = [
    "house",
    "box-arrow-in-right",
    "person-plus",
    "person",
    "speedometer2"
]

current_index = pages.index(st.session_state.page) if st.session_state.page in pages else 0

col1, col2 = st.columns([1, 5])

with col1:
    st.image("assets/logo.png", width=75)

with col2:
    selected = option_menu(
        menu_title=None,
        options=pages,
        icons=icons[:len(pages)],
        orientation="horizontal",
        default_index=current_index
    )

st.session_state.page = selected

if st.session_state.page == "Home":
    show_home()

elif st.session_state.page == "Login":
    show_login()

elif st.session_state.page == "Sign Up":
    show_signup()

elif st.session_state.page == "Profile":
    show_profile()

elif st.session_state.page == "Dashboard":
    show_dashboard()