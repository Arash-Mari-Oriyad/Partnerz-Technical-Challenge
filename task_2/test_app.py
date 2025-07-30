import requests

API_URL = "http://localhost:8000/chat"

messages = [
    {"role": "ai", "content": "Hi. I am your shopping assistant."},
    {"role": "human", "content": "Hi, how are you?"},
]

state = {
    "messages": messages,
    "next_node": "",
    "product_type": "",
    "attributes": {},
    "product_name": "",
    "is_finished": False,
}

response = requests.post(
    API_URL,
    json={"messages": messages, "state": state},
)

data = response.json()
print(data["ai_message"])
