import pytest
import summarizer
import extractor

# 正常系: 有効なニュース記事のURL
# ここではextract_article_textがファイルパスを受け取れる前提でテスト

def test_input_url_valid():
    text = extractor.extract_article_text("fixtures/sample_article.html")
    assert isinstance(text, str)
    assert len(text) >= 100

# 異常系: 空入力

def test_input_empty():
    with pytest.raises(ValueError):
        summarizer.summarize_article("", {'ai': {'summarization_prompt': '要約'}})

# 異常系: 最大長+1

def test_input_max_length_plus1():
    with open("fixtures/too_long_text.txt", encoding="utf-8") as f:
        text = f.read()
    with pytest.raises(ValueError):
        summarizer.summarize_article(text, {'ai': {'summarization_prompt': '要約'}})

# 異常系: 未対応画像形式（TIFF）

def test_input_unsupported_image_format():
    with pytest.raises(ValueError):
        extractor.extract_article_text("fixtures/sample_image.tiff")

# 異常系: None

def test_input_none():
    with pytest.raises(ValueError):
        summarizer.summarize_article(None, {'ai': {'summarization_prompt': '要約'}})

# 異常系: 必須パラメータ欠落

def test_input_missing_param():
    with pytest.raises(TypeError):
        summarizer.summarize_article() 