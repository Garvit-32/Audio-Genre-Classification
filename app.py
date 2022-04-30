import streamlit as st
import pandas as pd
import numpy as np
from inference import predict
# from pydub import AudioSegment
import os
import pickle
from typing import Tuple


import base64


def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.

    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "png"

    # st.markdown(
    #      f"""
    #      <style>
    #      .stApp {{
    #          background: url('https://www.freepik.com/premium-photo/white-headphone-sweet-pastel-background_4373057.htm');
    #          background-size: cover
    #      }}
    #      </style>
    #      """,
    #      unsafe_allow_html=True
    #  )
    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


set_bg_hack('bg.png')


st.markdown(
    """<h1 style='text-align: left;margin-left :10px;color: black;font-size:80px;margin-top:-50px;'>AUDIO GENRE CLASSIFIER</h1><h1 style='text-align: left; color: white;font-size:30px;margin-top:-30px;'></h1>""",
    unsafe_allow_html=True)


file = st.sidebar.file_uploader("Upload Audio To Classify", type=["wav"])

rad_test = st.sidebar.radio(
    "Select format of audio file", options=['mp3', 'wav'])
if file is not None:
    st.markdown(
        """<h1 style='color:gray;'>Audio </h1>""",
        unsafe_allow_html=True)
    st.audio(file)
    if st.button("Classify Audio"):
        prediction = predict(file)
        st.markdown(
            f"""<h1 style='color:gray;'>Genre </h1>""",
            # f"""<h1 <span style='color:black;'>{prediction}</span></h1>""",
            unsafe_allow_html=True)
        st.markdown(
            f"""<h2><span style='color:black;'>{prediction}</span></h2>""",
            unsafe_allow_html=True)
