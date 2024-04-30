import logging
import os
import glob
from PIL import Image
import unittest
import shutil

from clustering.faceCluster import FaceCluster
from pre_post_processing.vidClips import frame_duration, extract_clip
from pre_post_processing.vidToImg import extract_frames, detect_faces, folder_creation

class Clipper:
    def __init__(self):
        self.cluster = FaceCluster()

    def clip(self, input_path, output_dir):
        folder_creation('./tmp')
        img_output_folder = "./tmp/frames"
        cropped_output_folder = "./tmp/cropped"
        # extract frames from the video
        extract_frames(input_path, img_output_folder)
        # detect faces in frames and export cropped faces
        detect_faces(img_output_folder, cropped_output_folder)
        # Alternative approach: use mtcnn
        # self.cluster.batch_crop(img_output_folder, cropped_output_folder)

        cluster_result = self.cluster.recognition(cropped_output_folder)

        cluster_result.to_csv('./tmp/result.csv')
        cluster_folder = './tmp/clustered'
        os.makedirs(cluster_folder, exist_ok=True)

        # Iterate over the DataFrame
        for index, row in cluster_result.iterrows():
            # Folder path based on 'id'
            folder_path = os.path.join(cluster_folder, str(row['id']))
            # Ensure this subdirectory exists
            os.makedirs(folder_path, exist_ok=True)

            # Define source and destination file paths
            source_file = os.path.join(cropped_output_folder, row['file_name'])
            destination_file = os.path.join(folder_path, row['file_name'])
            # Move the file
            shutil.move(source_file, destination_file)

        logging.info(f"Finished clustering with {len(cluster_result['id'].unique())}")

        time_info = frame_duration(cluster_result)
        extract_clip(input_path, time_info, output_dir)

        # Delete intermediate products
        # shutil.rmtree(cropped_output_folder)
        # shutil.rmtree(img_output_folder)