import logging
import torch
from PIL import Image
import os
import pandas as pd

from facenet_pytorch import MTCNN, InceptionResnetV1

from sklearn.cluster import estimate_bandwidth, MeanShift
from collections import defaultdict
import glob
from IPython.display import display
# Initialize face detector
mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20)

# Initialize the pre-trained face embedding model
resnet = InceptionResnetV1(pretrained='vggface2').eval()

def facenet_embedding(image):
    face, prob = mtcnn(image, return_prob=True)
    if prob is not None:
        return resnet(face.unsqueeze(0))
    else:
        return None

def meanshift(embeddings):
    bandwidth = estimate_bandwidth(embeddings, quantile=0.2, n_samples=500)
    # Create Mean Shift model with the estimated bandwidth
    ms = MeanShift(bandwidth=bandwidth)
    ms.fit(embeddings)

    # Retrieve the labels and cluster centers
    labels = ms.labels_
    # cluster_centers = ms.cluster_centers_
    return labels


class FaceCluster(object):
    """
        Recognize faces in images and cluster them.
    """
    def __init__(self, embedding=facenet_embedding, clustering=meanshift) -> None:
        self.embedding = embedding # embedding method
        self.clustering = clustering # clustering method
        self.embeddings = [] # list of embedding codes of images
        self.image_names = [] # list of names of images
        self.batch_mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20, keep_all=True)

    def recognition(self, input_path):
        """
            args: input_path - directory that contains all images
            return DataFrame {"id", "file_name"}
        """
        self.image_embedding(input_path)
        clusters = self.clustering(self.embeddings)
        return self.cluster_process(clusters)

    def image_embedding(self, directory_path):
        """
            Compute the embedding code of images
        """
        entries = os.listdir(directory_path)
        # print(entries)
        for entry in entries:
            image_path = os.path.join(directory_path, entry)
            image_file = Image.open(image_path)
            img_embedding = self.embedding(image_file)
            if img_embedding is not None:
                self.embeddings.append(img_embedding.detach().numpy().reshape([512, ]))
                self.image_names.append(entry)

    def cluster_process(self, clusters):
        df = pd.DataFrame({
            'id': clusters,
            'file_name': self.image_names
        })
        return df

    def single_frame_crop(self, img_path, save_path=None):
        faces = self.batch_mtcnn.forward(Image.open(img_path), save_path=save_path)
        return faces

    def batch_crop(self, input_dir, output_dir, keep_all=True):
        batch_mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20, keep_all=keep_all)
        img_path_list = list(glob.glob(input_dir + '/'+'*.jpg'))
        for img_path in img_path_list:
            # print(img_path.split('/'))
            img_name = img_path.split('/')[-1]
            # print(img_name)
            save_path = output_dir + '/' + img_name
            with Image.open(img_path)as img:
                res = batch_mtcnn.forward(img, save_path=save_path)
            if keep_all:
                logging.info(f'cropped {0 if res is None else res.shape[0]} from {img_name}')

# def cluster_print(df):
#     # Initialize a dictionary to hold the clusters
#     clustered_images = defaultdict(list)
#
#     # Group images by their cluster labels
#     for path, cluster_id in zip(df["file_name"], df["id"]):
#         clustered_images[cluster_id].append(path)
#
#     for cluster in clustered_images:
#         print(cluster)
#         for img_path in clustered_images[cluster]:
#             print(img_path, end=' ')  # Or load and display the image using an image library
#             image_file = Image.open(os.path.join("cropped", img_path))
#             # display(image_file)
#         print(' ')
#
# if __name__ == "__main__":
#     recog = FaceCluster()
#     df = recog.recognition("./cropped")
#     cluster_print(df)
