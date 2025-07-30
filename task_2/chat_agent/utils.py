import json
import requests
from typing import Type

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel


from .config import NodeName, State
from .prompts import (
    PRODUCT_TYPE_ANALYSIS_PROMPT_TEMPLATE,
    ATTRIBUTES_ANALYSIS_PROMPT_TEMPLATE,
    PRODUCT_NAME_ANALYSIS_PROMPT_TEMPLATE,
)


SHOP_DOMAIN = "amirtest100.myshopify.com"
MCP_ENDPOINT = f"https://{SHOP_DOMAIN}/api/mcp"


def generate_response(
    llm: ChatOpenAI, prompt: str, output_format: Type[BaseModel] = None
):
    if output_format:
        llm = llm.with_structured_output(output_format, method="json_mode")
    response = llm.invoke(prompt)
    if output_format:
        response = response.model_dump()
    return response


def format_messages_for_prompt(messages: list[BaseMessage]) -> str:
    result = []
    for msg in messages:
        result.append(f"{msg.type.capitalize()}: {msg.content}")
    return "\n".join(result)


def format_dict_for_prompt(attr_dict: dict) -> str:
    lines = []
    for k, v in attr_dict.items():
        value = v if v else "[empty]"
        lines.append(f"{k}: {value}")
    return "\n".join(lines)


def format_list_for_prompt(items: list[str], style: str = "comma") -> str:
    if not items or len(items) == 0:
        return ""
    if style == "bullet":
        return "\n".join(f"- {item}" for item in items)
    return ", ".join(items)


def format_list_dict_for_prompt(
    items: list[dict[str, str]], style: str = "bullet"
) -> str:
    if not items or len(items) == 0:
        return ""
    lines = []
    for d in items:
        if style == "comma":
            content = ", ".join(f"{k}: {v}" for k, v in d.items())
        else:
            content = "\n  ".join(f"{k}: {v}" for k, v in d.items())
        lines.append(f"- {content}")
    return "\n".join(lines)


def get_payload(name, arguments):
    return {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "id": 1,
        "params": {"name": name, "arguments": arguments},
    }


def search_shop_catalog(product_type="shirt", description=""):
    payload = get_payload(
        name="search_shop_catalog",
        arguments={"query": product_type, "context": description},
    )
    headers = {"Content-Type": "application/json"}
    response = requests.post(MCP_ENDPOINT, json=payload, headers=headers, timeout=10)
    content = json.loads(response.json()["result"]["content"][0]["text"])
    products = []
    for product in content["products"]:
        products.append(
            {"name": product["title"], "description": product["description"]}
        )
    return products


def all_attributes_filled(attibutes: dict) -> bool:
    filled = True
    for key, value in attibutes.items():
        if value == "" or value is None:
            filled = False
    return filled


def is_finished(state: State) -> bool:
    return state["product_name"] != ""


def get_next_node(state):
    if state["product_type"] == "" or state["product_type"] is None:
        return NodeName.PRODUCT_TYPE_SELECTION
    else:
        if state["attributes"] == {}:
            return NodeName.ATTRIBUTE_NAMES_SELECTION
        filled = all_attributes_filled(attibutes=state["attributes"])
        if filled:
            if state["product_name"] == "" or state["product_name"] is None:
                return NodeName.PRODUCT_NAME_SELECTION
            else:
                return NodeName.END
        else:
            return NodeName.ATTRIBUTES_SELECTION


def get_analysis_prompt_template(state: State):
    if state["product_type"] == "" or state["product_type"] is None:
        return PRODUCT_TYPE_ANALYSIS_PROMPT_TEMPLATE
    else:
        filled = all_attributes_filled(attibutes=state["attributes"])
        if filled:
            if state["product_name"] == "" or state["product_name"] is None:
                return PRODUCT_NAME_ANALYSIS_PROMPT_TEMPLATE
            else:
                pass
        else:
            return ATTRIBUTES_ANALYSIS_PROMPT_TEMPLATE
