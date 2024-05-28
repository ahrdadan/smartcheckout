import streamlit as st
from st_pages import Page, show_pages, add_page_title

add_page_title()


show_pages(
    [
        Page("streamlit_app.py", "Home", "🏠"),
        Page("pages/daftar_harga.py", "Daftar Harga", "📊"),
        Page("pages/predict.py", "SmartCheckout", "🛒"),
    ]
)
