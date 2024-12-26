# llm_utils.py

from langchain_groq import ChatGroq

def get_llm():
    # Example using ChatGroq
    llm = ChatGroq(
        model="mixtral-8x7b-32768",
        temperature=0.1
    )
    return llm

# def get_google_genai():
#     # Example using GoogleGenerativeAI
#     genai_llm = GoogleGenerativeAI()
#     return genai_llm

# def get_openai_llm():
#     # Example using OpenAI
#     llm = ChatOpenAI(model="gpt-4o-2024-05-13", temperature=0)
#     return llm
