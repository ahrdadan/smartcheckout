from PIL import Image
import streamlit as st
import dataframe
from modules import helper, settings
import numpy as np
import supervision as sv
from tqdm.notebook import tqdm
import pandas as pd
import cv2
import io
import tempfile
import numpy as np
import supervision as sv
from ultralytics import YOLO
from tqdm.notebook import tqdm
import pandas as pd
import os
import json
import uuid
import ffmpeg
from datetime import datetime
# import time
import uuid

file_json='output/output_list.json'

def disable_btn1(b):
        st.session_state["btn1"] = b

def save_frames_as_video(frames, output_path, fps=30):
    height, width, layers = frames[0].shape
    size = (width, height)
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    for frame in frames:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame_rgb)
    out.release()

def detect_video(confidence):
    f = st.file_uploader("Upload file",type=["mp4"])
    if f:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(f.read())
        vf = cv2.VideoCapture(tfile.name)
        fps = int(vf.get(cv2.CAP_PROP_FPS))
        disable_btn1(False)

    if st.button('Detect Video', use_container_width=True, disabled=st.session_state.get("btn1", True)):
        temp_dir = tempfile.TemporaryDirectory()
        st.write(temp_dir.name)
        
        stframe = st.empty()
        frames = []
        while vf.isOpened():
            ret, frame = vf.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            stframe.image(frame)
            frames.append(frame)

        name_video = f"{uuid.uuid4()}.mp4"
        output_video = f"{uuid.uuid4()}.mp4"

        name_video_path = f'output/{name_video}'
        output_video_path = f'output/{output_video}'

        save_frames_as_video(frames, name_video_path, fps)
        create_data_to_output(name_video, datetime.now())
        
        encode_video(name_video_path,output_video_path)
        create_data_to_output(output_video, datetime.now())


        video_file = open(output_video_path, 'rb')
        video_bytes = video_file.read()
        stframe.video(video_bytes,format='video/mp4')

def encode_video(input_file, output_file):
    try:
        print(f"Encoding {input_file} to {output_file} with x264 codec...")
        (
            ffmpeg
            .input(input_file)
            .output(output_file, vcodec='libx264')
            .run(overwrite_output=True)
        )
        print(f"Successfully encoded {input_file} to {output_file} with x264 codec.")
    except ffmpeg.Error as e:
        stderr = e.stderr.decode() if e.stderr else "No stderr available"
        print(f"An error occurred: {stderr}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

# input_file = 'output_video.mp4'  # Path to your input file
# output_file = 'output_video1.mp4'  # Path to your output file

# encode_video(input_file, output_file)

# output_path = 'videos/linezone.mp4'

# video_file = open(output_file, 'rb')
# video_bytes = video_file.read()


# st.video(video_bytes, format="mp4")
# os.remove(output_file)


def create_data_to_output(name, time):
    
    with open(file_json, 'r') as datas:
        data = json.load(datas)
    info={"name":str(name), "create_time":str(time)}
    data["results"].append(info)
    
    with open(file_json, 'w') as output_file:
        json.dump(data, output_file, indent=4)
    print(f'Success {info}')
    

def delete_output_video():
    with open(file_json, 'r') as output_file:
        data = json.load(output_file)
    if data["results"]:
        print('ada datanya')
    
        for item in data["results"]:
            create_time = datetime.strptime(item["create_time"], "%Y-%m-%d %H:%M:%S.%f")
            time_now = datetime.now()
            time_difference = time_now - create_time
            difference_in_seconds = time_difference.total_seconds()

            if difference_in_seconds > 3:
                print(item["name"])
                print("Selisih waktu lebih dari 3 detik")
            else:
                print("Selisih waktu kurang dari atau sama dengan 3 detik")
            # json.dump(data, output_file, indent=4)
    else:
        print('tida')
    



# name = uuid.uuid4()
# time = datetime.now()
# create_data_to_output(name, time)

# delete_output_video()