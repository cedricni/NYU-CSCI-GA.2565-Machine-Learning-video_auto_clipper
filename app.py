import streamlit as st
import time
import base64

def get_base64_of_file(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_up_styles():
    background_base64 = get_base64_of_file("bg.jpg")
    background_url = f"data:image/jpeg;base64,{background_base64}"
    css = f"""
    <style>
    .stApp {{
        background-image: url("{background_url}");
        background-size: cover;
        background-attachment: fixed; 
    }}
    .reportview-container .main .block-container{{
        background-color: rgba(255, 255, 255, 0.8); 
        padding: 5rem;
        border-radius: 25px;
    }}
    h1, h2, h3, h4, h5, h6 {{
        font-size: 1.5em;
    }}
    .css-1d391kg {{
        padding: 15px 30px;
        font-size: 20px;
    }}
    div, label, p, .stTextInput, .stSelectbox, .stDateInput, .stTimeInput {{
        font-size: 25px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_up_styles()

def check_login(username, password):
    return username == "admin" and password == "admin"

def login_page():
    st.title("Login to VAC")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_login(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['page'] = 'main'
            st.experimental_rerun()
        else:
            st.error("Incorrect Username/Password")

def main_page():
    st.title("Video Analysis Console")
    sidebar_navigation()
    video_file = st.file_uploader("Upload a video", type=['mp4', 'mov', 'avi', 'asf', 'm4v'])
    if video_file is not None:
        st.session_state['video_file'] = video_file
        st.session_state['video_display'] = video_file.getvalue()

    if 'video_display' in st.session_state:
        st.video(st.session_state['video_display'])

    if st.button("Process Video") and 'video_display' in st.session_state:
        st.session_state['processing'] = True
        st.experimental_rerun()

    if st.button("Clear Uploaded Video"):
        if 'video_display' in st.session_state:
            del st.session_state['video_display']
            del st.session_state['video_file']
            st.experimental_rerun()

def show_processing_page():
    st.empty()
    st.title("Processing...")
    time.sleep(2)
    st.session_state['processing'] = False
    st.session_state['page'] = 'display_results'
    st.experimental_rerun()

def display_results():
    st.title("Video Processing Completed. Displaying Results:")
    sidebar_navigation()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://via.placeholder.com/250")
        if st.button("Show Clips for Action 1", key="action1"):
            st.session_state['page'] = 'clip_view'
            st.experimental_rerun()
    with col2:
        st.image("https://via.placeholder.com/250")
        if st.button("Show Clips for Face 1", key="face1"):
            st.session_state['page'] = 'clip_view'
            st.experimental_rerun()
    with col3:
        st.image("https://via.placeholder.com/250")
        if st.button("Show Clips for Action 2", key="action2"):
            st.session_state['page'] = 'clip_view'
            st.experimental_rerun()

def clip_view_page():
    st.title("Video Clips")
    sidebar_navigation()
    if 'video_display' in st.session_state:
        st.video(st.session_state['video_display'])
    if st.button("Back to Results"):
        st.session_state['page'] = 'display_results'
        st.experimental_rerun()

def sidebar_navigation():
    st.sidebar.write(f"Logged in as {st.session_state['username']}")
    if st.sidebar.button("Logout"):
        logout_user()
    if st.sidebar.button("Home"):
        st.session_state['page'] = 'main'
        st.experimental_rerun()

def logout_user():
    st.session_state['logged_in'] = False
    st.session_state.pop('username', None)
    st.session_state['page'] = 'login'
    st.experimental_rerun()

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state['page'] = 'login'

    if st.session_state.get('processing', False):
        show_processing_page()
    elif not st.session_state.logged_in or st.session_state['page'] == 'login':
        login_page()
    elif st.session_state['page'] == 'main':
        main_page()
    elif st.session_state['page'] == 'display_results':
        display_results()
    elif st.session_state['page'] == 'clip_view':
        clip_view_page()

if __name__ == "__main__":
    main()