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

df = pd.read_csv(FILE_DATASET)

info_datas={}



class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.tracker = sv.ByteTrack()
        self.smoother = sv.DetectionsSmoother()
        self.bounding_box_annotator = sv.BoundingBoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()

        self.text_anchor = sv.Point(x=50, y=50)
        self.model = helper.load_model(settings.MODEL_PATH)
        self.text_scale = sv.calculate_optimal_text_scale((460,640))
        

        # self.start_point = sv.Point(0, 640*(3/4))
        # self.end_point = sv.Point(460, 640*(3/4))

        # self.line_zone = sv.LineZone(start=self.start_point, end=self.end_point)

        # self.line_annotator = sv.LineZoneAnnotator(color=sv.Color.GREEN,
        #                                     text_scale=self.text_scale,
        #                                     custom_in_text="OUT",
        #                                     custom_out_text="IN")
        self.confidence=0.4

        # self.datas = 'Total Harga'
        # self.t_price=0
        

    def reader_obj(self, image):        
        result = self.model(image)[0]
        
        detections = sv.Detections.from_ultralytics(result)
        
        detections = detections[detections.confidence > self.confidence]
        
        
        # update detections with tracker id's
        detections = self.tracker.update_with_detections(detections)
        detections = self.smoother.update_with_detections(detections)
        
        labels = [
            f"{class_id} {confidence:.2f}"
            for class_id, confidence
            in zip(df['id_name'][detections.class_id], detections.confidence)]

        b_annotated_frame = self.bounding_box_annotator.annotate(
            scene=image.copy(),
            detections=detections)
        l_annotated_frame = self.label_annotator.annotate(
            scene=b_annotated_frame.copy(),
            detections=detections, labels=labels)
       
        # crossed_in, crossed_out = self.line_zone.trigger(detections)
        
        # if np.any(crossed_in) or np.any(crossed_out):
        #     detections_crossed_out = detections[crossed_out]
        #     for cls_id in detections_crossed_out.class_id:
        #         self.t_price=dataframe.total_Price(cls_id, self.t_price)
        #         self.datas = f'Rp {str(self.t_price)}'
        
        # l_annotated_frame = sv.draw_text(scene=l_annotated_frame.copy(), text=self.datas, text_anchor=self.text_anchor, text_thickness=2, text_color=sv.Color.BLACK)
        
        print("ok")
        # annotated_frame = self.line_annotator.annotate(frame=l_annotated_frame.copy(), line_counter=self.line_zone)
        print("ok3")
        
        return l_annotated_frame
    
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        image = frame.to_ndarray(format="bgr24")
        annotated_image = self.reader_obj(image)
        return av.VideoFrame.from_ndarray(annotated_image, format="bgr24")
    


def web_rtc():
    ctx = webrtc_streamer(key="Realtime_Detect_Product", 
                    # video_frame_callback=video_frame_callback,
                    mode=WebRtcMode.SENDRECV,
                    video_transformer_factory=VideoTransformer,
                    media_stream_constraints={"video":True,"audio":False},
                    async_processing=True
                    )
    

    # ctx = webrtc_streamer(key="example", video_frame_callback=video_frame_callback)
    
    # while ctx.state.playing:
    #     with lock:
    #         img = img_container["img"]
    #     if img is None:
    #         continue
    #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     ax.cla()
    #     ax.hist(gray.ravel(), 256, [0, 256])
    #     fig_place.pyplot(fig)