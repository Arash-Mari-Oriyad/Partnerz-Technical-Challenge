import os
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from langchain_core.messages import HumanMessage, AIMessage
import environ

BASE_DIR = Path(__file__).resolve().parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

from chat_agent.builder import build_graph


app = FastAPI()
graph = build_graph()


class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    state: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    ai_message: str
    state: Dict[str, Any]
    is_finished: bool


def convert_messages(msgs):
    res = []
    for m in msgs:
        if m["role"] == "human":
            res.append(HumanMessage(m["content"]))
        elif m["role"] == "ai":
            res.append(AIMessage(m["content"]))
        else:
            raise ValueError(f"Unknown message role: {m['role']}")
    return res


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    state = request.state or {
        "messages": [],
        "next_node": "",
        "product_type": "",
        "attributes": {},
        "product_name": "",
        "is_finished": False,
    }
    state["messages"] = convert_messages(request.messages)
    result_state = graph.invoke(state)
    ai_msg = ""
    if result_state["messages"]:
        ai_msg = result_state["messages"][-1].content
    return ChatResponse(
        ai_message=ai_msg,
        state=result_state,
        is_finished=result_state.get("is_finished", False),
    )
