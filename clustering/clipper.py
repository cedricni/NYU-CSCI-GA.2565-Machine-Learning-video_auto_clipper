import logging
import os
import glob
from PIL import Image
import unittest
import shutil

from clustering.faceCluster import FaceCluster
from pre_post_processing.vidClips import frame_duration, extract_clip
from pre_post_processing.vidToImg import extract_frames, detect_faces

class Clipper:
    def __init__(self):
        self.cluster = FaceCluster()

    def clip(self, input_path, output_dir):
        img_output_folder = "./temp_imgs"
        cropped_output_folder = "./temp_cluster"
        # extract frames from the video
        extract_frames(input_path, img_output_folder)
        # detect faces in frames and export cropped faces
        detect_faces(img_output_folder, cropped_output_folder)

        cluster_result = self.cluster.recognition(cropped_output_folder)
        logging.info(f"Finished clustering with {len(cluster_result['id'].unique())}")

        time_info = frame_duration(cluster_result)
        extract_clip(input_path, time_info, output_dir)

        # Delete intermediate products
        shutil.rmtree(cropped_output_folder)
        shutil.rmtree(img_output_folder)