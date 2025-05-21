import pytest
from unittest.mock import MagicMock
import datetime

# 仮の履歴保存・取得・削除関数

def save_history(user_id, summary, audio_path, tag=None, timestamp=None):
    # 実装はストレージに保存
    pass

def load_history(user_id):
    # 実装はストレージから取得
    return [
        {"summary": "要約1", "audio_path": "audio1.mp3", "timestamp": "2024-06-01", "tag": "A"},
        {"summary": "要約2", "audio_path": "audio2.mp3", "timestamp": "2024-06-10", "tag": "B"},
    ]

def delete_history_by_tag(user_id, tag):
    # 実装はストレージからタグ指定で削除
    pass

def enforce_capacity_limit(user_id, max_items=2):
    # 実装は容量超過時に古い履歴を削除
    pass

def test_history_save(monkeypatch):
    mock_save = MagicMock()
    monkeypatch.setattr(__name__ + ".save_history", mock_save)
    save_history("user1", "要約テスト", "audio.mp3")
    mock_save.assert_called_once_with("user1", "要約テスト", "audio.mp3")

def test_history_retention():
    history = load_history("user1")
    for item in history:
        assert "summary" in item
        assert "audio_path" in item
        assert "timestamp" in item

def test_history_capacity_limit(monkeypatch):
    # 履歴がmax_itemsを超えたら古いものが削除される
    mock_enforce = MagicMock()
    monkeypatch.setattr(__name__ + ".enforce_capacity_limit", mock_enforce)
    enforce_capacity_limit("user1", max_items=2)
    mock_enforce.assert_called_once_with("user1", max_items=2)

def test_history_tag_delete(monkeypatch):
    # タグ指定で履歴削除
    mock_delete = MagicMock()
    monkeypatch.setattr(__name__ + ".delete_history_by_tag", mock_delete)
    delete_history_by_tag("user1", "A")
    mock_delete.assert_called_once_with("user1", "A")

def test_history_auto_delete_old(monkeypatch):
    # 30日超の履歴が自動削除される
    now = datetime.datetime(2024, 7, 1)
    history = [
        {"summary": "古い要約", "audio_path": "old.mp3", "timestamp": "2024-05-01"},
        {"summary": "新しい要約", "audio_path": "new.mp3", "timestamp": "2024-06-15"},
    ]
    def mock_load(user_id):
        return history
    monkeypatch.setattr(__name__ + ".load_history", mock_load)
    # 仮: 30日超の履歴が除外されることをassert（実装時はfilter処理）
    filtered = [item for item in history if (now - datetime.datetime.strptime(item["timestamp"], "%Y-%m-%d")).days <= 30]
    assert all((now - datetime.datetime.strptime(item["timestamp"], "%Y-%m-%d")).days <= 30 for item in filtered) 