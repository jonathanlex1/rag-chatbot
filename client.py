import streamlit as st
import requests

st.set_page_config(page_title="RAG Chatbot", page_icon="💬")

st.header('🤖 Loan Finance Asistant Chatbot')

query = st.chat_input('Ask something about finance loan')

if 'output' not in st.session_state : 
    st.session_state.output = ''

def generate(query:str) :
    if query : 
        with st.spinner('Thinking....') :
            response = requests.post('http://127.0.0.1:8000/generate',
                                    json={
                                        'prompt' : query,
                                        'session_id' : 'default'
                                    })
            if response.ok : 
                st.session_state.output = response.json()['response']
            else : 
                st.session_state.output = "⚠️ Error from API"
    st.write(st.session_state.output)

if __name__ == '__main__' : 
    generate(query)


