from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI


from ..config import State
from ..utils import generate_response, format_messages_for_prompt
from ..prompts import PRODUCT_TYPE_SELECTION_PROMPT_TEMPLATE


llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)


def product_type_selection_node(state: State) -> State:
    chat_history = format_messages_for_prompt(messages=state["messages"])
    product_type_selection_prompt = PRODUCT_TYPE_SELECTION_PROMPT_TEMPLATE.format(
        chat_history=chat_history
    )
    response = generate_response(llm=llm, prompt=product_type_selection_prompt)
    state["messages"].append(AIMessage(response.content))
    return state
