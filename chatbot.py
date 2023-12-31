import streamlit as st
from streamlit_chat import message
from utils import get_initial_message, get_chatgpt_response, update_chat
import os
from dotenv import load_dotenv
load_dotenv()
import openai

# When you are working locally set your api keys with this:
# openai.api_key = os.getenv('OPENAI_API_KEY')
# pinecone_api_key = os.getenv('PINECONE_API_KEY')

# When you are uploading to Streamlit, set your keys like this:
# pinecone_api_key = st.secrets["API_KEYS"]["pinecone"]
openai.api_key = st.secrets["API_KEYS"]["openai"]

st.title("Chatbot : ChatGPT General Bot To Ask General Questions")
st.subheader("AI General Chatbot:")

model = st.selectbox(
    "Select a model",
    ("gpt-3.5-turbo", "gpt-4")
)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_area("Query: ", key="input")  # Changed st.text_input to st.text_area

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()
 
if query:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        # st.write("Before  making the API call")
        # st.write(messages)
        response = get_chatgpt_response(messages,model)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)
        
if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

    with st.expander("Show Messages"):
        st.write(messages)
