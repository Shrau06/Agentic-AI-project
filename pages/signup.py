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
            placeholder="Enter your full name"
        )

        email = st.text_input(
            "Email",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm your password"
        )

        st.write("")

        if st.button("Create Account", use_container_width=True):

            if not name or not email or not password or not confirm_password:
                st.warning("Please fill all fields.")

            elif password != confirm_password:
                st.error("Passwords do not match.")

            elif len(password) < 8:
                st.error("Password must be at least 8 characters long.")

            else:

                success = register_user(
                    name,
                    email,
                    password
                )

                if success:

                    st.success("🎉 Account created successfully!")

                    st.info("You can now login with your credentials.")

                    if st.button("Go to Login"):
                        st.session_state.page = "Login"
                        st.rerun()

                else:

                    st.error("An account with this email already exists.")

        st.write("")

        st.markdown(
            "<div style='text-align:center;'>Already have an account?</div>",
            unsafe_allow_html=True
        )

        if st.button("Login Instead", use_container_width=True):
            st.session_state.page = "Login"
            st.rerun()