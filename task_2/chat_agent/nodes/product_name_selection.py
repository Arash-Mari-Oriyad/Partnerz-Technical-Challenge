from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI


from ..config import State
from ..utils import (
    format_messages_for_prompt,
    format_dict_for_prompt,
    search_shop_catalog,
    generate_response,
    format_list_dict_for_prompt,
)
from ..prompts import PRODUCT_NAME_SELECTION_PROMPT_TEMPLATE


llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)


def product_name_selection_node(state: State) -> State:
    chat_history = format_messages_for_prompt(messages=state["messages"])

    product_type = state["product_type"]
    attributes_text = format_dict_for_prompt(state["attributes"])
    available_products = search_shop_catalog(
        product_type=product_type, description=attributes_text
    )
    available_products_text = format_list_dict_for_prompt(available_products)
    product_name_selection_prompt = PRODUCT_NAME_SELECTION_PROMPT_TEMPLATE.format(
        chat_history=chat_history,
        product_type=product_type,
        attributes_text=attributes_text,
        available_products_text=available_products_text,
    )
    response = generate_response(llm=llm, prompt=product_name_selection_prompt)
    state["messages"].append(AIMessage(response.content))
    return state
