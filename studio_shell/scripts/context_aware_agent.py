import os

def run_agent():
    # 1. 定義路徑
    workspace_dir = "studio_shell/workspace"
    context_file = os.path.join(workspace_dir, "context.txt")
    
    # 2. 模擬使用者輸入的 Query (這部分在 Playground 頁面會由 UI 提供)
    user_query = "請幫我寫一段關於機器學習的介紹。"

    print("--- [Agent 啟動中] ---")
    
    # 3. 核心邏輯：讀取 Extra Context
    extra_context = ""
    if os.path.exists(context_file):
        with open(context_file, "r", encoding="utf-8") as f:
            extra_context = f.read()
        print(f"[系統訊息] 成功讀取到 Extra Context。")
    else:
        print("[系統警告] 未發現 Context 檔案，將使用預設 Prompt。")

    # 4. 構建最終的 Prompt (Context Injection)
    # 我們將 Context 放在 Prompt 的最前面，作為指令的補充
    final_prompt = f"【Extra Context】\n{extra_context}\n\n【User Query】\n{user_query}"
    
    print("\n--- [最終注入 LLM 的 Prompt 內容] ---")
    print(final_prompt)
    print("--------------------------------------\n")

    # 5. 模擬 LLM 回應 (在實際環境中，這裡會呼叫 OpenAI/Anthropic API)
    print("[Agent 回應模擬]:")
    if "專業" in extra_context:
        print("機器學習是一種利用數據與演算法來進行學習的技術，其核心在於從經驗中提取模式...")
    else:
        print("機器學習是讓電腦學習的技術。")

if __name__ == "__main__":
    run_agent()
