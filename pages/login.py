import streamlit as st
from auth import login_user


def show_login():

    left, center, right = st.columns([1, 2, 1])

    with center:


        st.markdown(
            "<h1 style='text-align:center;'>WealthLens AI</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<h3 style='text-align:center;'>Welcome Back 👋</h3>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='text-align:center;color:gray;'>Login to continue your investment journey.</p>",
            unsafe_allow_html=True
        )

        st.write("")

        email = st.text_input(
            "Email",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        st.write("")

        if st.button("Login", use_container_width=True):

            if email == "" or password == "":
                st.warning("Please fill all fields.")

            else:

                user = login_user(email, password)

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user_id = user[0]
                    st.session_state.name = user[1]
                    st.session_state.email = user[2]

                    st.success(f"Welcome {user[1]}!")

                    st.session_state.page = "Dashboard"

                    st.rerun()

                else:

                    st.error("Invalid email or password.")

        st.write("")

        st.markdown(
            "<div style='text-align:center;'>Don't have an account?</div>",
            unsafe_allow_html=True
        )

        if st.button("Create Account", use_container_width=True):
            st.session_state.page = "Sign Up"
            st.rerun()