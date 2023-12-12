import streamlit as st
import pandas as pd
import subprocess
import os
import openpyxl
from openpyxl import Workbook

# Function to create a new user account
def signup(username, password):
    users_df = pd.read_csv("user_credentials.csv")

    # Check if the username already exists
    if username in users_df["Username"].values:
        st.error("Username already exists. Please choose a different username.")
    else:
        # Add the new user to the CSV file
        new_user = pd.DataFrame({"Username": [username], "Password": [password]})
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        users_df.to_csv("user_credentials.csv", index=False)
        data_folder = "data"
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        database_columns = ['gender', 'meds', 'steroids', 'age', 'family_History', 'weight', 'height', 'bmi', 'smoker', 'score']
        profile_columns = ['date', 'fname', 'lname', 'age', 'gender', 'weight', 'height']
        input_columns = ['date','hypertension','heart_diesease', 'hemolvl', 'glulvl']

        df = pd.DataFrame(columns=database_columns)
        df2 = pd.DataFrame(columns=profile_columns)
        df3 = pd.DataFrame(columns=input_columns)

        df.to_csv(os.path.join(data_folder, f"{username}_data.csv"), index=False)
        df2.to_csv(os.path.join(data_folder, f"{username}_profile_data.csv"), index=False)
        df3.to_csv(os.path.join(data_folder, f"{username}_input_data.csv"), index=False)

        st.success("Account created successfully. You can now log in.")




# Function to authenticate a user
def login(username, password):
    users_df = pd.read_csv("user_credentials.csv")

    if username in users_df["Username"].values:
        user_row = users_df.loc[users_df["Username"] == username]
        if user_row["Password"].values[0] == password:
            return True
    return False



# Initialize user_credentials.csv with header if it doesn't exist
try:
    pd.read_csv("user_credentials.csv")
except FileNotFoundError:
    initial_df = pd.DataFrame(columns=["Username", "Password"])
    initial_df.to_csv("user_credentials.csv", index=False)


#Keep tract of users login
# Check if the file exists, and if not, create a new workbook
try:
    workbook = openpyxl.load_workbook("user_login.xlsx")
except FileNotFoundError:
    # If the file does not exist, create a new workbook
    workbook = Workbook()
    sheet = workbook.active
    header = ["Username"]
    sheet.append(header)
    workbook.save("user_login.xlsx")

# Streamlit UI
st.title("AI-betes Advisor")
tabs = st.tabs(["Signup", "Login"])

# Define the content for the "Signup" tab
with tabs[0]:
    st.header("Sign up")
    new_username = st.text_input("Username", key="signup_username")
    new_password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        if new_username and new_password:
            signup(new_username, new_password)

# Define the content for the "Login" tab
with tabs[1]:
    st.header("Login")
    entered_username = st.text_input("Username", key="login_username")
    entered_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log In"):
        if entered_username and entered_password:
            if login(entered_username, entered_password):
                st.success("Logged in successfully.")

                # Select the active sheet (usually the first sheet)
                sheet = workbook.active
                # Data to add as a new row
                data_to_add = [entered_username]
                # Append the data as a new row in the sheet
                sheet.append(data_to_add)
                # Save the changes to the Excel file
                workbook.save("user_login.xlsx")
                # Close the workbook
                workbook.close()
                subprocess.Popen(["streamlit", "run", "Profile.py"])
            else:
                st.error("Invalid username or password. Please try again.")

