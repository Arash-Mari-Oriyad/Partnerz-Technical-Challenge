# Multi-Turn Sales & Shopping Chatbot

## Overview

This project implements a robust multi-turn conversational AI chatbot for online sales and shopping assistance. The system guides users through a natural conversation to discover products, clarify preferences, and recommend items from a real or simulated catalog, leveraging modular orchestration and LLM reasoning.

---

## Project Structure

```
task_2/
│
├── app.py                       # Main entry point to run the chatbot
├── test_app.py                  # Basic tests for chatbot logic
├── conversation_example.md      # Example conversation for demo/testing
├── requirements.txt             # Python dependencies
│
└── chat_agent/
    ├── __init__.py
    ├── config.py                # Central configuration (product attributes, prompt settings)
    ├── prompts.py               # All LLM prompt templates and helpers
    ├── builder.py               # Constructs the chatbot's LangGraph
    ├── usage_example.py         # Example of using the agent programmatically
    ├── utils.py                 # Utilities (Shopify MCP integration, helpers)
    │
    └── nodes/
        ├── start.py                      # Start node (greeting, welcome)
        ├── end.py                        # End node (goodbye)
        ├── product_type_selection.py     # Asks user for product category/type
        ├── product_name_selection.py     # Gathers specific product name or brand
        ├── attribute_names_selection.py  # Selects which attributes to clarify
        ├── attributes_selection.py       # Collects attribute values (e.g., size, color)
        ├── analysis.py                   # LLM-based intent analysis or decision
```

---

## Design & Architecture

### LangGraph Orchestration

At the heart of this project is [LangGraph](https://github.com/langchain-ai/langgraph), a stateful computation framework for building complex multi-turn conversational agents. LangGraph allows you to represent your chatbot’s **dialogue flow as a directed graph** of nodes and edges:

- **Nodes** represent discrete conversational actions or states (e.g., greeting, asking for product type, analysis, ending).
- **Edges** define transitions between nodes, usually determined by user input or the result of LLM reasoning.

**LangGraph Structure in This Project:**
- The conversation starts at the `start` node (greeting).
- The agent traverses through product discovery steps (`product_type_selection`, `product_name_selection`).
- The `attribute_names_selection` node determines which attributes (like size/color) are relevant.
- The `attributes_selection` node collects user preferences for those attributes.
- The `analysis` node may be used to clarify user intent or finalize the product recommendation.
- The flow concludes at the `end` node.

This graph structure is assembled in `chat_agent/builder.py` and makes it trivial to adjust, extend, or reorder the conversational logic by modifying nodes and transitions.

### LLM Prompt Engineering

All prompts and dialogue templates are managed in `prompts.py` and `config.py`, enabling easy updates and experimentations with LLM instruction patterns. This ensures that all interactions are clear, consistent, and optimized for high-quality user experience.

### Product Search via Shopify Storefront MCP

A core functionality of the chatbot is **real-time product discovery**. The project integrates with the Shopify Storefront MCP (Multi-Channel Platform) API, allowing the chatbot to:
- Search and retrieve live product information (titles, descriptions, prices, images).
- Surface actual product recommendations to the user based on preferences collected in the chat.

All Shopify API interaction logic is abstracted in `utils.py`, making it easy to swap between real API and mock/testing mode.

### Utility Layer

The `utils.py` module centralizes:
- Functions for querying Shopify’s Storefront MCP
- Formatting and normalization utilities for product data
- Helper functions for dialog flow

This design keeps node logic focused and clean, while enabling code reuse.

---

## How to Run

1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Configure Shopify MCP access (if using live data):**
    - Set environment variables or edit config as described in `chat_agent/config.py`.

3. **Run the chatbot:**
    ```bash
    python app.py
    ```

4. **Example code:**  
    See `chat_agent/usage_example.py` for integrating or testing the agent in scripts.

---

## Extending the Chatbot

- **To add a new conversational step:**  
  Create a new Python file in `chat_agent/nodes/`, then connect it in `builder.py` as a new node in the LangGraph flow.
- **To adjust prompts or attributes:**  
  Modify or add prompt templates in `prompts.py` or configuration in `config.py`.
- **To integrate new APIs:**  
  Add or update utility functions in `utils.py`.

---

## Example Conversation

A step-by-step sample dialogue is provided in `conversation_example.md`.  
This showcases the full multi-turn flow, from greeting to recommendation and farewell.

---

## Testing

- Run all tests with:
    ```bash
    python test_app.py
    ```
- The suite covers critical logic and edge cases for multi-turn chat flows and product retrieval.

---

