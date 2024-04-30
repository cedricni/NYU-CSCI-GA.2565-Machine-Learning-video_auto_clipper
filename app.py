import streamlit as st
import time
import base64
import os
from pathlib import Path
import random

from clustering.clipper import Clipper

def display_videos_starting_with_digit(directory, digit):
    """
    Display video files from the specified directory that start with the given digit.

    Parameters:
        directory (str): The directory containing the video files.
        digit (int): The digit (0-9) that the video filenames should start with.
    """
    # List all files in the directory
    video_files = [f for f in os.listdir(directory) if f.endswith(('.mp4', '.mov', '.avi', '.mkv')) and f.startswith(str(digit))]
    
    if video_files:
        # Display each video file
        for video_file in video_files:
            video_path = os.path.join(directory, video_file)
            st.video(video_path)
            st.write(video_file)  # Optionally display the file name
    else:
        st.write(f"No video files found in the directory starting with digit {digit}.")

def display_random_image_from_directory(directory):
    # Ensure the directory exists
    if not os.path.exists(directory):
        st.error("Directory does not exist.")
        return

    # List all files in the directory
    files = os.listdir(directory)
    # Optionally filter for specific file extensions (e.g., jpg, png)
    image_files = [file for file in files if file.endswith(('.jpg', '.jpeg', '.png'))]

    if not image_files:
        st.error("No image files found in the directory.")
        return

    # Randomly select an image file
    chosen_image = random.choice(image_files)
    image_path = os.path.join(directory, chosen_image)

    # Display the image
    st.image(image_path)

def save_video_file(video_file):
    # Define the directory to save videos
    video_dir = Path('uploaded_videos')
    video_dir.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist

    # Define the path to save the video
    video_path = video_dir / video_file.name

    # Write the video file to the specified path
    with open(video_path, 'wb') as f:
        f.write(video_file.getvalue())  # Write the video content to a local file
    
    return video_path

def delete_video_file(file_path):
    # Remove the video file from the directory
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

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
        font-size: 3.5em;
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
            st.rerun()
        else:
            st.error("Incorrect Username/Password")

def main_page():
    st.title("Video Analysis Console")
    # Assume sidebar_navigation() is defined elsewhere in your script
    sidebar_navigation()

    # Initialize a key for the file uploader to control its reset behavior
    video_file = st.file_uploader("Upload a video", type=['mp4', 'mov', 'avi', 'asf', 'm4v'], key='file_uploader')

    if video_file is not None:
        video_path = save_video_file(video_file)  # Save the video file
        st.session_state['video_file_path'] = video_path  # Store the file path in the session
        st.session_state['video_display'] = video_file.getvalue()
        st.success(f"Video saved to {video_path}")  # Notify the user where the video was saved
        st.video(st.session_state['video_display'])

    if 'video_display' in st.session_state:
        if st.button("Process Video"):
            st.session_state['start_processing'] = True  # Set flag to start processing
            st.session_state['processing'] = True  # Processing is ongoing
            st.session_state['page'] = 'processing'
            st.rerun()  # Rerun the app to switch to processing page


    if 'video_display' in st.session_state:
        if st.button("Clear Uploaded Video"):
            video_path = st.session_state.get('video_file_path', '')
            if video_path and delete_video_file(video_path):  # Delete the file from the directory
                st.success("Video file has been deleted.")
            else:
                st.error("Failed to delete the video file or file not found.")
            # Reset the file uploader widget by deleting its key in session state
            del st.session_state['file_uploader']
            # Remove video related session states
            del st.session_state['video_display']
            if 'video_file' in st.session_state:
                del st.session_state['video_file']
            if 'video_file_path' in st.session_state:
                del st.session_state['video_file_path']
            # Rererun the app to reset to the default page
            st.rerun()

def processing_page():
    if st.session_state.get('start_processing', False):  # Check if processing should start
        st.title("Processing Video...")
        # Perform processing here
        cliper = Clipper()
        input_path = './uploaded_videos/input.mp4'
        output_dir = './test_output'
        cliper.clip(input_path, output_dir)
        # Processing done, update state
        st.session_state['start_processing'] = False  # Prevent reprocessing
        st.session_state['processing'] = False  # Processing finished
        st.session_state['page'] = 'display_results'
        st.rerun()  # Rerun the app to update the page



def display_results():
    st.title("Video Processing Completed. Displaying Top 3 Results:")
    sidebar_navigation()
    col1, col2, col3 = st.columns(3)
    with col1:
        display_random_image_from_directory("./tmp/clustered/0")
        if st.button("Show Clips for Face 1", key="face1"):
            st.session_state['video_digit'] = 0
            st.session_state['page'] = 'clip_view'
            st.rerun()
    with col2:
        display_random_image_from_directory("./tmp/clustered/1")
        if st.button("Show Clips for Face 2", key="face2"):
            st.session_state['video_digit'] = 1
            st.session_state['page'] = 'clip_view'
            st.rerun()
    with col3:
        display_random_image_from_directory("./tmp/clustered/2")
        if st.button("Show Clips for Face 3", key="face3"):
            st.session_state['video_digit'] = 2
            st.session_state['page'] = 'clip_view'
            st.rerun()

def clip_view_page():
    st.title("Video Clips")
    sidebar_navigation()
    if 'video_digit' in st.session_state:
        display_videos_starting_with_digit("./test_output", st.session_state['video_digit'])
    else:
        st.write("Select a face category to view corresponding clips.")

    if st.button("Back to Results"):
        st.session_state['page'] = 'display_results'
        st.rerun()


def sidebar_navigation():
    st.sidebar.write(f"Logged in as {st.session_state['username']}")
    if st.sidebar.button("Logout"):
        logout_user()
    if st.sidebar.button("Home"):
        st.session_state['page'] = 'main'
        st.rerun()

def logout_user():
    st.session_state['logged_in'] = False
    st.session_state.pop('username', None)
    st.session_state['page'] = 'login'
    st.rerun()

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state['page'] = 'login'

    if st.session_state.get('processing', False):
        processing_page()
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