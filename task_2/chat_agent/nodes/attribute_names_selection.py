import ast

from langchain_openai import ChatOpenAI

from ..utils import generate_response
from ..config import State, AttributeNames
from ..prompts import ATTRIBUTE_NAMES_SELECTION_PROMPT_TEMPLATE


llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)


def attribute_names_selection_node(state: State) -> State:
    attribute_names_selection_prompt = ATTRIBUTE_NAMES_SELECTION_PROMPT_TEMPLATE.format(
        product_type=state["product_type"],
    )
    response = generate_response(
        llm=llm, prompt=attribute_names_selection_prompt, output_format=AttributeNames
    )
    state["attributes"] = {key: "" for key in response["result"]}
    return state
