import os
import sys
import time
import streamlit as st
from st_pages import add_page_title
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from modules import helper, settings, detect_img, detect_video,detect_by_webcam


add_page_title()

st.sidebar.header("Smart Checkout")

confidence = float(st.sidebar.slider("Select Model Confidence", 25, 100, 40)) / 100

st.sidebar.header("Detect Source")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST)

if source_radio == settings.IMAGE:
    st.header(f"With {source_radio}")
    detect_img.detect_img(confidence)


elif source_radio == settings.VIDEO:
    st.header(f"With {source_radio}")
    detect_video.detect_video(confidence)

elif source_radio == settings.WEBCAM:
    st.header(f"With {source_radio}")
    
    detect_by_webcam.web_rtc(confidence)
    # helper.play_webcam(confidence, model)
    # from streamlit_webrtc import webrtc_streamer
    # import av


    # flip = st.checkbox("Flip")


    # def video_frame_callback(frame):
    #     img = frame.to_ndarray(format="bgr24")

    #     flipped = img[::-1,:,:] if flip else img
        
    #     helper.play_webcam(confidence, model)

    #     return av.VideoFrame.from_ndarray(flipped, format="bgr24")
        


    # webrtc_streamer(
    #     key="example",
    #     video_frame_callback=video_frame_callback,
    #     # video_transformer_factory=YOLOv8VideoTransformer,
    #     # rtc_configuration=RTC_CONFIGURATION,
    #     media_stream_constraints={
    #         "video": True,
    #         "audio": False
    #     },
    # )

else:
    st.error("Please select a valid source type!")

