import streamlit as st

def require_auth():
    """Call at the top of every page. Returns True if admin, False if guest."""
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False

    with st.sidebar.expander("🔐 Admin Login", expanded=not st.session_state.is_admin):
        if not st.session_state.is_admin:
            admin_pw = st.text_input("Admin password", type="password", key="admin_pw_input")
            if st.button("Login", key="admin_login_btn"):
                if admin_pw == st.secrets["ADMIN_PASSWORD"]:
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.sidebar.error("Incorrect password")
        else:
            st.sidebar.success("✅ Logged in as admin")
            if st.button("Logout", key="admin_logout_btn"):
                st.session_state.is_admin = False
                st.rerun()

    return st.session_state.is_admin