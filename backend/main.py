import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from tool import purchase_price, initiate_payment
from langchain_mistralai import ChatMistralAI
# from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

class UserQuery(BaseModel):
    query: str

# model = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv('GROQ_KEY'))
model = ChatMistralAI(model="mistral-small-latest", api_key=os.getenv('MISTRAL_KEY'))
tools = [purchase_price, initiate_payment]
# model_with_tools = model.bind_tools(tools)
agent_executor = create_react_agent(model, tools)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return { "Data": "Test" }

@app.post("/ask")
async def ask(user_input: UserQuery):
    # response = model_with_tools.invoke([HumanMessage(content=user_input.query)])
    responses = agent_executor.invoke({"messages": [HumanMessage(content=user_input.query)]})
    # Read
    # https://github.com/langchain-ai/langchain/discussions/28686


    return { "response": responses["messages"][-2] }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)