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

---

## APIスイッチ機構（ダミー⇄本番API切替）

- 本ツールはGemini要約APIの「ダミー（スタブ）⇄本番API」を**環境変数または設定ファイル**で切り替え可能です。
- テストやCIでは`USE_DUMMY_API=true`（または`config.yaml: ai.use_dummy_api: true`）で**外部APIを呼ばずに安全に検証**できます。
- 実装はFactoryパターン/DI方式で、SDK版・REST版のインターフェースを統一しています。
- 詳細設計は`docs/adr/0001-api-switch.md`を参照してください。

---

## アクセシビリティ・セキュリティ・運用要件

- **アクセシビリティ**
  - コントラスト比4.5:1以上、キーボード操作対応、WCAG 2.1 AAレベルを満たす設計です。
- **セキュリティ**
  - APIキーは`.env`またはGitHub Secretsで安全に管理し、90日ごとにローテーション推奨。
  - 監査ログ・データマスキング・TLS1.2以上の暗号化を実施。
- **運用・監視**
  - 主要メトリクス（要約/音声合成成功率・処理時間等）をELK等でモニタリング。
  - 失敗率5%超でSlack等に自動アラート。
  - ログはJSON形式・トレースID付きで30日間保存。
- **DB・スケール**
  - 履歴DBはSQLite/DuckDBを選択可能。クラウド移行時はマネージドDBも検討。

---

## ドキュメント・設計方針

- 詳細な設計・運用ルールは`docs/`配下（例：`docs/accessibility.md`, `docs/security.md`, `docs/monitoring.md`）やADR（`docs/adr/0001-api-switch.md`）に記載しています。
- CI/CD・E2E・監視設定例は`.github/workflows/`や`docs/monitoring.md`を参照してください。 