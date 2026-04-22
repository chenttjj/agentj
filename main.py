import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAi
load_dotenv()


def main():
    agent_name = "akuma"
    print(f"Hello {agent_name}")


if __name__ == "__main__":
    main()
