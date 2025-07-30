from typing import TypedDict, Union, Dict
from enum import Enum

from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage


class NodeName(str, Enum):
    ANALYSIS = "analysis"
    PRODUCT_TYPE_SELECTION = "product_type_selection"
    ATTRIBUTE_NAMES_SELECTION = "attribute_names_selection"
    ATTRIBUTES_SELECTION = "attributes_selection"
    PRODUCT_NAME_SELECTION = "product_name_selection"
    START = "start"
    END = "end"


class State(TypedDict, total=False):
    messages: list[BaseMessage]
    intent: str
    next_node: str
    product_type: str
    attributes: dict[str:str]
    product_name: str
    is_finished: bool


class AnalysisResponse(BaseModel):
    result: Dict[str, Union[str, Dict[str, str]]] = Field(
        ..., description="The retrieved result by LLM"
    )
    intent: str = Field(..., description="The intent of the user message")


class AttributeNames(BaseModel):
    result: list[str] = Field(..., description="A list of attribute names")
