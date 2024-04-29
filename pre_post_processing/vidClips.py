from moviepy.editor import VideoFileClip
import pandas as pd
import os
from vidToImg import folder_creation

"""
extract frame number and calculate frame durations from file names
input:
    dataframe with columns: id, file_name
output:
    a new dataframe with id, frame_number, and duration
"""
def frame_duration(meta_data):

    meta_data['frame_number'] = meta_data['file_name'].apply(lambda x: int(x.split('_')[1]))
    meta_data['duration'] = 0
    meta_data = meta_data.sort_values(by='id').sort_values(by='names')
    
    for id, group in meta_data.groupby('id'):
        for idx, row in group.iterrows():
            if idx==0:
                if row['frame_number']+1 != meta_data.at[idx + 1, 'frame_number']:
                    print('test')
                    meta_data.at[idx, 'duration'] = 1
                else:
                    meta_data.at[idx, 'duration'] = 0
                    meta_data.at[idx+1, 'duration'] = 1
            else:
                if row['frame_number'] == meta_data.at[idx - 1, 'frame_number'] +1:
                    meta_data.at[idx, 'duration'] = 1+meta_data.at[idx- 1, 'duration']
                    meta_data.at[idx- 1, 'duration'] = 0
                else:
                    meta_data.at[idx, 'duration'] = 1

    meta_data = meta_data[meta_data["duration"]!=0].drop(columns=['names'])
    return meta_data


"""
export video clips with given time_info dataframe
input:
    input_file: video file path
    time_info: dataframe contains id, frame_number, and duration
    vid_output_folder: name a new output folder name for video clips
"""
def extract_clip(input_file, time_info, vid_output_folder):
    
    folder_creation(vid_output_folder)

    video = VideoFileClip(input_file)

    for idx, row in time_info.iterrows():
        id = row['id']
        start = row['frame_number']
        duration = row['duration']
        end = start+duration-0.5

        output_path = os.path.join(vid_output_folder, f"{id}_{duration}.mp4")

        clip = video.subclip(start, end)
        clip.write_videofile(output_path, codec="libx264")


if __name__ == "__main__":
    input_file = "input.mp4"
    meta_data = pd.DataFrame({'id':['0','0','0','0','0','1','2'], 
                              'file_name':["vid-img/cropped/frame_21_20979.jpg",
                                       "vid-img/cropped/frame_23_22981.jpg",
                                       "vid-img/cropped/frame_25_24983.jpg",
                                       "vid-img/cropped/frame_26_25984.jpg",
                                       "vid-img/cropped/frame_27_26985.jpg",

                                       "vid-img/cropped/frame_44_44002.jpg",

                                       "vid-img/cropped/frame_95_95011.jpg",
                                       ]})
    vid_output_folder = "vids"

    time_info = frame_duration(meta_data)
    extract_clip(input_file, time_info, vid_output_folder)
