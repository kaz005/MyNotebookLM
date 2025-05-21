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
  - OpenAI GPT-4.1-nano（現状の主機能）による日本語要約・解説生成  
  - Gemini API（Google Generative AI）は将来対応予定
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
- `summarizer.py` : OpenAI GPT-4.1-nanoによる要約・解説生成（Gemini APIは未実装）
- `tts.py` : gTTSまたはGoogle Cloud TTSによる音声合成
- `config.yaml` : サンプル設定ファイル（詳細はconfig.sample.yaml参照）
- `requirements.txt` : 必要なPythonパッケージ一覧

---

## 入力条件・制限事項

| 入力種別 | 制限内容 |
|----------|------------------------------------------------------|
| URL      | httpsのみ対応・本文最大10万文字・無効URLはエラー      |
| 画像     | png/jpg/jpeg/webp・最大10MB・TIFF等は未対応           |
| テキスト | 最大100,000文字・空文字/Noneはエラー                 |

---

## エラーコード一覧・トラブルシューティング

| エラーコード         | 主な原因                       | 対処法                         |
|---------------------|-------------------------------|--------------------------------|
| ERR_INVALID_URL     | URL形式不正/非https            | 入力URLを確認                  |
| ERR_OCR_FAIL        | 画像に文字がない/解析失敗      | 画像内容・形式を確認           |
| ERR_TTS_TIMEOUT     | 音声合成APIタイムアウト         | 再試行・ネットワーク確認        |
| ERR_INPUT_TOO_LONG  | 入力が最大長超過               | 入力を短くする                  |
| ERR_EMPTY_INPUT     | 入力が空/None                  | 有効な値を入力                  |
| ERR_UNSUPPORTED_FORMAT | 未対応画像/ファイル形式      | png/jpg/jpeg/webpのみ対応       |
| ERR_PDF_GENERATION  | PDF出力時のフォント等の失敗    | サーバ側フォント設定を確認      |
| ERR_STORAGE_FULL    | 履歴DB容量超過                 | 古い履歴削除・容量拡張          |

---

## セットアップガイド

- 詳細なセットアップ手順（Tesseract/Gemini API等）は `docs/setup_guide.md` を参照してください。
- **APIキー・各種設定は `.env` ファイルで管理します（git管理しません）**
- サンプルとして `.env.sample` を同梱しています。必要に応じてコピー・編集してください。
- `config.yaml` はサンプルとして `config.sample.yaml` を参照してください。

### .env.sample の内容例
```env
OPENAI_API_KEY=sk-xxxxxxx
GOOGLE_API_KEY=your-gemini-api-key
SUMMARIZER_ENGINE=openai  # openai/gemini/dummy
USE_DUMMY_API=false
TTS_ENGINE=gtts  # gtts/google_cloud
```

---

## 使い方

### 1. セットアップ

#### Python依存パッケージ
```bash
pip install -r requirements.txt
```

#### Tesseract OCRのインストール
- macOS: `brew install tesseract`
- Ubuntu: `sudo apt-get install tesseract-ocr`
- Windows: [公式インストーラ](https://github.com/tesseract-ocr/tesseract)

#### .envファイルの作成
- `.env.sample` をコピーして `.env` を作成し、APIキー等を記入

### 2. Webアプリとして起動
```bash
streamlit run app.py
```

### 3. CLIとして利用
```bash
python main.py <URLまたは画像ファイルパスまたはテキスト>
```

---

## 主な機能
- ビジネス風の高コントラストUI（ダーク/ライト両対応）
- Web記事・画像・テキストのAI要約＆日本語音声化
- 履歴はSQLite DB（notebooklm_history.db）に自動保存
- .envでAPIキー・エンジン切替を一元管理
- .envはgit管理せず、.env.sampleを利用

---

## 注意事項
- 入力内容は一時的にのみ処理され、サーバーに保存されません（履歴DBはローカルのみ）
- 個人情報・機密情報の入力はご注意ください
- .envファイルは絶対にgitにコミットしないでください

---

## 設定ファイル（config.yaml）

- サンプル: `config.sample.yaml` を参照
- `ai.openai_api_key` : OpenAI APIのAPIキー
- `ai.summarizer_engine` : "openai"（現状対応）/"gemini"（将来対応）
- `tts.engine` : "gtts" または "google_cloud"
- `tts.lang` : 音声合成言語（デフォルト: ja）

---

## 依存ライブラリ

- openai
- google-cloud-texttospeech
- python-dotenv
- requests
- gtts
- PyYAML
- beautifulsoup4
- readability-lxml
- pillow
- pytesseract
- streamlit

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

---

## 未実装機能・今後のロードマップ
- Gemini API連携による本格要約（現状は未実装）
- CleanShot OCR連携
- VOICEVOX等のTTSエンジン追加
- PDF/WAV等の多様な出力フォーマット
- CLIコマンド`aisum`の提供
- 履歴保存・自動削除機能の強化

---

## 仮想環境・APIキー・E2E/CI/CD運用手順

### 1. 仮想環境の作成・有効化
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. APIキー・認証情報の設定
- `.env` または環境変数で以下を設定
  - `OPENAI_API_KEY` : OpenAI GPT-4.1-nano用
  - `GOOGLE_API_KEY` : Gemini API用
  - `GOOGLE_APPLICATION_CREDENTIALS` : Google Cloud TTS用サービスアカウントJSONパス
- 例：
```env
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIza...
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account.json
```

### 3. APIスイッチ・本番/ダミー切替
- 要約API: `SUMMARIZER_ENGINE=openai|gemini|dummy`、`USE_DUMMY_API=true|false`
- TTS: `TTS_ENGINE=gtts|google_cloud`
- DB: `NOTEBOOKLM_DB_PATH=...` でDBファイル切替

### 4. E2E/CI/CD運用
- GitHub Actionsで自動テスト・E2E・カバレッジ・Slack通知
- 本番API用secrets例：
  - `OPENAI_API_KEY`、`GOOGLE_API_KEY`、`GOOGLE_APPLICATION_CREDENTIALS` をGitHubリポジトリのSecretsに登録
- cron実行時は本番APIでE2Eテスト、push/PR時はダミーAPIで安全に検証

--- 