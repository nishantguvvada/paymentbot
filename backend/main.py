import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from tool import purchase_price
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
import os

model = ChatMistralAI(model="mistral-small-latest", api_key=os.getenv('API_KEY'))
tools = [purchase_price]
model_with_tools = model.bind_tools(tools)
agent_executor = create_react_agent(model, tools)

app = FastAPI()

class UserQuery(BaseModel):
    query: str

@app.get("/")
def home():
    return { "Data": "Test" }

@app.post("/ask")
async def ask(user_input: UserQuery):
    # response = model_with_tools.invoke([HumanMessage(content=user_input.query)])
    response = agent_executor.invoke({"messages": [HumanMessage(content=user_input.query)]})

    # Read
    # https://github.com/langchain-ai/langchain/discussions/28686

    return { "Response": response["messages"] }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)