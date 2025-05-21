import pytest
import summarizer
import yaml

@pytest.mark.parametrize("length", [50, 100, 200, 400])
def test_summarization_length(length):
    # テスト用の長文テキストをfixturesから読み込む
    with open("fixtures/long_text.txt", encoding="utf-8") as f:
        article_text = f.read()
    # 仮のconfig（プロンプトのみ）
    config = {'ai': {'summarization_prompt': '要約してください。'}}
    summary = summarizer.summarize_article(article_text, config, length=length)
    assert abs(len(summary) - length) < 0.1 * length, f"要約長が指定値±10%を超えています: {len(summary)} vs {length}"

@pytest.mark.parametrize("level", ["gist", "standard", "detailed"])
def test_summarization_detail_level(level):
    with open("fixtures/long_text.txt", encoding="utf-8") as f:
        article_text = f.read()
    config = {'ai': {'summarization_prompt': f'要約してください。詳細度: {level}'}}
    summary = summarizer.summarize_article(article_text, config, length=100)
    assert isinstance(summary, str)
    # ダミー実装では同じ結果になるが、将来は内容差分をassertする 