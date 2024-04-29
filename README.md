# Video Auto-clipper App

## Overview
The Video Auto-clipper App is a Streamlit-based application designed for automating the process of locating and clipping specific characters or actions in video files. Developed as part of the NYU CSCI-GA 2565 Machine Learning course, this app utilizes advanced machine learning techniques for face and action recognition to streamline video editing.

Try the live app: [Video Auto-clipper](https://vedioautoclipper-n6jcncachknycsullwmsot.streamlit.app/)

## Team Members
- Lubin Sun
- Cedric Ni
- Zhiheng Wang
- Helen Zhou

## Features
- **Face Recognition**: Automatically identify and extract video segments featuring a specific character.
- **Action Recognition**: Locate and clip scenes based on particular actions within the video.
- **Time-saving**: Provides timestamps for each character's appearance to ease the editing process.

## Usage
1. Upload your video file to the app.
2. Specify the character or action you wish to clip.
3. Let the app process the video and provide you with the timestamps and clips.

## How It Works
The app uses [insert technology/algorithms used], enabling it to analyze video content efficiently. Face and action recognition are powered by [insert specific machine learning models or libraries used].

## Installation
To run the app locally, follow these steps:

```bash
git clone [repository-link]
cd [repository-name]
pip install -r requirements.txt
streamlit run app.py
