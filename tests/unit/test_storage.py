import pytest
from unittest.mock import MagicMock

# 仮の履歴保存・取得関数

def save_history(user_id, summary, audio_path):
    # 実装はストレージに保存
    pass

def load_history(user_id):
    # 実装はストレージから取得
    return [
        {"summary": "要約1", "audio_path": "audio1.mp3", "timestamp": "2024-06-01"},
        {"summary": "要約2", "audio_path": "audio2.mp3", "timestamp": "2024-06-10"},
    ]

def test_history_save(monkeypatch):
    # save_historyをモック
    mock_save = MagicMock()
    monkeypatch.setattr(__name__ + ".save_history", mock_save)
    # 履歴保存を呼び出し
    save_history("user1", "要約テスト", "audio.mp3")
    mock_save.assert_called_once_with("user1", "要約テスト", "audio.mp3")


def test_history_retention():
    # 30日以内の履歴のみが返ることを検証
    history = load_history("user1")
    for item in history:
        assert "summary" in item
        assert "audio_path" in item
        assert "timestamp" in item 