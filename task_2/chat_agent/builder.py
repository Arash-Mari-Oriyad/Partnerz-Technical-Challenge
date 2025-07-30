from langgraph.graph import StateGraph

from .config import NodeName, State
from .nodes.analysis import analysis_node
from .nodes.start import start_node
from .nodes.end import end_node
from .nodes.product_type_selection import product_type_selection_node
from .nodes.attribute_names_selection import attribute_names_selection_node
from .nodes.attributes_selection import attributes_selection_node
from .nodes.product_name_selection import product_name_selection_node
from .utils import get_next_node


def build_graph():
    graph = StateGraph(State)

    graph.add_node(NodeName.START, start_node)
    graph.add_node(NodeName.ANALYSIS, analysis_node)
    graph.add_node(NodeName.PRODUCT_TYPE_SELECTION, product_type_selection_node)
    graph.add_node(NodeName.ATTRIBUTE_NAMES_SELECTION, attribute_names_selection_node)
    graph.add_node(NodeName.ATTRIBUTES_SELECTION, attributes_selection_node)
    graph.add_node(NodeName.PRODUCT_NAME_SELECTION, product_name_selection_node)
    graph.add_node(NodeName.END, end_node)

    graph.set_entry_point(NodeName.START)

    graph.add_edge(NodeName.START, NodeName.ANALYSIS)

    graph.add_conditional_edges(
        NodeName.ANALYSIS,
        lambda state: get_next_node(state),
        {
            "product_type_selection": NodeName.PRODUCT_TYPE_SELECTION,
            "attribute_names_selection": NodeName.ATTRIBUTE_NAMES_SELECTION,
            "attributes_selection": NodeName.ATTRIBUTES_SELECTION,
            "product_name_selection": NodeName.PRODUCT_NAME_SELECTION,
            "end": NodeName.END,
        },
    )

    graph.add_edge(NodeName.ATTRIBUTE_NAMES_SELECTION, NodeName.ATTRIBUTES_SELECTION)

    for node_name in [
        NodeName.PRODUCT_TYPE_SELECTION,
        NodeName.ATTRIBUTES_SELECTION,
        NodeName.PRODUCT_NAME_SELECTION,
    ]:
        graph.add_edge(node_name, NodeName.END)

    return graph.compile()
