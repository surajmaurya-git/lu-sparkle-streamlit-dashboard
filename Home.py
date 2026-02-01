"""Sparkle Dashboard  by Anedya"""

import streamlit as st
import os
import json
import requests
from streamlit_autorefresh import st_autorefresh
from streamlit_db.session_storage import initialize_session_state
from cloud.firestore.firestore_client_handler import firebase_db_setup
from css.control_streamlit_cloud_features import hide_streamlit_style
from cloud.anedya_cloud import Anedya
from users_ui.admin.admin_dashboard import drawAdminDashboard
from users_ui.users.users_units_dashboard import drawUsersDashboard

DASHBOARD_NAME=st.secrets["DASHBOARD_NAME"]
st.set_page_config(page_title=DASHBOARD_NAME, layout="wide")

refresh_interval = 30000
st_autorefresh(interval=refresh_interval, limit=None, key="auto-refresh-handler", debounce=True)


# --------------- HELPER FUNCTIONS -----------------------
def V_SPACE(lines):
    for _ in range(lines):
        st.write("&nbsp;")



def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    if "LoggedIn" not in st.session_state:
        st.session_state.LoggedIn = False
    
    # Load Custom CSS
    load_css("css/style.css")
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # ---------------------- UI ---------------------------------------
    if st.session_state.LoggedIn is False:
        project_setup()
        drawLogin()
    else:
        if st.session_state.view_role == "admin" or st.session_state.view_role == "super-admin":
            drawAdminDashboard()
        else:
            drawUsersDashboard()


def project_setup():
    initialize_session_state() # Initialize Session State
    # firebase_db_setup()  # Firebase client Setup
    st.session_state.http_client =requests.Session()
    # Manage Anedya Connection Credentials
    API_KEY=st.secrets["API_KEY"]
    anedya= Anedya()
    anedya_client = anedya.new_client(API_KEY)
    st.session_state.anedya_client = anedya_client

    NODES_ID = os.getenv("NODES_ID")
    NODES_ID_JSON = json.loads(NODES_ID)
    st.session_state.nodesId=NODES_ID_JSON
    VARIABLES = os.getenv("VARIABLES")
    VARIABLES_JSON = json.loads(VARIABLES)
    st.session_state.variables=VARIABLES_JSON


def drawLogin():
    current_dir=os.getcwd()
    NODES_NAME=st.session_state.nodesId["identifier"]
    pages = {
        f"{NODES_NAME}s": [
            st.Page(f"{current_dir}/nodes/node.py", title="Node"),
        ]
    }
    st.navigation(pages,position="hidden")

    # Centered Layout with Glassmorphism feel
    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        
        # Smart RO Icon
        try:
            subcol = st.columns([1, 1, 1])
            with subcol[1]:
                st.image("images/smart_ro_icon.png", width=120)
        except Exception:
            pass # Fallback if image fails
            
        # Using the accent color for the 'Smart' part or entire title
        st.markdown('<p class="login-title">Smart RO Dashboard</p>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">Intelligent Water Purification System</p>', unsafe_allow_html=True)
        
        username_inp = st.text_input("Email", placeholder="admin@example.com").strip()
        password_inp = st.text_input("Password", type="password", placeholder="••••••••").strip()
        
        st.write("") # Spacer
        
        if st.button("Sign In", use_container_width=True):
            check_credentials(username_inp, password_inp)
            
        st.markdown('</div>', unsafe_allow_html=True)


def check_credentials(username,password):
    if username == st.secrets["SUPER_ADMIN_EMAIL"] and password == st.secrets["SUPER_ADMIN_CRED"]:
        st.session_state.view_role = "super-admin"
        st.session_state.LoggedIn = True
        st.rerun()
    if username == st.secrets["ADMIN_EMAIL"] and password == st.secrets["ADMIN_CRED"]:
        st.session_state.view_role = "admin"
        st.session_state.LoggedIn = True
        st.rerun()

    user_details = st.session_state.firestore_client.collection("users").document(username).get().to_dict()
    if user_details is None:
        st.error("Invalid Credential!")
        st.stop()
    if password != user_details["password"]:
        st.error("Incorrect Password!")
        st.stop()

    if user_details["role"] == "admin":
        st.session_state.view_role = "admin"
        st.session_state.LoggedIn = True
        st.rerun()
    elif user_details["role"] == "user":
        st.session_state.view_role = "user"
        st.session_state.user_permissions = user_details["permissions"]
        st.session_state.user_variables_access = user_details["variables_access"]
        st.session_state.LoggedIn = True
        st.rerun()

if __name__ == "__main__":
    main()
