import streamlit as st
import requests

st.set_page_config(page_title="RAG Chatbot", page_icon="💬")

st.header('🤖 Loan Finance Asistant Chatbot')

def generate(query:str) -> str :
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
    return st.session_state.output


def processing() : 
    if "messages" not in st.session_state : 
        st.session_state.messages = []

    for message in st.session_state.messages : 
        with st.chat_message(message['role']) : 
            st.markdown(message['content'])

    if query := st.chat_input('Ask something about finance loan') : 
        #inputan user
        st.chat_message('user').markdown(query)
        #inputan user akan disimpan kedalam state
        st.session_state.messages.append({
            'role' : 'user', 
            'content' : query
        })

        response = generate(query) #generate response dari query
        with st.chat_message("assistant"):
            st.markdown(response) # menampilkan response ui

        st.session_state.messages.append({"role": "assistant", "content": response}) #menyimpan respon llm ke state

if __name__ == '__main__' : 
    processing() 


