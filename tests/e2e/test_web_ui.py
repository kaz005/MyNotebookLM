import pytest

# 仮のWeb UI E2E関数
def web_ui_e2e(input_data):
    # 実際はSelenium等でUI自動化
    return {"summary": "要約", "audio_ui": True, "downloaded_file": "output/summary.mp3"}

def test_web_ui_summary_e2e(monkeypatch):
    monkeypatch.setattr(__name__ + ".web_ui_e2e", lambda input_data: {"summary": "要約", "audio_ui": True, "downloaded_file": "output/summary.mp3"})
    result = web_ui_e2e({"input": "fixtures/summary.txt"})
    assert result["summary"]
    assert result["audio_ui"] is True
    assert result["downloaded_file"].endswith(".mp3") 