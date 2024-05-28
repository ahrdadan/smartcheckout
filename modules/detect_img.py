from PIL import Image
import streamlit as st
import dataframe
from modules import helper, settings

st.session_state.TOTAL_HARGA = 0

def disable_btn1(b):
        st.session_state["btn1"] = b
def disable_btn2(b):
        st.session_state["btn2"] = b

def detect_img(confidence):
    uploaded_files = st.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'),accept_multiple_files=True)
    if uploaded_files:
        disable_btn1(False)


    col1, col2 = st.columns(2)

    if st.button('Detect Object', use_container_width=True, disabled=st.session_state.get("btn1", True)):
        disable_btn2(False)
        disable_btn1(True)
        with st.spinner('Load Model...'):
            model = helper.load_model(settings.MODEL_PATH)

        with st.spinner('Detect Image...'):
            for uploaded_file in uploaded_files:
                image = Image.open(uploaded_file)                
                res = model.predict(image,conf=confidence,imgsz=320)
                res_plotted=res[0].plot()[:, :, ::-1]
                with col1:
                    st.image(image, caption=uploaded_file.name)
                    st.divider()

                with col2:
                    st.image(
                        res_plotted,
                        caption=f'Result {uploaded_file.name}',
                        use_column_width=True
                        )
                    with st.expander(f"Total Harga {uploaded_file.name}: "):
                        col1ex, col2ex = st.columns(2)

                        for result in res:
                            for box in result.boxes:
                                class_id = int(box.cls)
                                class_name = model.names[class_id]
                                st.session_state.TOTAL_HARGA=dataframe.total_Price(
                                    class_id,
                                    st.session_state.TOTAL_HARGA)
                                with col1ex:
                                    st.write(class_name)
                                with col2ex:
                                    st.write(dataframe.format_rupiah(dataframe.get_price(class_id)))
                        with col1ex:
                            st.divider()
                            st.write('Total')
                        with col2ex:
                            st.divider()
                            st.write(dataframe.format_rupiah(st.session_state.TOTAL_HARGA))
                        st.session_state.TOTAL_HARGA = 0
       

    if st.button('Reset', use_container_width=True, disabled=st.session_state.get("btn2", True)):
        st.rerun()
