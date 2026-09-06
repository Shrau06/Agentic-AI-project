import streamlit as st
from auth import register_user


def show_signup():

    left, center, right = st.columns([1, 2, 1])

    with center:

        st.markdown(
            "<h1 style='text-align:center;'>WealthLens AI</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<h3 style='text-align:center;'>Create Your Account</h3>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='text-align:center;color:gray;'>Start your AI-powered investment journey.</p>",
            unsafe_allow_html=True
        )

        st.write("")

        name = st.text_input(
            "Full Name",
            placeholder="Enter your full name",
            key="signup_name_field"
        )

        email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="signup_email_field"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password (min 8 chars)",
            key="signup_password_field"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm your password",
            key="signup_confirm_password_field"
        )

        st.write("")

        if st.button("Create Account", key="signup_submit_btn", use_container_width=True):

            if not name.strip() or not email.strip() or not password or not confirm_password:
                st.warning("Please fill all fields.")

            elif password != confirm_password:
                st.error("Passwords do not match.")

            elif len(password) < 8:
                st.error("Password must be at least 8 characters long.")

            else:

                success = register_user(
                    name.strip(),
                    email.strip().lower(),
                    password
                )

                if success:
                    # Clear session state so new user starts completely fresh
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.session_state.signup_success_msg = "🎉 Account created successfully! Please log in."
                    st.session_state.page = "Login"
                    st.rerun()
                else:
                    st.error("An account with this email already exists.")

        st.write("")

        st.markdown(
            "<div style='text-align:center; margin-top: 10px;'>Already have an account?</div>",
            unsafe_allow_html=True
        )

        if st.button("Login Instead", key="signup_to_login_btn", use_container_width=True):
            st.session_state.page = "Login"
            st.rerun()