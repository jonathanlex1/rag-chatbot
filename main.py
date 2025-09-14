from fastapi import FastAPI
from pydantic import BaseModel
import os
from rag import rag_with_config_history

app = FastAPI(
    title='LLM Server', 
    version=1.0,
    description='Simple api using langchain',
)

class RequestPrompt(BaseModel) : 
    prompt:str 
    session_id:str = 'default'

class ResponseModel(BaseModel) : 
    response : str

@app.post('/generate', response_model=ResponseModel) 
async def generate(request : RequestPrompt) : 
    config = {
     'configurable' : {
         'session_id' : request.session_id
        }
    }
    
    response = rag_with_config_history.invoke({'input' : request.prompt}, config=config)

    return ResponseModel(response=response['answer'])

if __name__ == '__main__' : 
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
