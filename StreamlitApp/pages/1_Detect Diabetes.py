import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os
import plotly.express as px
import subprocess
import csv
from datetime import date


username = None

user_login = pd.read_excel('user_login.xlsx')
username = user_login.iloc[-1, 0]
print(username)

data = pd.read_csv(f'data\\{username}_profile_data.csv')
try:
    last_data = data.iloc[-1]
    print(last_data)
except IndexError:
    last_data = ['','','',0,'Male',60,180]


# Load the pre-trained model
model = pickle.load(open('diabPredict.pkl', 'rb'))


def convert_binary(value):
    return 1 if value.lower() == 'yes' else 0

def calculate_bmi(weight, height):
    return weight / (height ** 2)

# Function to predict diabetes
def predict_diabetes(age, hypertension, heart_disease, bmi, HbA1c_level, blood_glucose_level):
    input_data = np.array([age, hypertension, heart_disease, bmi, HbA1c_level, blood_glucose_level]).reshape(1, -1)
    prediction = model.predict(input_data)
    return prediction[0]

# Streamlit app
def main():
    st.set_page_config(layout="wide")
    st.title("Diabetes Prediction")

    # User input
    age = st.slider("Age", min_value=1, max_value=150, value=last_data[3])
    hypertension_input = st.selectbox("Hypertension", ['No', 'Yes'])
    heart_disease_input = st.selectbox("Heart Disease", ['No', 'Yes'])
    bmi_value = calculate_bmi(last_data[5], last_data[6])
    print(bmi_value)
    bmi = st.slider("BMI", min_value=10.0, max_value=50.0, value=bmi_value)
    HbA1c_level = st.slider("Hemoglobin A1c (HbA1c) Level", min_value=4.0, max_value=10.0)
    blood_glucose_level = st.slider("Blood Glucose Level", min_value=50.0, max_value=300.0)

    hypertension = convert_binary(hypertension_input)
    heart_disease = convert_binary(heart_disease_input)

    # Make prediction
    if st.button("Predict"):
        result = predict_diabetes(age, hypertension, heart_disease, bmi, HbA1c_level, blood_glucose_level)
        today =date.today()
        data_to_add = [today, hypertension, heart_disease, HbA1c_level, blood_glucose_level]
        with open(f'data\\{username}_input_data.csv', mode='a', newline='') as file:
            print(data_to_add)
            writer = csv.writer(file)
            # Write the data as a new row
            writer.writerow(data_to_add)
        if result==0:
            st.success("You are: Non-Diabetic")
        else:
            st.error('You are: Diabetic')
    if st.button("Don't Know Hemoglobin or Blood Glucose level? Try Diabete Risk Calculator"):
        subprocess.Popen(["streamlit", "run", "signup/Calculate Risk Score.py"])






    st.divider()
    # Load your data into a Pandas DataFrame
    data = pd.read_csv(f'data\\{username}_data.csv')
    data2 = pd.read_csv(f'data\\{username}_input_data.csv')

    # Set page title and add spacing
    st.title('Health Analysis')
    st.write("")

    # Create two columns for better layout
    col1, col2 = st.columns(2)

    # Visualize the distribution of weight over time
    fig_weight = px.line(data, y="weight", title="Weight Distribution Over Time")
    fig_weight.update_traces(line=dict(color='#1f77b4'))  # Set line color
    fig_weight.update_layout(xaxis_title='Index', yaxis_title='Weight (kg)')
    col1.plotly_chart(fig_weight)

    # Visualize the distribution of hemoglobin levels over time
    fig_hemo = px.line(data2, x='date', y="hemolvl", title="Hemoglobin Distribution Over Time")
    fig_hemo.update_traces(line=dict(color='#2ca02c'))  # Set line color
    fig_hemo.update_layout(xaxis_title='Date', yaxis_title='Hemoglobin Level')
    col1.plotly_chart(fig_hemo)

    # Visualize the distribution of BMI over time
    fig_bmi = px.line(data, y="bmi", title="BMI Distribution Over Time")
    fig_bmi.update_traces(line=dict(color='#1f77b4'))  # Set line color
    fig_bmi.update_layout(xaxis_title='Index', yaxis_title='BMI')
    col2.plotly_chart(fig_bmi)

    # Visualize the distribution of blood glucose levels over time
    fig_glu = px.line(data2, x='date', y="glulvl", title="Blood Glucose Distribution Over Time")
    fig_glu.update_traces(line=dict(color='#2ca02c'))  # Set line color
    fig_glu.update_layout(xaxis_title='Date', yaxis_title='Blood Glucose Level')
    col2.plotly_chart(fig_glu)




#------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()