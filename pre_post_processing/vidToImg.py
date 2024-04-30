import cv2
import os
import shutil

"""
Check if output folder already exists, 
delete previous result and create new folder for outputs
"""
def folder_creation(output_folder):
    if os.path.exists(output_folder):
        print("output folder already exists. Deleting existing folder...")
        shutil.rmtree(output_folder)

    print("Creating new output folder...")
    os.makedirs(output_folder)


"""
convert mp4 to frames every 1s
inputs:
    video_path: path to mp4 file
    output_folder: name a new output folder name for frame images
outputs: 
    a new folder in the local directory with frame images
"""
def extract_frames(video_path, output_folder):

    folder_creation(output_folder)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("error: unable to open video file.")
        return
    
    # read frames interval = 1s
    frame_count = 0
    frame_interval_ms = 1000
    
    # store frames to output folder 
    while True:
        cap.set(cv2.CAP_PROP_POS_MSEC, frame_count * frame_interval_ms)
        ret, frame = cap.read()
        if not ret:
            break
        timestamp_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
        frame_path = f"{output_folder}/frame_{frame_count}_{int(timestamp_ms)}.jpg"
        cv2.imwrite(frame_path, frame)
        frame_count += 1
    
    cap.release()
    print(f"frames extracted: {frame_count}")


"""
detect face and output cropped images of faces 
inputs:
    video_path: path to mp4 file
    output_folder: name a new output folder name
outputs: 
    a new folder in the local directory with frame images
"""
def detect_faces(folder_path, output_folder):

    folder_creation(output_folder)
    
    # load the pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # process each frame in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            # read the frame and detect face
            frame_path = os.path.join(folder_path, filename)
            frame = cv2.imread(frame_path)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            # crop and save detected faces
            if len(faces) > 0:
                for i, (x, y, w, h) in enumerate(faces):
                    face = frame[y:y+h, x:x+w]
                    face = cv2.resize(face, (160, 160))
                    face_output_path = os.path.join(output_folder, f"{filename}")
                    cv2.imwrite(face_output_path, face)
    print("face cropping export completed.")


if __name__ == "__main__":
    input_file = "input.mp4"
    img_output_folder = "imgs"
    cropped_output_folder = "cropped"
    
    # extract frames from the video
    extract_frames(input_file, img_output_folder)
    
    # detect faces in frames and export cropped faces
    detect_faces(img_output_folder, cropped_output_folder)
