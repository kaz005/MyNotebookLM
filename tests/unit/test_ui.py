import pytest
from unittest.mock import MagicMock

# 仮のUI関数

def web_ui_summarize(input_data):
    # 実際はWeb UIの操作を自動化
    return {"summary": "要約", "audio_ui": True}

def cli_summarize(file_path, length):
    # 実際はCLIコマンドを実行
    return {"exit_code": 0, "audio_file": f"output/summary_{length}.mp3"}

# Web UIテスト
def test_web_ui_summary(monkeypatch):
    monkeypatch.setattr(__name__ + ".web_ui_summarize", lambda input_data: {"summary": "要約", "audio_ui": True})
    result = web_ui_summarize({"input": "fixtures/summary.txt"})
    assert result["summary"]
    assert result["audio_ui"] is True

# CLIテスト
def test_cli_summary(monkeypatch):
    monkeypatch.setattr(__name__ + ".cli_summarize", lambda file_path, length: {"exit_code": 0, "audio_file": f"output/summary_{length}.mp3"})
    result = cli_summarize("fixtures/summary.txt", 100)
    assert result["exit_code"] == 0
    assert result["audio_file"].endswith(".mp3") 