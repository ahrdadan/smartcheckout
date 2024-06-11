import streamlit as st
from st_pages import Page, show_pages, add_page_title
import streamlit.components.v1 as components

show_pages(
    [
        Page("streamlit_app.py", "Home", "🏠"),
        Page("pages/price_list.py", "Price List", "📊"),
        Page("pages/smartcheckout.py", "SmartCheckout", "🛒"),
    ]
)

with open("templates/index.html", "r") as file:
    html_content = file.read()

components.html(html_content, height=4000, scrolling=True)