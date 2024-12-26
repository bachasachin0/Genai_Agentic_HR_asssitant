# import streamlit as st
# from workflow import graph
# from mongodb_utils import get_session_history
# from typing import List, Dict
# import pprint
# from langchain_core.messages import BaseMessage, AIMessage, ToolMessage, HumanMessage
# import time

# # Function to simulate message processing with animation
# def process_event(event: Dict) -> List[BaseMessage]:
#     new_messages = []
#     for value in event.values():
#         if isinstance(value, dict) and 'messages' in value:
#             for msg in value['messages']:
#                 if isinstance(msg, BaseMessage):
#                     new_messages.append(msg)
#                 elif isinstance(msg, dict) and 'content' in msg:
#                     new_messages.append(AIMessage(content=msg['content'], additional_kwargs={'sender': msg.get('sender')}))
#                 elif isinstance(msg, str):
#                     new_messages.append(ToolMessage(content=msg))
#     return new_messages

# # Main function for the Streamlit application
# def main():
#     # Set up Streamlit page
#     st.set_page_config(page_title="AI Workflow", layout="wide")

#     # Display title
#     st.title("AI Workflow for Designing Teams")

#     # Placeholder for loading animation
#     loading_text = st.empty()
#     progress_bar = st.progress(0)

#     # Get session history
#     temp_mem = get_session_history("test")

#     # Streamlit widget to display the input message
#     input_message = "Design an iOS app development team for a new mobile application. Identify the key roles required, including their responsibilities and necessary skills."

#     # Show a loading message and simulate progress
#     loading_text.text("Processing your request...")
#     for i in range(1, 101):
#         progress_bar.progress(i)
#         time.sleep(0.05)

#     # Process the event
#     events = graph.stream(
#         {"messages": [HumanMessage(content=input_message)]},
#         {"recursion_limit": 17},
#     )

#     # Process and display messages
#     st.subheader("Messages:")
#     for event in events:
#         pprint.pprint(event)
#         new_messages = process_event(event)
#         if new_messages:
#             temp_mem.add_messages(new_messages)

#     # Display final state of messages with customized styling
#     st.subheader("Final state of temp_mem:")
#     if hasattr(temp_mem, 'messages'):
#         for msg in temp_mem.messages:
#             message_type = msg.__class__.__name__
#             message_content = msg.content
#             color = ""
            
#             # Add different colors or symbols based on the message type
#             if isinstance(msg, AIMessage):
#                 color = "lightblue"  # Blue color for AIMessage
#             elif isinstance(msg, ToolMessage):
#                 color = "lightgreen"  # Green color for ToolMessage
            
#             # Display message with color and symbol
#             st.markdown(f"""
#                 <div style="background-color:{color}; padding: 10px; margin: 5px; border-radius: 8px;">
#                     <b>Type: {message_type}</b><br>
#                     <pre>{message_content}</pre>
#                 </div>
#             """, unsafe_allow_html=True)
#     else:
#         st.write("temp_mem does not have a 'messages' attribute")

# # Run the app if this is the main module
# if __name__ == "__main__":
#     main()
#-------------------------------------------------------------------------------
# import streamlit as st
# from workflow import graph
# from mongodb_utils import get_session_history
# from typing import List, Dict
# import time
# from langchain_core.messages import BaseMessage, AIMessage, ToolMessage, HumanMessage


# # Function to simulate message processing with animation
# def process_event(event: Dict) -> List[BaseMessage]:
#     new_messages = []
#     for value in event.values():
#         if isinstance(value, dict) and 'messages' in value:
#             for msg in value['messages']:
#                 if isinstance(msg, BaseMessage):
#                     new_messages.append(msg)
#                 elif isinstance(msg, dict) and 'content' in msg:
#                     new_messages.append(AIMessage(content=msg['content'], additional_kwargs={'sender': msg.get('sender')}))
#                 elif isinstance(msg, str):
#                     new_messages.append(ToolMessage(content=msg))
#     return new_messages


# # Cache function to process the graph and messages
# @st.cache_data
# def generate_messages(user_input: str) -> List[BaseMessage]:
#     # Get session history
#     temp_mem = get_session_history("test")

#     # Process the event
#     events = graph.stream(
#         {"messages": [HumanMessage(content=user_input)]},
#         {"recursion_limit": 17},
#     )

#     # Process and store new messages
#     all_messages = []
#     for event in events:
#         new_messages = process_event(event)
#         all_messages.extend(new_messages)
#         temp_mem.add_messages(new_messages)

#     return all_messages


# # Main function for the Streamlit application
# def main():
#     # Set up Streamlit page with custom theme
#     st.set_page_config(page_title="AI Team Design Workflow", layout="wide")

#     # Title of the app
#     st.markdown("<h1 style='text-align: center; color: #2F4F4F;'>AI Team Design Workflow</h1>", unsafe_allow_html=True)
#     st.markdown("<p style='text-align: center; color: #2F4F4F;'>Designing a team for iOS app development.</p>", unsafe_allow_html=True)

#     # Sidebar for input
#     st.sidebar.title("User Input")
#     user_input = st.sidebar.text_area("Enter a description or request", height=200)

#     # Submit button for processing the input
#     if st.sidebar.button("Process Request"):
#         if user_input:
#             # Show progress bar and loading message while processing
#             loading_text = st.empty()
#             progress_bar = st.progress(0)

#             # Display loading message
#             loading_text.text("Processing your request...")
#             for i in range(1, 101):
#                 progress_bar.progress(i)
#                 time.sleep(0.05)

#             # Call the cache function to generate the messages
#             generated_messages = generate_messages(user_input)

#             # Display final state of messages
#             st.subheader("Final state of temp_mem:")

#             # Loop through each message and display with a 3-second delay
#             for idx, msg in enumerate(generated_messages):
#                 message_type = msg.__class__.__name__
#                 message_content = msg.content
#                 color = ""

#                 # Add different colors or symbols based on the message type
#                 if isinstance(msg, AIMessage):
#                     color = "#ADD8E6"  # Light blue color for AIMessage
#                 elif isinstance(msg, ToolMessage):
#                     color = "#98FB98"  # Light green color for ToolMessage

#                 # Add delay to make the messages appear one by one with animation
#                 time.sleep(2)  # 3-second delay

#                 # Use expandable and collapsible sections for the message content
#                 with st.expander(f"{message_type}", expanded=False):
#                     # Add glow effect and black text color for the content
#                     st.markdown(f"""
#                         <div style="background-color:{color}; padding: 15px; margin: 10px 0; border-radius: 12px; 
#                                     box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1), 0 0 15px {color};">
#                             <b style="font-size: 18px; color: #2F4F4F;">Type: {message_type}</b><br>
#                             <pre style="color: black; font-size: 16px; white-space: pre-wrap; word-wrap: break-word;">
#                                 {message_content}
#                             </pre>
#                         </div>
#                     """, unsafe_allow_html=True)
#         else:
#             st.error("Please enter a request in the text box before clicking 'Process Request'.")


# # Run the app if this is the main module
# if __name__ == "__main__":
#     main()
#-------------------------------------------------------
import streamlit as st
from workflow import graph
from mongodb_utils import get_session_history
from typing import List, Dict
import time
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage, HumanMessage
from config import MONGO_URI
from pymongo import MongoClient

# Function to clear the history collection
def clear_history_collection():
    # Connect to MongoDB using the URI
    client = MongoClient(MONGO_URI)
    
    # Access the database and collection

    db = client["company_employees"]
    history_collection = db["history"]
    
    # Delete all documents in the collection
    result = history_collection.delete_many({})
    
    # client.close()

    
    # Log the result
    print(f"Deleted {result.deleted_count} documents from the history collection.")
    return result.deleted_count


# Function to simulate message processing with animation
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


# Cache function to process the graph and messages

def generate_messages(user_input: str) -> List[BaseMessage]:
    # Get session history
    temp_mem = get_session_history("test")

    # Process the event
    events = graph.stream(
        {"messages": [HumanMessage(content=user_input)]},
        {"recursion_limit": 17},
    )

    # Process and store new messages
    all_messages = []
    for event in events:
        new_messages = process_event(event)
        all_messages.extend(new_messages)
        temp_mem.add_messages(new_messages)

    return all_messages


# Main function for the Streamlit application
def main():
   
    # Sidebar for input
    st.sidebar.title("User Input")
    user_input = st.sidebar.text_area("Enter a description or request", height=200)
    # Sidebar button for clearing history
    if st.sidebar.button("Clear History"):
        # Simulate a dialog with a selectbox for confirmation
        confirmation = st.radio(
            "Are you sure you want to clear the history? This action cannot be undone.",
            ("select option","Yes, Clear History", "No, Return")
        )

        if confirmation == "Yes, Clear History":
            # Confirm clear history
            deleted_count = clear_history_collection()
            st.success(f"History cleared! Deleted {deleted_count} documents.")
            # Optionally, rerun the page to refresh the state
            # st.experimental_rerun()  # Refresh the app to remove the selectbox options

        elif confirmation == "No, Return":
            st.info("History clearing was canceled.")

    # Submit button for processing the input
    if st.sidebar.button("Process Request"):
        if user_input:
            # Show progress bar and loading message while processing
            loading_text = st.empty()
            progress_bar = st.progress(0)

            # Display loading message
            loading_text.text("Processing your request...")
            for i in range(1, 101):
                progress_bar.progress(i)
                time.sleep(0.05)

            # Call the cache function to generate the messages
            generated_messages = generate_messages(user_input)

            # Display final state of messages
            st.subheader("Final state of temp_mem:")

            # Loop through each message and display with a 3-second delay
            for idx, msg in enumerate(generated_messages):
                message_type = msg.__class__.__name__
                message_content = msg.content
                color = ""

                # Add different colors or symbols based on the message type
                if isinstance(msg, AIMessage):
                    color = "#ADD8E6"  # Light blue color for AIMessage
                elif isinstance(msg, ToolMessage):
                    color = "#98FB98"  # Light green color for ToolMessage

                # Add delay to make the messages appear one by one with animation
                time.sleep(2)  # 3-second delay

                # Use expandable and collapsible sections for the message content
                with st.expander(f"{message_type}", expanded=False):
                    # Add glow effect and black text color for the content
                    st.markdown(f"""
                        <div style="background-color:{color}; padding: 15px; margin: 10px 0; border-radius: 12px; 
                                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1), 0 0 15px {color};">
                            <b style="font-size: 18px; color: #2F4F4F;">Type: {message_type}</b><br>
                            <pre style="color: black; font-size: 16px; white-space: pre-wrap; word-wrap: break-word;">
                                {message_content}
                            </pre>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("Please enter a request in the text box before clicking 'Process Request'.")


# Run the app if this is the main module
if __name__ == "__main__":
    main()

