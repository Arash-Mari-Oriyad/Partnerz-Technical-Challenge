import os
from pathlib import Path

import environ
from langchain_core.messages import HumanMessage, AIMessage

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

from .builder import build_graph


graph = build_graph()


initial_message = "Hi. I am your shopping assistant."
messages = [AIMessage(initial_message)]


print(f"AI: {initial_message}")
print(50 * "-")


state = {
    "messages": messages,
    "next_node": "",
    "product_type": "",
    "attributes": {},
    "product_name": "",
    "is_finished": False,
}


while True:
    user_message = input("Human: ")
    print(50 * "-")

    state["messages"].append(HumanMessage(user_message))

    state = graph.invoke(state)

    print(f"{state["messages"][-1].content}")
    print(50 * "-")

    if state["is_finished"]:
        print("END CONVERSATION!")
        break
