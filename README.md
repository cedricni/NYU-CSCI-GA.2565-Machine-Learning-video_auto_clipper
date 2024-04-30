# Video Auto-clipper App

## Overview
The Video Auto-clipper App is a Streamlit-based application designed for automating the process of locating and clipping specific characters or actions in video files. Developed as part of the NYU CSCI-GA 2565 Machine Learning course, this app utilizes advanced machine learning techniques for face and action recognition to streamline video editing.

Try the live app: [Video Auto-clipper](https://vedioautoclipper-n6jcncachknycsullwmsot.streamlit.app/) or watch the [demo video](https://youtu.be/hSCzFqr9dg0?si=HMgs1iJGpHbmq_Lz).
- username: admin
- pwd: admin

## Team Members
- Lubin Sun
- Cedric Ni
- Zhiheng Wang
- Helen Zhou

## Features
- **Face Recognition**: Automatically identify and extract video segments featuring a specific character.
- **Time-saving**: Provides timestamps for each character's appearance to ease the editing process.
- **(future)Action Recognition**: Locate and clip scenes based on particular actions within the video.

## Usage
1. Upload your video file to the app.
2. Click 'Process Video'.
3. Let the app process the video and provide you with the clips.

## How It Works
The app uses streamlit, enabling it to analyze video content efficiently. Face and action recognition are powered by MTCNN.

## Installation for Local Running
To run the app locally, follow these steps:

```bash
git clone [repository-link]
cd [repository-name]
pip install -r requirements.txt
streamlit run app.py
