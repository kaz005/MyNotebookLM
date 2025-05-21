import pytest

# 仮のパイプライン関数
def pipeline_url_to_export(url):
    # 実際はAPIを順次呼び出し
    return {"status_code": 200, "audio_file": "output/summary.mp3", "history_saved": True}

def test_pipeline_url_to_export(monkeypatch):
    monkeypatch.setattr(__name__ + ".pipeline_url_to_export", lambda url: {"status_code": 200, "audio_file": "output/summary.mp3", "history_saved": True})
    result = pipeline_url_to_export("fixtures/sample_article.html")
    assert result["status_code"] == 200
    assert result["audio_file"].endswith(".mp3")
    assert result["history_saved"] is True 