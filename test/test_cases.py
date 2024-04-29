import logging
import os
import glob
from PIL import Image
import unittest
# import natsort

from clustering.faceCluster import FaceCluster
from pre_post_processing.vidClips import frame_duration, extract_clip


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