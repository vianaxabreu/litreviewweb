import streamlit as st
import requests
#import pandas as pd
#import random
import time
#from google.cloud import bigquery
from litreview.params import PROJECT_ID, LOCATION, check_table_name

#################
## hard codes ##
#################
API_URL = 'https://newliteraturereview-z37yi6v7za-ew.a.run.app/predict'
API_LOCAL = 'http://127.0.0.1:8000/predict'
#FILENAME = 'https://storage.googleapis.com/wagon-data-735-vianadeabreu/data/arxiv-metadata_final.csv'
FILENAME = 'https://storage.googleapis.com/wagon-data-735-vianadeabreu/data/trimmed_arxiv_docs.csv'

st.set_page_config(
    page_title="Automated Literature Review",  # => Quick reference - Streamlit
    page_icon="📚",
    layout="wide",  # wide
    initial_sidebar_state="auto")  # collapsed

#######################
## setup for sidebar ##
#######################
sideb = st.sidebar
sideb.image("images/logo.png", use_column_width=True)
sideb.markdown(
    "<h1 style='text-align: center; color: #5D6D7E;'>Demo Day - Batch 735 - Berlin</h1>",
    unsafe_allow_html=True)
sideb.write(
    "<h1 style='text-align: center; color: #5D6D7E; font-size: 13px;'>Claire Filtz, Felix Wohlleben</h1>",
    unsafe_allow_html=True)
sideb.write(
    "<h1 style='text-align: center; color: #5D6D7E; font-size: 13px;'>Issa Al Barwani, Alex Viana</h1>",
    unsafe_allow_html=True)
sideb.markdown(
    "<h1 style='text-align: center; color: #5D6D7E; font-size: 13px;'>With the 🥋💪🏏💥 of Ben Auzanneau</h1>",
    unsafe_allow_html=True)
# unused emojis:  🚀🎾

#######################
## setup for main #####
#######################
st.markdown(
    "<h1 style='text-align: center; color: #5D6D7E;'>An Automated Literature Review Tool</h1>",
    unsafe_allow_html=True)
st.markdown(
    "<h5 style='text-align: center; color: #5D6D7E;'>You give us one paper, we give you many. </h5>",
    unsafe_allow_html=True)
##########################
## setup for search bar ##
##########################

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',
                unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>',
                unsafe_allow_html=True)


local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

icon("search")
input_abstract = st.text_input("", placeholder="Please paste the abstract of your paper here")
input_title = st.text_input("", placeholder="OPTIONAL: What is the title of your paper?")
input_author = st.text_input("", placeholder="OPTIONAL: Who are the authors of your paper?")

input_user = input_abstract + " " + input_title + " " + input_author

#st.markdown("", placeholder="OPTIONAL: Who are the authors of your paper?")
neighbors = st.number_input(
    label='How many papers are you looking for?',
    min_value=2,
    max_value=30,
    value=5
)
button_clicked = st.button("OK")

name_url = API_URL + '?user_input=' + input_user + '&neighbors=' + str(
    neighbors)
if button_clicked:
    #begin = time.time()
    response = requests.get(name_url)
    prediction = response.json()
    st.write(
        f"<h1 style='text-align: left; color: #5D6D7E; font-size: 18px;'>Here are {neighbors} nice papers to read:</h1>",
        unsafe_allow_html=True)
    for i in range(neighbors):
        st.write(
            f"<h1 style='text-align: left; color: #ABB2B9; font-size: 19px;'>{prediction[str(i)][0]}</h1>",
            unsafe_allow_html=True)
        st.write(
            f"<h5 style='text-align: left; color: #566573; font-size: 15px;'>by {prediction[str(i)][3]}</h5>",
            unsafe_allow_html=True)
        st.write(
            f"<h1 style='text-align: left; color: #ABB2B9; font-size: 17px; font-style: italic;'>{prediction[str(i)][1]}</h1>",
            unsafe_allow_html=True)
        link = f"https://arxiv.org/pdf/{prediction[str(i)][2]}.pdf"
        st.write(f"[get PDF]({link})")
