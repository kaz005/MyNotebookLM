import os
from dotenv import load_dotenv

print("[DIAGNOSE] .envファイルの自動ロードを開始...")
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
if api_key:
    print(f"[OK] OPENAI_API_KEYが取得できました: {api_key[:8]}...（一部省略）")
else:
    print("[NG] OPENAI_API_KEYが取得できませんでした。\n- .envの場所・内容・不可視文字・権限を再確認してください。\n- .envはプロジェクトルートにあり、'OPENAI_API_KEY=xxxx'の形式で記載されていますか？") 