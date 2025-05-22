from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever

from langchain_core.prompts import MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory


from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
os.environ['LANGSMITH_API_KEY'] = os.getenv('LANGSMITH_API_KEY')
os.environ['LANGSMITH_TRACING_V2'] = 'true'
os.environ['LANGSMITH_PROJECT'] = 'Loan RAG Chatbot'

embedding_model = HuggingFaceEmbeddings(model='all-MiniLM-L6-v2')
vector_db = Chroma(persist_directory='.chroma_index', embedding_function=embedding_model)
retriever = vector_db.as_retriever()

#LLM aware history
llm = ChatGroq(model='meta-llama/llama-4-scout-17b-16e-instruct', api_key=GROQ_API_KEY)

#contextualized prompt 
contextualized_prompt = """
You are a helpful assistant specialized in data analysis and answering questions about datasets.

Your job is to rephrase follow-up questions into fully standalone questions by using the previous chat history for context.

Only output the rephrased standalone question. Do not answer the question.
"""

contextualized_prompt = ChatPromptTemplate.from_messages([
    ('system', contextualized_prompt),
    (MessagesPlaceholder('chat_history')),
    ('human', '{input}')
])

#chain with retriever aware history
retriever_aware_history = create_history_aware_retriever(llm, retriever, contextualized_prompt)

# qa prompt context integration 
prompt = ChatPromptTemplate.from_messages([
    ('system', 'You are a financial analyst who helps users understand financial data and answer queries.'),
    (MessagesPlaceholder('chat_history')),
    ('human', 'Here is the data:\n{context}\n\nQuestion: {input}')
])

# context chain 
llm_context_chain = create_stuff_documents_chain(llm, prompt)

#chain the retriever aware history and llm context
rag_chain = create_retrieval_chain(retriever_aware_history, llm_context_chain)  

# history config
store = {}
def get_config_history(session_id) -> BaseChatMessageHistory : 
    if session_id not in store : 
        store[session_id] = ChatMessageHistory()
    return store[session_id]

rag_with_config_history = RunnableWithMessageHistory(rag_chain, get_config_history, input_messages_key='input', history_messages_key='chat_history', output_messages_key='answer')
