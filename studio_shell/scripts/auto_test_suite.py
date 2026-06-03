import json
import os
import subprocess

def run_test_case(test_name, new_context, expected_keyword):
    """
    自動化測試案例：
    1. 修改左欄配置
    2. 執行 Agent 腳本
    3. 驗證結果是否包含預期關鍵字
    """
    config_path = "studio_shell/workspace/agent_config.json"
    agent_script = "studio_shell/scripts/auto_integrate_agent.py"
    
    print(f"🧪 [測試開始] 案例名稱: {test_name}")
    
    # 1. 修改左欄配置 (Update Left Panel)
    try:
        with open(config_app_path := config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        config["extra_context"] = new_context
        
        with open(config_app_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        print(f"✅ 已更新左欄 Context: {new_context[:30]}...")
    except Exception as e:
        print(f"❌ 更新配置失敗: {e}")
        return False

    # 2. 執行 Agent 腳本 (Execute Agent)
    print(f"🚀 正在啟動 Agent 進行驗證...")
    try:
        # 使用 uv run 執行
        result = subprocess.run(
            ["uv", "run", "python", agent_script],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout
        print(f"📄 Agent 輸出內容:\n{output}")
    except Exception as e:
        print(f"❌ 執行 Agent 失敗: {e}")
        return False

    # 3. 驗證結果 (Verify Result)
    if expected_keyword in output:
        print(f"✨ [測試通過] 成功偵測到關鍵字: '{expected_keyword}'")
        return True
    else:
        print(f"🚨 [測試失敗] 未能在輸出中找到關鍵字: '{expected_keyword}'")
        return False

if __name__ == "__main__":
    # 測試案例 1: 測試預算變動
    print("=== 測試案例 1: 預算變動 ===")
    run_test_case(
        "Budget Change Test", 
        "目前的專案進度是 100%，預算剩餘 5,000 元。", 
        "5,000"
    )

    print("\n" + "="*30 + "\n")

    # 測試案例 2: 測試日期變動
    print("=== 測試案例 2: 日期變動 ===")
    run_test_case(
        "Date Change Test", 
        "截止日期已更改為 2025-01-01。", 
        "2025-01-01"
    )
