# AI要約・解説＆音声化ツール

## 概要

本プロジェクトは、Web記事・画像・テキストをAIで要約・解説し、日本語音声に変換するツールです。
StreamlitによるWebアプリと、コマンドライン（CLI）両方で利用可能です。

---

## 主な機能

- **多様な入力対応**  
  - Web記事URL  
  - 画像ファイル（日本語OCR対応）  
  - 直接テキスト入力
- **AIによる要約・解説**  
  - Gemini API（Google Generative AI）を利用した日本語要約・解説生成
- **日本語音声合成**  
  - gTTS（Google Text-to-Speech）による音声ファイル（mp3）生成
- **WebアプリUI**  
  - Streamlitベースの直感的なインターフェース
- **CLIツール**  
  - コマンドラインからも一連の処理が可能

---

## ファイル構成

- `app.py` : Streamlit Webアプリ本体
- `main.py` : CLI用エントリポイント
- `extractor.py` : 入力（URL/画像/テキスト）から本文抽出
- `summarizer.py` : Gemini APIによる要約・解説生成
- `tts.py` : gTTSによる音声合成
- `config.yaml` : APIキーやプロンプト等の設定ファイル
- `requirements.txt` : 必要なPythonパッケージ一覧

---

## 使い方

### 1. セットアップ

```bash
pip install -r requirements.txt
```

- `config.yaml` の `gemini_api_key` にご自身のAPIキーを設定してください。

### 2. Webアプリとして起動

```bash
streamlit run app.py
```

### 3. CLIとして利用

```bash
python main.py <URLまたは画像ファイルパスまたはテキスト>
```

---

## 設定ファイル（config.yaml）

- `ai.gemini_api_key` : Gemini APIのAPIキー
- `ai.summarization_prompt` : 要約・解説のプロンプト
- `tts.lang` : 音声合成言語（デフォルト: ja）

---

## 依存ライブラリ

- google-generativeai
- requests
- gtts
- PyYAML
- beautifulsoup4
- readability-lxml
- pillow
- pytesseract
- streamlit

---

## 注意事項

- Gemini APIの利用にはAPIキーが必要です。
- 画像からの日本語テキスト抽出にはTesseract OCRが必要です（環境によっては別途インストールが必要）。
- 音声合成はgTTS（Google Text-to-Speech）を利用しています。

---

## ライセンス

MIT License

---

## 開発・貢献

バグ報告・機能要望・プルリクエスト歓迎します。

---

📝 詳細な実装や拡張方法については各モジュールのdocstringやコメントをご参照ください。 