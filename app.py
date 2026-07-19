import streamlit as st
from streamlit_option_menu import option_menu

from pages.home import show_home
from pages.login import show_login
from pages.signup import show_signup

hide_streamlit = """
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

</style>
"""

st.markdown(hide_streamlit, unsafe_allow_html=True)

st.set_page_config(
    page_title="WealthLens AI",
    page_icon="💰",
    layout="wide"
)

# Initialize current page
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Navigation Bar
col1, col2 = st.columns([1, 5])

with col1:
    st.image("assets/logo.png", width=75)

with col2:
    selected = option_menu(
        menu_title=None,
        options=["Home", "Login", "Sign Up"],
        icons=["house", "box-arrow-in-right", "person-plus"],
        orientation="horizontal",
    )

st.session_state.page = selected

# Page Routing
if selected == "Home":
    show_home()

elif selected == "Login":
    show_login()

elif selected == "Sign Up":
    show_signup()