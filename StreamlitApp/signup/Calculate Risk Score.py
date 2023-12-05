import streamlit as st
import math
import pandas as pd
import csv



#---------------------------------------FUNCTIONS------------------------------------------------------------------------------


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


def calculate_bmi(weight, height):
    return weight / (height ** 2)


def calculator():
    # Define the constants and variables
    alpha = -6.322
    beta1 = -0.879  # Gender
    beta2 = 1.222   # Prescribed antihypertensive medication
    beta3 = 2.191   # Prescribed steroids
    beta4 = 0.063   # Age in years

    x1 = 0 if gender == "Male" else 1
    x2 = 1 if meds else 0
    x3 = 1 if steroids else 0

    if bmi <25:
        beta_x5 = 0
    elif 25 <= bmi < 27.5:
        beta_x5 = 0.699
    elif 27.5 <= bmi < 30:
        beta_x5 = 1.97
    elif bmi >= 30:
        beta_x5 = 2.518

    if family_history == "No diabetic 1st-Degree relative":
        beta_x6 = 0
    elif family_history == "Parent or sibling with diabetes":
        beta_x6 = 0.728
    else:
        beta_x6 = 0.753

    if smoking_history == "Non-smoker":
        beta_x7 = 0
    elif smoking_history == "Ex-smoker":
        beta_x7 = -0.218
    else:
        beta_x7 = 0.855

    exponent = alpha + (beta1 * x1) + (beta2 * x2) + (beta3 * x3) + (beta4 * age) + beta_x5 + beta_x6 + beta_x7

    probability = 1 / (1 + math.exp(-exponent))

    return probability


#-----------------------------------------------------------------------------------------------------------------------------------------
st.set_page_config(layout="wide")


username = None

user_login = pd.read_excel('user_login.xlsx')
username = user_login.iloc[-1, 0]
print(username)


data = pd.read_csv(f'data\\{username}_profile_data.csv')
try:
    last_data = data.iloc[-1]
    print(last_data)
except IndexError:
    last_data = ['','','',0,'Male',60,1.7]


st.title("Diabetes Risk Score")
gender = st.radio('Pick your gender',['Male','Female'], horizontal=True)
meds = st.checkbox('Prescribed anti-hypertensive medication')
steroids = st.checkbox('Prescribed steroid')
age = st.number_input('Age', min_value=0, step=1, value=last_data[3])

family_history = st.selectbox('Family History', ['No diabetic 1st-Degree relative', 'Parent or sibling with diabetes', 'Parent and sibling with diabetes'])
col3, col4 = st.columns(2)
with col3:
    weight = st.number_input("Enter weight", min_value=1.0, value=last_data[5])
    height = st.number_input("Enter height", min_value=1.0, value=last_data[6])

with col4:
    weight_unit = st.selectbox("Unit", ['kg', 'lbs'])
    height_unit = st.selectbox("Unit", ['meter', 'feet', 'inch', 'cm'])

weight, height = convert_to_kg(weight, weight_unit, height, height_unit)
bmi = calculate_bmi(weight, height)

st.text(f"BMI Score: {bmi:.2f}")
smoking_history = st.selectbox('Smoking History', ['Non-smoker', 'Ex-smoker', 'Current smoker'])
st.session_state.clicked = st.button('Check Score')

if "clicked" not in st.session_state:
    st.session_state.clicked=False

if st.session_state.clicked:

    result = calculator()
    score = result * 100
    st.success(f"Probability of having Type-2 Diabetes : {score:.2f}%")
    st.info("If your score is over 11%, there's an 85% chance it can accurately detect diabetes in people with high Hemoglobin (HgbA1c) levels (≥7.0%).")
    data_to_add = [gender, meds, steroids, age, family_history, weight, height, bmi, smoking_history, score]
    with open(f'data\\{username}_data.csv', mode='a', newline='') as file:
        print(data_to_add)
        writer = csv.writer(file)
        # Write the data as a new row
        writer.writerow(data_to_add)

#-----------------------------------------------------------------------------------------------------------------------------------------



