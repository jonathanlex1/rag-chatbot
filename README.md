# 🧠 RAG Chatbot with LLaMA (Groq API), FastAPI, Langchain, and Streamlit

A Retrieval-Augmented Generation (RAG) chatbot that integrates Meta’s LLaMA model via Groq API, allowing fast and intelligent responses based on chat history and custom document retrieval.

## 🚀 Features

- 🔗 **LLM via Groq**  
  Uses `meta-llama/llama-4-scout-17b-16e-instruct` served through the Groq API for high-speed inference.

- 💬 **Chat History Aware**  
  Implements `RunnableWithMessageHistory` to support multi-turn, contextual conversations.

- 📄 **Custom Knowledge Base**  
  Retrieves context from local documents using **ChromaDB** and **HuggingFace Embeddings (MiniLM-L6-v2)**.

- ⚙️ **FastAPI Backend**  
  Serves RAG pipeline as a RESTful API with session-based conversation handling.

- 🖥️ **Streamlit Frontend**  
  Simple UI to interact with the chatbot by sending prompts via HTTP request.

- 📊 **LangSmith Tracking**  
  Monitors LLM behavior and debugging trace using LangSmith integration.

---

## 📦 Tech Stack

| Component        | Tech                        |
|------------------|-----------------------------|
| LLM              | Meta LLaMA via Groq API     |
| Retriever        | ChromaDB + MiniLM Embedding |
| API              | FastAPI                     |
| Frontend         | Streamlit                   |
| Monitoring       | LangSmith                   |

---

## 🛠️ How to Run

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/rag-chatbot.git
cd rag-chatbot

```
### 2 Install Dependecies
```bash
pip install -r requirements.txt

```
### 3 Set Up Environment Variables
```bash
GROQ_API_KEY=your_groq_api_key
```

### 4 Run FastAPI Server

```bash
py main.py
```

### 5 Run Streamlit 
```bash
streamlit run client.py

```