import logging
import os
import glob
from PIL import Image
import unittest
# import natsort
import shutil

from clustering.faceCluster import FaceCluster
from clustering.clipper import Clipper
from pre_post_processing.vidClips import frame_duration, extract_clip
from pre_post_processing.vidToImg import extract_frames, detect_faces

class clipper_test(unittest.TestCase):
    """
    The clipper is involved with 4 phases:
    (1)Video Input (2) Cropping (3) Clustering (4) Clipping
    The test cases covers the whole process
    """
    def test_case_cluser(self):
        """
        Covers (3)
        :return:
        """
        # img_folder = './cropped'
        # if not os.path.exists(img_folder):
        #     raise FileNotFoundError('Image directory not found')
        # img_names = list(glob.glob(img_folder + '/'+'*.jpg'))
        # img_names = natsort.natsorted(img_names)
        #
        # with Image.open(img_names[0]) as img:
        #     print("Image count:", len(img_names), '\nImage size:', img.size)
        # print(img_names)
        cluster = FaceCluster()
        result = cluster.recognition("./cropped")
        print(result)
        # true_labels = [
        #     0, 1, 2, 3, 4, 0,
        #     0, 0, 0, 0, 0, 0,
        #     0, 0, 5, 0, 0, 6,
        #     7, 8, 9, 10, 2, 11,
        #     7, 12, 0, 0, 0, 13,
        #     0, 2, 0, 8, 2, 2,
        #     8, 1, 1, 14, 14, 0,
        #     15, 15, 8, 8, 8, 0,
        #     0, 16, 16, 0, 0, 0,
        #     1, 1, 1, 1, 0, 0,
        #     0, 0, 0, 17, 17, 0,
        #     0, 14, 0, 0, 17, 18,
        #     19, 0, 20, 2, 21, 22,
        #     23, 24, 7, 8, 2, 13,
        #     13, 0, 0, 0, 0, 8,
        #     8
        # ]

    def test_case_clipper_process(self):
        """
        Cover (3) (4)
        :return:
        """
        # img_folder = './cropped'
        # if not os.path.exists(img_folder):
        #     raise FileNotFoundError('Image directory not found')
        # img_names = list(glob.glob(img_folder + '/' + '*.jpg'))
        # img_names = natsort.natsorted(img_names)
        #
        # with Image.open(img_names[0]) as img:
        #     print("Image count:", len(img_names), '\nImage size:', img.size)

        cluster = FaceCluster()
        cluster_result = cluster.recognition("./cropped")
        logging.info(f"Finished clusering with {len(cluster_result['id'].unique())}")

        output_dir = './test_output'
        video_path = './video/input.mp4'
        time_info = frame_duration(cluster_result)
        extract_clip(video_path, time_info, output_dir)


    def test_case_clip_cluster_output(self):
        """
        Test (2) (3) (4)
        :return:
        """
        video_path = './video/input.mp4'
        input_file = video_path

        img_output_folder = "imgs"
        cropped_output_folder = "./test_temp"
        # extract frames from the video
        extract_frames(input_file, img_output_folder)

        # detect faces in frames and export cropped faces
        detect_faces(img_output_folder, cropped_output_folder)

        cluster = FaceCluster()
        cluster_result = cluster.recognition(cropped_output_folder)
        logging.info(f"Finished clusering with {len(cluster_result['id'].unique())}")

        output_dir = './test_output'
        time_info = frame_duration(cluster_result)
        extract_clip(video_path, time_info, output_dir)

        # Delete cropped
        # shutil.rmtree(cropped_output_folder)
        # shutil.rmtree(img_output_folder)

    def test_case_clipper(self):
        cliper = Clipper()
        input_path = './video/input.mp4'
        output_dir = './test_output'
        cliper.clip(input_path, output_dir)