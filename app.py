import imp
import streamlit as st
from predict_page import show_predict
from Explore import show_explore_page

page = st.sidebar.selectbox("Explore Or Predict", ("Predict", "Explore"))

if(page=="Predict"):
    show_predict()
else:
    show_explore_page()