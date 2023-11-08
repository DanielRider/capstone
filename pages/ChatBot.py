import streamlit as st
import openai
import pandas as pd
#from Capstone import key_config




def chat_with_bot(message_history):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
    )
    return response.choices[0].message['content']
#---------------------------------------------------------------------------------------------


openai.api_key = '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'# key_config.openai_key

username = None
user_login = pd.read_excel('user_login.xlsx')
username = user_login.iloc[-1, 0]
print(username)


null_flag=False
data = pd.read_csv(f'data\\{username}_data.csv')


try:
    last_data = data.iloc[-1]
except IndexError:
    null_flag=True
print(last_data)


st.title("Chatbot with Streamlit and OpenAI")
if "message_history" not in st.session_state:
    st.session_state.message_history = [{"role": "system", "content": "YOU ARE STRICTLY A DIABETES MANAGMENT ASSISTANT WHO WILL HELP AND GUIDE USERS QUERIES."}]


if st.button("Get recommandation"):
    gender = last_data['gender']
    meds = last_data['meds']
    steroids = last_data['steroids']
    age = last_data['age']
    family_history = last_data['family_History']
    weight = last_data['weight']
    height = last_data['height']
    bmi = last_data['bmi']
    smoking_history = last_data['smoker']



    info = f'''Based on users information, Recommand Excerices and Diet to user to prevent diabetes.
    Gender: {gender},
    take prescribed anti-hypertensive medication?: {meds},
    take prescribed steroids?: {steroids},
    Age: {age},
    Family history: {family_history},
    Weight: {weight} meters,
    height: {height} Kg,
    BMI(Body Mass Index): {bmi},
    Smoking History: {smoking_history}'''


    user_info_message = [{"role": "user", "content": info}]
    #st.session_state.message_history.append(user_info_message)

    response = chat_with_bot(user_info_message)
    st.session_state.message_history.append({"role": "assistant", "content": response})

#else:
#    with st.chat_message('assistant'):
#        st.markdown("How can I help you?")

for message in st.session_state.message_history[1:]:
   with st.chat_message(message["role"]):
       st.markdown(message["content"])

prompt = st.chat_input("Ask a Question...")
if prompt:
    with st.chat_message('user'):
        st.markdown(prompt)

    st.session_state.message_history.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        print(st.session_state.message_history)
        response = chat_with_bot(st.session_state.message_history)
        print(response)
        st.markdown(response)

    st.session_state.message_history.append({"role": "assistant", "content": response})
