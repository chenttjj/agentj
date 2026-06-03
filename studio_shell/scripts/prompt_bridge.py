import json
import sys
import os

def build_prompt(user_query, config_path):
    """
    讀取左欄的 JSON 配置，並將 extra_context 注入到 User Query 中。
    """
    if not os.path.exists(config_path):
        return f"Error: Configuration file not found at {config_path}"

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        extra_context = config.get("extra_context", "")
        agent_name = config.get("agent_name", "Assistant")

        # 構建最終的 Prompt 結構
        full_prompt = f"--- Agent Role: {agent_name} ---\n"
        full_prompt += f"--- Extra Context ---\n{extra_context}\n"
        full_prompt += f"--- User Query ---\n{user_query}\n"
        full_prompt += "----------------------\n"
        full_prompt += "Please process the query using the context provided above."
        
        return full_prompt

    except Exception as e:
        return f"Error processing prompt: {str(e)}"

if __name__ == "__main__":
    # 預設配置路徑
    CONFIG_FILE = "studio_shell/workspace/agent_config.json"
    
    # 從命令列接收使用者問題 (如果有的話)
    # 使用方式: uv run python studio_shell/scripts/prompt_bridge.py "你的問題"
    query = sys.argv[1] if len(sys.argv) > 1 else "預設測試問題"
    
    result_prompt = build_prompt(query, CONFIG_FILE)
    print(result_prompt)
