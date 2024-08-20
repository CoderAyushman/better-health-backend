
from dotenv import load_dotenv
import getpass
import os
from fastapi import FastAPI, HTTPException
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# Load environment variables from .env file
load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")
    
    
def chat(txt:str):
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    result = llm.invoke(txt)
    # print(result.content) 
    # return result.content 
    return result.content

# testing
# print(chat("write about narendra modi"))


@app.get("/")
def hello():
    return "hello world"


class RequestModel(BaseModel):
    prompt: str

@app.post("/api/langchain/gemini")
async def generate_response(request: RequestModel):
    try:
        prompt = request.prompt
        response = chat(prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)