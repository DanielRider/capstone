import streamlit as st
import os
from datetime import date
import pandas as pd
import csv

username = None

user_login = pd.read_excel('user_login.xlsx')
username = user_login.iloc[-1, 0]


null_flag=False
data = pd.read_csv(f'data\\{username}_profile_data.csv')


try:
    last_data = data.iloc[-1]
    print(last_data)
except IndexError:
    last_data = ['','','',0,'Male',60.0,1.7]

def convert_to_kg(weight, weight_unit, height, height_unit):
    if weight_unit == 'lbs':
        weight = weight * 0.453592  # Convert lbs to kg

    if height_unit == 'inch':
        height = height * 0.0254  # Convert inches to meters
    elif height_unit == 'feet':
        height = height * 0.3048  # Convert feet to meters
    elif height_unit == 'cm':
        height = height * 0.01

    return weight, height

# Title and description
st.title("User Profile Information")
st.write("Please fill out the following information:")

# Input fields for user profile information
first_name = st.text_input("First Name", value=last_data[1])
last_name = st.text_input("Last Name", value=last_data[2])
age = st.number_input("Age", min_value=0, max_value=150, value=last_data[3])
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
col3, col4 = st.columns(2)
with col3:
    weight = st.number_input("Enter weight", min_value=1.0, value=last_data[5])
    height = st.number_input("Enter height", min_value=1.0, value=last_data[6])

with col4:
    weight_unit = st.selectbox("Unit", ['kg', 'lbs'])
    height_unit = st.selectbox("Unit", ['meter', 'feet', 'inch', 'cm'])
weight, height = convert_to_kg(weight, weight_unit, height, height_unit)


# Save the user input
if st.button("Save Profile"):
    today = date.today()
    data_to_add = [today, first_name, last_name, age, gender, weight, height]
    # You can add code here to save the user's profile data to a database or file.
    with open(os.path.join("data", f"{username}_profile_data.csv"), mode='a', newline='') as file:
        print(data_to_add)
        writer = csv.writer(file)
        # Write the data as a new row
        writer.writerow(data_to_add)
    st.success("Profile saved successfully!")


# You can add additional functionality to save the user data to a database or perform other actions.
