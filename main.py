import streamlit as st
from PIL import Image
from helper import defaultConfig
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import threading
import av
import cv2
from typing import Union
import numpy as np
import uuid
import os
import csv

#Config
defaultConfig()

# Header
img = Image.open("./media/UCoE-Web-Logo.png")
st.image(img)
st.title('Admission process')


class VideoTransformer(VideoTransformerBase):
    frame_lock: threading.Lock  

    out_image: Union[np.ndarray, None]

    def __init__(self) -> None:
        self.frame_lock = threading.Lock()
        self.out_image = None

    def transform(self, frame: av.VideoFrame) -> np.ndarray:
        out_image = frame.to_ndarray(format="bgr24")

        with self.frame_lock:
            self.out_image = out_image

        height, width, _ = out_image.shape
        x = int(width/4)
        y = int(height/4)
        w = int(width/2)
        h = int(height/2)
        
        out_image = cv2.rectangle(out_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return out_image

# Tabs

def main_page():
    tab1, tab2, tab3, tab4 = st.tabs(["Personal", "Marks", "Admission", 'Scanner'])

    with tab1:
        # -Aadhar
        # -leaving
        # -photo of student
        # -Student domicile certificate
        # - Student Medical certificate
        # -if defence certificate
        # -Gap certificate
        col1, col2 = st.columns(2)

        with col1:
            upload_photo = st.file_uploader("Photo of Student")
            upload_adhaar = st.file_uploader("Adhaar card")
            upload_lc = st.file_uploader("Leaving Certificate")
            migrant = st.checkbox("Click If you are Migrant Student")
            if migrant:
                upload_migrant = st.file_uploader("Migrant Certificate")
            gap = st.checkbox("Click if you have Gap Certificate")
            if gap:
                upload_gap = st.file_uploader("Gap certificate")
            defence = st.checkbox("click if you have Defence Certificate")
            if defence:
                upload_defence = st.file_uploader(" Defence Certificate")

        with col2:
            upload_domicile = st.file_uploader("Student domicile certificate")
            upload_medical = st.file_uploader("Student Medical certificate")
            upload_income = st.file_uploader("Income Certificate")
            upload_caste = st.file_uploader("Caste Certificate")

    with tab2:
        # 10/12/cet/jee
        upload_ten = st.file_uploader("10th Marksheet")
        upload_twelve = st.file_uploader("12th Marksheet")
        cet = st.checkbox("Click to take Addmission with CET")
        jee = st.checkbox("Click to take Addmission with JEE")
        if cet:
            upload_cet = st.file_uploader("CET Marksheet")
        if jee:
            upload_jee = st.file_uploader("JEE Marksheet")

    with tab3:
        # -Cap receipt( cum Acknowledgement letter)
        # -Addmission reporting/
        # seat acceptance letter
        upload_cap_recipt = st.file_uploader(
            "Cap receipt( cum Acknowledgement letter)")
        upload_report_letter = st.file_uploader(
            "Admission reporting/seat acceptance letter")



    with tab4:
        wrtc = webrtc_streamer(key="snapshot", video_transformer_factory=VideoTransformer)
    
        if wrtc.video_transformer:
            snap = st.button("Snapshot")

            if snap:
                with wrtc.video_transformer.frame_lock:
                    out_image = wrtc.video_transformer.out_image

                if out_image is not None:
                    height, width, _ = out_image.shape
                    x = int(width/4)
                    y = int(height/4)
                    w = int(width/2)
                    h = int(height/2)
                    
                    cropped_image = out_image[y+2:y+h-2, x+2:x+w-2]
                    rgbImage = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(rgbImage)

                    folder_path = './images'
                    for file_name in os.listdir(folder_path):
                        if file_name.endswith('.jpg'):
                            os.remove(os.path.join(folder_path, file_name))

                    csv_folder_path = './my_folder'
                    csv_file_name = 'data.csv'

                    file_path = os.path.join(csv_folder_path, csv_file_name)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"File {csv_file_name} deleted from folder {csv_folder_path}")

                    uid = uuid.uuid4().hex
                    filename = f'./images/{uid}.jpg'

                    image.save(filename)

                    aadhar_number = '1234 5678 9012'
                    name = 'John Doe'
                    date_of_birth = '01/01/1990'
                    address = '123 Main St, Anytown, USA'

                    data = [filename, aadhar_number, name, date_of_birth, address]

                    with open('./userdata/data.csv', mode='w') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow(data)
                        print('Data written to CSV file')

                    st.image(filename)

            
                        
                else:
                    st.warning("No frames available yet.")
    # with col2:
    submitButton = st.button("Submit")

    if submitButton:
        st.success("click on the form to see your form fill")

main_page()


# def form():
#     st.markdown("")

# page_names_to_funcs = {
#     "Page 2": form,
# }