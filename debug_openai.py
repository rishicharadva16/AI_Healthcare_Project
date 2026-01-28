import os
from openai import OpenAI

try:
    client = OpenAI(api_key="test")
    print(f"Client attributes: {dir(client)}")
    if hasattr(client, 'responses'):
        print("client.responses EXISTS")
    else:
        print("client.responses DOES NOT EXIST")
except Exception as e:
    print(f"Error: {e}")
