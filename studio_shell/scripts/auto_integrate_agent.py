import json
import os

def run_agent_simulation(user_query, config_path):
    """
    模擬 Agent 接收到串接後的 Prompt 並進行回答的過程。
    """
    print(f"🚀 [Agent 啟動中...]")
    print(f"📂 正在讀取左欄配置: {config_path}")

    # 1. 讀取左欄資訊
    if not os.path.exists(config_path):
        print("❌ 錯誤：找不到左欄配置檔案！")
        return

    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    agent_name = config.get("agent_name", "Unknown Agent")
    extra_context = config.get("extra_context", "")

    # 2. 執行串接 (Context Injection)
    # 這是你要求的核心：將左欄資訊串接到右邊的 Query
    integrated_prompt = f"""
    [SYSTEM MESSAGE]
    You are {agent_name}.
    
    [EXTRA CONTEXT FROM LEFT PANEL]
    {extra_context}
    
    [USER QUERY FROM RIGHT PANEL]
    {user_query}
    
    [INSTRUCTION]
    Please answer the user query strictly based on the provided context.
    """

    print("\n--- 📥 傳送至右欄 Agent 的完整 Prompt ---")
    print(integrated_prompt)
    print("--- 📤 傳送結束 ---\n")

    # 3. 模擬 Agent 的執行結果 (模擬 LLM 根據 Prompt 產出的回答)
    print(f"🤖 {agent_name} 正在思考...")
    
    # 這裡模擬 Agent 讀取了 Context 並找到了答案
    if "預算" in user_query and "20,000" in extra_context:
        response = "根據左欄提供的資訊，目前的預算剩餘 20,000 元。"
    elif "進度" in user_query and "50%" in extra_context:
        response = "根據左欄提供的資訊，目前的專案進度為 50%。"
    else:
        response = "我已收到您的問題，但我需要更多上下文資訊來回答。"

    print(f"\n✅ Agent 回答結果：\n{response}")

if __name__ == "__main__":
    # 設定路徑
    CONFIG_FILE = "studio_shell/workspace/agent_config.json"
    # 模擬使用者在右欄輸入的問題
    QUERY = "請告訴我目前的預算狀況。"
    
    run_agent_simulation(QUERY, CONFIG_FILE)
