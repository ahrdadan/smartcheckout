import threading

import cv2
import streamlit as st
from matplotlib import pyplot as plt

import numpy as np
import supervision as sv
import av

import queue
from modules import helper,settings,dataframe

from streamlit_webrtc import webrtc_streamer,VideoTransformerBase,WebRtcMode
import time


import pandas as pd
FILE_DATASET = settings.FILE_DATASET

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.bounding_box_annotator = sv.BoundingBoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()

        self.text_anchor = sv.Point(x=50, y=50)
        self.model = helper.load_model(settings.MODEL_PATH)
        self.text_scale = sv.calculate_optimal_text_scale((460,640))
        
        self.confidence=0.4

    def reader_obj(self, image):
        df = pd.read_csv(FILE_DATASET)   
        result = self.model(image)[0]
        
        detections = sv.Detections.from_ultralytics(result)
        
        detections = detections[detections.confidence > self.confidence]
        
        labels = [
            f"{name} Rp{price:,.0f} {confidence:.2f}"
            for name, price, confidence
            in zip(detections.data['class_name'], df['price'][detections.class_id], detections.confidence)]

        b_annotated_frame = self.bounding_box_annotator.annotate(
            scene=image.copy(),
            detections=detections)
        print("ok")
        l_annotated_frame = self.label_annotator.annotate(
            scene=b_annotated_frame.copy(),
            detections=detections, labels=labels)
      
        print("ok3")
        
        return l_annotated_frame
    
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        image = frame.to_ndarray(format="bgr24")
        annotated_image = self.reader_obj(image)
        return av.VideoFrame.from_ndarray(annotated_image, format="bgr24")
    


def web_rtc(confidence):
    ctx = webrtc_streamer(key="Realtime_Detect_Product", 
                    mode=WebRtcMode.SENDRECV,
                    video_transformer_factory=VideoTransformer,
                    media_stream_constraints={"video":True,"audio":False},
                    async_processing=True
                    )
    
    # while ctx.state.playing:
    #     with lock:
    #         img = img_container["img"]
    #     if img is None:
    #         continue
    #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     ax.cla()
    #     ax.hist(gray.ravel(), 256, [0, 256])
    #     fig_place.pyplot(fig)