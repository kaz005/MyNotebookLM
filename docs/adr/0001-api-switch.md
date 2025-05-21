# ADR: 0001 APIスイッチ機構設計

## 概要
Gemini要約APIの「ダミー（スタブ）⇄本番API」切替を柔軟かつ安全に行うための設計方針を記録する。

## 決定事項
- API呼び出し層は**Factoryパターン/DI（依存性注入）方式**で実装する。
- 環境変数（例: `USE_DUMMY_API=true`）または`config.yaml`の設定値（`ai.use_dummy_api: true`）で切替可能とする。
- SDK版・REST版の両方に対応し、**共通インターフェース（summarize(text: str) -> str）**を提供する。
- テスト・CIでは常にダミーAPIを利用し、外部APIコスト・障害リスクを排除する。
- 本番運用時は明示的に本番APIを有効化する（デフォルトはダミー）。

## 背景
- テスト容易性・CI自動化・APIコスト最適化・障害耐性向上のため、API切替機構が必須。
- 実装者・運用者が明示的に切替状態を把握できるよう、設定値・ログに状態を出力する。

## 実装例
```python
# summarizer_factory.py
import os
from .summarizer_dummy import DummySummarizer
from .summarizer_gemini import GeminiSummarizer

def get_summarizer():
    use_dummy = os.getenv("USE_DUMMY_API", "false").lower() == "true"
    if use_dummy:
        return DummySummarizer()
    else:
        return GeminiSummarizer()
```

## メリット
- テスト・CIで外部APIを呼ばずに済む
- 本番API障害時もダミーで継続運用可能
- 実装の拡張性（SDK/REST/他API追加）

## デメリット
- 切替状態の管理ミスによる誤運用リスク（ログ・UIで明示）

## 参考
- [Factoryパターン（Python）](https://refactoring.guru/ja/design-patterns/factory-method/python/example)
- [依存性注入（DI）](https://qiita.com/yuji38kwmt/items/2e8e6e6e6e6e6e6e6e6e) 