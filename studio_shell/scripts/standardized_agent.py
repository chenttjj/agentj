import json
import os

class ContextManager:
    def __init__(self, context_path):
        self.context_path = context_path
        self.data = {}

    def load_context(self):
        """從 JSON 檔案載入結構化上下文"""
        if os.path.exists(self.context_path):
            try:
                with open(self.context_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                return True
            except Exception as e:
                print(f"[錯誤] 載入 Context 失敗: {e}")
                return False
        return False

    def build_prompt_components(self):
        """將 JSON 結構轉換為 Prompt 的各個組成部分"""
        components = {
            "system": self.data.get("system_prompt", "You are a helpful assistant."),
            "preferences": "",
            "knowledge": "",
            "constraints": ""
        }
        
        # 處理使用者偏好
        prefs = self.data.get("user_preferences", {})
        if prefs:
            pref_list = [f"- {k}: {v}" for k, v in prefs.items()]
            components["preferences"] = "\n".join(pref_list)
            
        # 處理知識庫
        kb = self.data.get("knowledge_base", [])
        if kb:
            components["knowledge"] = "\n".join([f"- {item}" for item in kb])
            
        # 處理限制條件
        constraints = self.data.get("constraints", [])
        if constraints:
            components["constraints"] = "\n".join([f"- {c}" for c in constraints])
            
        return components

def run_standardized_agent():
    # 設定路徑
    context_file = "studio_shell/workspace/config_context.json"
    
    # 1. 初始化 Context Manager (模擬 Home Page 的初始化邏輯)
    manager = ContextManager(context_file)
    
    print("--- [Agent 啟動中：Home 模式初始化] ---")
    
    # 2. 載入與解析
    if manager.load_context():
        print("[系統] 成功從左欄配置載入結構化 Context。")
        components = manager.build_prompt_components()
        
        # 3. 模擬 User Query
        user_query = "請介紹一下這個專案，並告訴我你的身份。"
        
        # 4. 構建最終 Prompt (注入過程)
        final_prompt = f"### SYSTEM INSTRUCTION ###\n{components['system']}\n\n"
        if components['preferences']:
            final_prompt += f"### USER PREFERENCES ###\n{components['preferences']}\n\n"
        if components['knowledge']:
            final_prompt += f"### KNOWLEDGE BASE ###\n{components['knowledge']}\n\n"
        if components['constraints']:
            final_prompt += f"### CONSTRAINTS ###\n{components['constraints']}\n\n"
        final_prompt += f"### USER QUERY ###\n{user_query}"
        
        print("\n--- [最終注入 LLM 的結構化 Prompt] ---")
        print(final_prompt)
        print("--------------------------------------\n")
        
        # 5. 模擬 Agent 執行
        print("[Agent 回應模擬]:")
        # 檢查是否有包含「法鬥超人」的限制
        if "法鬥超人" in final_prompt and "介紹" in user_query:
            print("你好！我是法鬥超人，你的程式助教。這個專案是 Agent Studio，一個基於 Streamlit 的自動化實驗室...")
        else:
            print("我正在處理您的請求...")
            
    else:
        print("[錯誤] 無法讀取 Context，請檢查左欄配置。")

if __name__ == "__main__":
    run_standardized_agent()
