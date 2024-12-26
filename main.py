# main.py

from workflow import graph
from mongodb_utils import get_session_history
from typing import List, Dict
import pprint
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage, HumanMessage


temp_mem = get_session_history("test")

events = graph.stream(
    {"messages": [HumanMessage(content="Design an iOS app development team for a new mobile application. Identify the key roles required, including their responsibilities and necessary skills.")]},
    {"recursion_limit": 17},
)

def process_event(event: Dict) -> List[BaseMessage]:
    new_messages = []
    for value in event.values():
        if isinstance(value, dict) and 'messages' in value:
            for msg in value['messages']:
                if isinstance(msg, BaseMessage):
                    new_messages.append(msg)
                elif isinstance(msg, dict) and 'content' in msg:
                    new_messages.append(AIMessage(content=msg['content'], additional_kwargs={'sender': msg.get('sender')}))
                elif isinstance(msg, str):
                    new_messages.append(ToolMessage(content=msg))
    return new_messages

for event in events:
    pprint.pprint(event)
    new_messages = process_event(event)
    if new_messages:
        temp_mem.add_messages(new_messages)

print("\nFinal state of temp_mem:")
if hasattr(temp_mem, 'messages'):
    for msg in temp_mem.messages:
        print(f"Type: {msg.__class__.__name__}")
        print(f"Content: {msg.content}")
        if msg.additional_kwargs:
            pprint.pprint(msg.additional_kwargs)
        print("---")
else:
    print("temp_mem does not have a 'messages' attribute")
