from langchain_openai import ChatOpenAI

from ..config import State, AnalysisResponse
from ..utils import (
    generate_response,
    is_finished,
    get_analysis_prompt_template,
    format_list_for_prompt,
)


llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)


def analysis_node(state: State) -> State:
    attribute_names = format_list_for_prompt(list(state.get("attributes", {}).keys()))
    available_product_names = format_list_for_prompt(
        state.get("available_product_names", [])
    )
    analysis_prompt_template = get_analysis_prompt_template(state=state)
    analysis_prompt = analysis_prompt_template.format(
        user_message=state["messages"][-1].content,
        attribute_names=attribute_names,
        available_product_names=available_product_names,
        product_type=state["product_type"],
    )
    response = generate_response(
        llm=llm, prompt=analysis_prompt, output_format=AnalysisResponse
    )
    state["intent"] = response["intent"]
    for key in response["result"].keys():
        if isinstance(response["result"][key], str):
            state[key] = response["result"][key]
        else:
            for k in response["result"][key].keys():
                if response["result"][key][k] != "":
                    state[key][k] = response["result"][key][k]
    state["is_finished"] = is_finished(state=state)
    return state
