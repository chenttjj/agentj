import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()



def main():
    agent_name = "Akuma"
    print(f"--- {agent_name} Agent System Initialized ---")
    api_key = os.getenv("OPENAI_API_KEY")
    print(api_key)
    print("Hello, World!")   
if __name__ == "__main__":
    main()

