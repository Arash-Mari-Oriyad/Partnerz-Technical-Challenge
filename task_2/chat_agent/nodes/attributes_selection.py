from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI


from ..config import State
from ..utils import (
    generate_response,
    format_messages_for_prompt,
    format_dict_for_prompt,
)
from ..prompts import ATTRIBUTE_SELECTION_PROMPT_TEMPLATE


llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)


def attributes_selection_node(state: State) -> State:
    chat_history = format_messages_for_prompt(messages=state["messages"])
    attributes_selection_prompt = ATTRIBUTE_SELECTION_PROMPT_TEMPLATE.format(
        chat_history=chat_history,
        product_type=state["product_type"],
        attributes_text=format_dict_for_prompt(state["attributes"]),
    )
    response = generate_response(llm=llm, prompt=attributes_selection_prompt)
    state["messages"].append(AIMessage(response.content))
    return state
