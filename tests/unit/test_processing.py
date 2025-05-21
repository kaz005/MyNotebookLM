import pytest
from notebooklm import summarizer
import yaml
import os

@pytest.mark.parametrize("length", [50, 100, 200, 400])
def test_summarization_length(monkeypatch, length):
    # 本番APIを強制
    monkeypatch.setenv("USE_DUMMY_API", "false")
    monkeypatch.setenv("SUMMARIZER_ENGINE", "openai")
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY未設定のためスキップ")
    with open("fixtures/long_text.txt", encoding="utf-8") as f:
        article_text = f.read()
    config = {'ai': {'summarization_prompt': '要約してください。'}}
    summary = summarizer.summarize_article(article_text, config, length=length)
    assert abs(len(summary) - length) < 0.1 * length, f"要約長が指定値±10%を超えています: {len(summary)} vs {length}"

@pytest.mark.parametrize("level", ["gist", "standard", "detailed"])
def test_summarization_detail_level(monkeypatch, level):
    monkeypatch.setenv("USE_DUMMY_API", "false")
    monkeypatch.setenv("SUMMARIZER_ENGINE", "openai")
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY未設定のためスキップ")
    with open("fixtures/long_text.txt", encoding="utf-8") as f:
        article_text = f.read()
    config = {'ai': {'summarization_prompt': f'要約({level})してください。'}}
    summary = summarizer.summarize_article(article_text, config, length=200)
    assert isinstance(summary, str) and len(summary) > 0

def test_summarization_dummy_fallback(monkeypatch):
    os.environ["USE_DUMMY_API"] = "true"
    article_text = "これは要約対象のテスト用テキストです。"
    config = {'ai': {'summarization_prompt': '要約してください。'}}
    summary = summarizer.summarize_article(article_text, config, length=50)
    assert summary.startswith("[要約ダミー]"), f"ダミー要約が返るべき: {summary}"
    del os.environ["USE_DUMMY_API"]

def test_summarization_openai(monkeypatch):
    """
    OpenAI gpt-4.1-nanoによる要約APIのE2Eテスト。
    OPENAI_API_KEYが設定されていない場合はスキップ。
    """
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEYが未設定のためスキップ")
    article_text = """
    Pythonは、汎用の高水準プログラミング言語であり、可読性の高いコードを書くことができる。多くの分野で利用されており、AI、Web開発、データ分析、教育など幅広い用途がある。シンプルな文法と豊富なライブラリが特徴である。
    """
    config = {'ai': {'summarization_prompt': '要約してください。'}}
    monkeypatch.setenv("USE_DUMMY_API", "false")
    monkeypatch.setenv("SUMMARIZER_ENGINE", "openai")
    summary = summarizer.summarize_article(article_text, config, length=60)
    assert isinstance(summary, str)
    assert len(summary) <= 70  # 多少の誤差を許容
    assert "Python" in summary

def test_summarization_gemini(monkeypatch):
    """
    Gemini APIによる要約APIのE2Eテスト。
    GOOGLE_API_KEYが設定されていない場合はスキップ。
    """
    if not os.getenv("GOOGLE_API_KEY"):
        pytest.skip("GOOGLE_API_KEYが未設定のためスキップ")
    article_text = """
    生成AIは、膨大なデータを学習し、人間のように自然な文章や画像を生成できる技術です。ビジネスや教育、クリエイティブ分野で活用が進んでいます。
    """
    config = {'ai': {'summarization_prompt': '要約してください。'}}
    monkeypatch.setenv("USE_DUMMY_API", "false")
    monkeypatch.setenv("SUMMARIZER_ENGINE", "gemini")
    summary = summarizer.summarize_article(article_text, config, length=60)
    assert isinstance(summary, str)
    assert len(summary) <= 70  # 多少の誤差を許容
    assert "生成AI" in summary 