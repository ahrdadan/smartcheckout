import threading

import cv2
import streamlit as st
from matplotlib import pyplot as plt

import numpy as np
import supervision as sv
import av

import queue
from modules import helper,settings,dataframe

from streamlit_webrtc import webrtc_streamer,VideoTransformerBase



model = helper.load_model(settings.MODEL_PATH)




class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.tracker = sv.ByteTrack()
        self.smoother = sv.DetectionsSmoother()
        self.bounding_box_annotator = sv.BoundingBoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()

        self.datas = 'Total Harga'
        self.t_price=0
        self.text_anchor = sv.Point(x=50, y=50)
        

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        height, width, layers = img.shape
        text_scale = sv.calculate_optimal_text_scale((width,height))
        

        start_point = sv.Point(0, height*(3/4))
        end_point = sv.Point(width, height*(3/4))

        line_zone = sv.LineZone(start=start_point, end=end_point)

        line_annotator = sv.LineZoneAnnotator(color=sv.Color.GREEN,
                                            text_scale=text_scale,
                                            custom_in_text="OUT",
                                            custom_out_text="IN")
        
        result = model(img)
        

        detections = sv.Detections.from_ultralytics(result)
        print("ok")
        detections = detections[detections.confidence > 0.4]
        

        # update detections with tracker id's
        detections = self.tracker.update_with_detections(detections)
        detections = selfsmoother.update_with_detections(detections)
        
        labels = [
            f"{class_id} {confidence:.2f}"
            for class_id, confidence
            in zip(dataframe.get_name_by_class(detections.class_id), detections.confidence)]
        
        b_annotated_frame = self.bounding_box_annotator.annotate(
            scene=frame.copy(),
            detections=detections)
        l_annotated_frame = label_annotator.annotate(
            scene=b_annotated_frame.copy(),
            detections=detections, labels=labels)
        
        crossed_in, crossed_out = line_zone.trigger(detections)
        if np.any(crossed_in) or np.any(crossed_out):
            detections_crossed_out = detections[crossed_out]
            for cls_id in detections_crossed_out.class_id:
                t_price=dataframe.total_Price(cls_id, t_price)
                datas = f'Rp {str(t_price)}'

        l_annotated_frame = sv.draw_text(scene=l_annotated_frame.copy(), text=datas, text_anchor=self.text_anchor, text_thickness=3, text_color=sv.Color.WHITE)

        annotated_frame = line_annotator.annotate(frame=l_annotated_frame.copy(), line_counter=line_zone)
        

        return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")
        
    


def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    
    height, width, layers = img.shape
    text_scale = sv.calculate_optimal_text_scale((width,height))
    

    start_point = sv.Point(0, height*(3/4))
    end_point = sv.Point(width, height*(3/4))

    line_zone = sv.LineZone(start=start_point, end=end_point)

    line_annotator = sv.LineZoneAnnotator(color=sv.Color.GREEN,
                                        text_scale=text_scale,
                                        custom_in_text="OUT",
                                        custom_out_text="IN")
    
    result = model(img)
    
    detections = sv.Detections.from_ultralytics(result)
    print("ok")
    detections = detections[detections.confidence > 0.4]
    

    # update detections with tracker id's
    detections = tracker.update_with_detections(detections)
    detections = smoother.update_with_detections(detections)
    
    labels = [
        f"{class_id} {confidence:.2f}"
        for class_id, confidence
        in zip(dataframe.get_name_by_class(detections.class_id), detections.confidence)]
    
    b_annotated_frame = bounding_box_annotator.annotate(
        scene=frame.copy(),
        detections=detections)
    l_annotated_frame = label_annotator.annotate(
        scene=b_annotated_frame.copy(),
        detections=detections, labels=labels)
    
    crossed_in, crossed_out = line_zone.trigger(detections)
    if np.any(crossed_in) or np.any(crossed_out):
        detections_crossed_out = detections[crossed_out]
        for cls_id in detections_crossed_out.class_id:
            t_price=dataframe.total_Price(cls_id, t_price)
            datas = f'Rp {str(t_price)}'

    l_annotated_frame = sv.draw_text(scene=l_annotated_frame.copy(), text=datas, text_anchor=text_anchor, text_thickness=3, text_color=sv.Color.WHITE)

    annotated_frame = line_annotator.annotate(frame=l_annotated_frame.copy(), line_counter=line_zone)


    return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")


def web_rtc():
    webrtc_streamer(key="Realtime_Detect_Product", 
                    # video_frame_callback=video_frame_callback,
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