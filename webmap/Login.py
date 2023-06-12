import streamlit as st
import pyrebase
from datetime import datetime
from pathlib import Path
import json
from streamlit.source_util import _on_pages_changed, get_pages
from streamlit_extras.switch_page_button import switch_page
import traceback
import logging

# Firebase configuration keys
firebaseConfig = {
  'apiKey': "AIzaSyCa1MRReuUd0xpwHCVXMoSBGE1CV40r6XE",
  'authDomain': "web-map-5766a.firebaseapp.com",
  'projectId': "web-map-5766a",
  'databaseURL': "https://web-map-5766a-default-rtdb.europe-west1.firebasedatabase.app/",
  'storageBucket': "web-map-5766a.appspot.com",
  'messagingSenderId': "408124257003",
  'appId': "1:408124257003:web:16ceb63827c758fa4b44ae",
  'measurementId': "G-52GPNVM6SZ"
}

DEFAULT_PAGE = "Login"
SECOND_PAGE_NAME = "Home"

def get_all_pages():
    default_pages = get_pages(DEFAULT_PAGE)

    pages_path = Path("pages.json")

    if pages_path.exists():
        saved_default_pages = json.loads(pages_path.read_text())
    else:
        saved_default_pages = default_pages.copy()
        pages_path.write_text(json.dumps(default_pages, indent=4))

    return saved_default_pages

def clear_all_but_first_page():
    current_pages = get_pages(DEFAULT_PAGE)

    if len(current_pages.keys()) == 1:
        return

    get_all_pages()

    # Remove all but the first page
    key, val = list(current_pages.items())[0]
    current_pages.clear()
    current_pages[key] = val

    _on_pages_changed.send()

def show_all_pages():
    current_pages = get_pages(DEFAULT_PAGE)

    saved_pages = get_all_pages()

    # Replace all the missing pages
    for key in saved_pages:
        if key not in current_pages:
            current_pages[key] = saved_pages[key]

    _on_pages_changed.send()

def hide_page(name: str):
    current_pages = get_pages(DEFAULT_PAGE)

    for key, val in current_pages.items():
        if val["page_name"] == name:
            del current_pages[key]
            _on_pages_changed.send()
            break

clear_all_but_first_page()

# Password check 
# Firebase authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()

# initialize state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Main function
def main():
    # """Login page"""
    st.title("welcome! ")
    menu = ["Login", "SignUp"]
    choice = st.selectbox(
        "Select Login or SignUp from dropdown box ▾",
        menu,
    )
    st.markdown(
        "<h10 style='text-align: left; color: #ffffff;'> If you do not have an account, create an accouunt by select SignUp option from above dropdown box.</h10>",
        unsafe_allow_html=True,
    )
    if choice == "":
        st.subheader("Login")
    elif choice == "Login":
        st.write("-------")
        st.subheader("Log in to the App")

        email = st.text_input("User Name", placeholder="email")

        password = st.text_input("Password", type="password")

        if st.checkbox("Login"):
            try:
                user = auth.sign_in_with_email_and_password(email,password)

                if  user:
                    st.session_state["logged_in"] = True
                    st.success("Logged In as {}".format(email))    
            except Exception as e:
                st.warning('Incorrect login details')         

    elif choice == "SignUp":
        st.write("-----")
        st.subheader("Create New Account")
        new_user = st.text_input("Username", placeholder="name")
        new_user_email = st.text_input("Email id", placeholder="email")
        new_password = st.text_input("Password", type="password")

        if st.button("Signup"):
            if new_user == "":  # if user name empty then show the warnings
                st.warning("Inavlid user name")
            elif new_user_email == "":  # if email empty then show the warnings
                st.warning("Invalid email id")
            elif new_password == "":  # if password empty then show the warnings
                st.warning("Invalid password")
            else:
                user = auth.create_user_with_email_and_password(new_user_email, new_password)
                st.success('Your account has been successfully created')
                st.balloons()
                # Sign in
                user = auth.sign_in_with_email_and_password(new_user_email, new_password)
                db.child(user['localId']).child('new_user').set(new_user)
                db.child(user['localId']).child('ID').set(user['localId'])
                st.title('Welcome' + new_user)
                st.info('Succefully Signed up, Login using dropdown select')

    if st.session_state["logged_in"]:
        show_all_pages()
        hide_page(DEFAULT_PAGE.replace(".py", ""))
        switch_page(SECOND_PAGE_NAME)
    else:
        clear_all_but_first_page()


if __name__ == "__main__":
    main()