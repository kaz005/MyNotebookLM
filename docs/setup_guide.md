# セットアップガイド

## 1. Python依存パッケージのインストール
```bash
pip install -r requirements.txt
```

## 2. Tesseract OCRのインストール
- macOS: `brew install tesseract`
- Ubuntu: `sudo apt-get install tesseract-ocr`
- Windows: [公式インストーラ](https://github.com/tesseract-ocr/tesseract)

## 3. Google Gemini APIキーの取得
1. [Google AI Studio](https://aistudio.google.com/app/apikey) にアクセス
2. APIキーを発行
3. `config.yaml` の `gemini_api_key` にコピー

## 4. 設定ファイルの編集
- `config.yaml` にAPIキーやプロンプト等を設定

## 5. 動作確認
- Webアプリ: `streamlit run app.py`
- CLI: `python main.py <入力>`

---

※詳細はREADMEも参照してください。 