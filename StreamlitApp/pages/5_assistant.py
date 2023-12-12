import streamlit as st
import openai
import pandas as pd

tab1, tab2 = st.tabs(["Case1", "Case2"])

case1data = pd.read_csv("StreamlitApp/data/patient1.csv")
case2data = pd.read_csv("StreamlitApp/data/patient2.csv")


