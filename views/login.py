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

        if "signup_success_msg" in st.session_state and st.session_state.signup_success_msg:
            st.success(st.session_state.signup_success_msg)
            del st.session_state.signup_success_msg

        email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="login_email_field"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password_field"
        )

        st.write("")

        if st.button("Login", key="login_submit_btn", use_container_width=True):

            if not email.strip() or not password:
                st.warning("Please fill all fields.")

            else:

                user = login_user(email.strip().lower(), password)

                if user:
                    # Clear any leftover session state from previous user
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]

                    st.session_state.logged_in = True
                    st.session_state.user_id = user[0]
                    st.session_state.name = user[1]
                    st.session_state.email = user[2]

                    # Load this user's profile from DB
                    from database import get_user_profile, get_default_profile, save_user_profile
                    user_profile = get_user_profile(user[0])
                    if not user_profile:
                        user_profile = get_default_profile()
                        save_user_profile(user[0], user_profile)

                    st.session_state.profile = user_profile
                    st.session_state.page = "Financial Dashboard"
                    st.rerun()

                else:

                    st.error("Invalid email or password.")

        st.write("")

        st.markdown(
            "<div style='text-align:center; margin-top: 10px;'>Don't have an account?</div>",
            unsafe_allow_html=True
        )

        if st.button("Create Account", key="login_to_signup_btn", use_container_width=True):
            st.session_state.page = "Sign Up"
            st.rerun()