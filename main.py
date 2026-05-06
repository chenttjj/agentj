import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()

def main():
    agent_name = "Akuma"
    print(f"--- {agent_name} Agent System Initialized ---")


    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("MODEL")
    base_url = os.getenv("BASE_URL")
    temp_env = os.getenv("TEMPERATURE")

    if api_key:
        print("OPENAI_API_KEY :已設定")
    else:
        print("未設定 OPENAI_API_KEY；請檢查 .env 或系統環境變數")
        return
        
    try:
        temperature = float(temp_env)
    except ValueError:
        temperature = 0.0

    llm = ChatOpenAI(
        model=model_name,
        base_url=base_url,
        api_key=api_key,
        temperature=temperature
    )
    while True:
        user_input = input("you :").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("bye")
            break
        if not user_input:
            continue

        
        for chunk in llm.stream(user_input):
            print(chunk.content,end="",flush=True)
        print()

    print(f"Using model: {model_name}")
    message = llm.invoke("Hello, World!")
    print(message.content)


if __name__ == "__main__":
    main()
