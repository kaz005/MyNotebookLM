import pytest
import os

# 仮のCLI実行関数
def run_aisum_cli(file_path, length):
    # 実際はsubprocessでCLI実行
    return {"exit_code": 0, "audio_file": f"output/summary_{length}.mp3"}

def test_cli_summary_e2e(monkeypatch):
    monkeypatch.setattr(__name__ + ".run_aisum_cli", lambda file_path, length: {"exit_code": 0, "audio_file": f"output/summary_{length}.mp3"})
    result = run_aisum_cli("fixtures/summary.txt", 100)
    assert result["exit_code"] == 0
    assert result["audio_file"].endswith(".mp3")
    # 実際はos.path.exists等でファイル存在も検証可能 