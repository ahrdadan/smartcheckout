import streamlit as st
import pandas as pd
from modules import settings 
from st_pages import add_page_title

add_page_title()

st.markdown("## List daftar harga")
st.markdown("Ubah harga dengan klik pada bagian `price`")

st.markdown("""
    <style>
   .image-cell img {
        max-width: 200px;
        max-height: 200px;
    }
    </style>
""", unsafe_allow_html=True)

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(data=pd.read_csv(settings.FILE_DATASET))

edited_df = st.data_editor(st.session_state.df,
                           use_container_width=True, 
                           column_config={
                               "img": st.column_config.ImageColumn(
                                   "Preview Image", 
                                   help="Streamlit app preview screenshots",
                                   width="small"
                                   ),
                                "price": st.column_config.NumberColumn(
                                    "Price (in IDR)",
                                    help="The price of the product in IDR",
                                    format="Rp%d",
                                    width="small"
                                    ),
                                "id_name": st.column_config.Column(
                                    "Name",
                                    help="Name Products",
                                    width="medium",
                                    required=True,
                                    ),
                                "currency": st.column_config.Column(
                                    "Currency",
                                    help="Name of Currency",
                                    width="small"
                                    )
                                    
                                },
                                
                            hide_index=True
                           )

edited_df.to_csv(settings.FILE_DATASET, index=False)