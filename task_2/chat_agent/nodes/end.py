from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI

from ..config import State
from ..prompts import FINISH_CHAT_PROMPT_TEMPLATE
from ..utils import (
    format_messages_for_prompt,
    format_dict_for_prompt,
    generate_response,
)


llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)


def end_node(state: State) -> State:
    print(state["product_name"])
    if state["is_finished"] == True:
        chat_history = format_messages_for_prompt(messages=state["messages"])
        finishing_chat_prompt = FINISH_CHAT_PROMPT_TEMPLATE.format(
            chat_history=chat_history,
            product_type=state["product_type"],
            attributes_text=format_dict_for_prompt(state["attributes"]),
            product_name=state["product_name"],
        )
        response = generate_response(llm=llm, prompt=finishing_chat_prompt)
        state["messages"].append(AIMessage(response.content))
    return state
