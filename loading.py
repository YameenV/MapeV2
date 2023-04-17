from turtle import width
import streamlit as st
from helper import defaultConfig
import requests
from streamlit_lottie import st_lottie
# from main import main_page

defaultConfig(1)


# for loader 
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def loadingPage():
    lottie_url_loader = "https://assets4.lottiefiles.com/private_files/lf30_al2qt2jz.json"
    lottie_loader = load_lottieurl(lottie_url_loader)

    col1, col2 = st.columns(2)

    with col1:
        st_lottie(lottie_loader,
            speed=0.8,
            height=300,
            width=450,
            key="loader")

    with col2:
        st.header("Processing...")
        st.text("Data Processing")
        st.text("Text Detection")
        st.text("Text Extraction")
        st.text("Entity Detection")

    # st.session_state.runpage = main_page
    # st.experimental_rerun()


if __name__ == "__main__":
    loadingPage()