import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()

def main():
    # 1. Check for API Key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("Error: OPENAI_API_KEY is not set correctly in your .env file.")
        print("Please edit the .env file and add your actual OpenAI API Key.")
        sys.exit(1)

    agent_name = "Akuma"
    print(f"--- {agent_name} Agent System Initialized ---")

    # 2. Initialize the Model
    # It will automatically use OPENAI_API_KEY from the environment
    llm = ChatOpenAI(model="gpt-4o")

    # 3. Simple Interaction
    print("\nAsking Akuma to introduce itself...")
    try:
        response = llm.invoke("請用繁體中文簡單介紹你自己，並說你是這個專案的 AI 助手。")
        print(f"\nAkuma: {response.content}")
    except Exception as e:
        print(f"\nAn error occurred while calling the OpenAI API: {e}")

if __name__ == "__main__":
    main()

