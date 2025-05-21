import os
import tempfile
import shutil
import pytest
from notebooklm import db
import datetime

@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    # テスト用一時DBファイル
    tmpdir = tempfile.mkdtemp()
    db_path = os.path.join(tmpdir, "test_history.db")
    monkeypatch.setenv("NOTEBOOKLM_DB_PATH", db_path)
    db.init_db()  # テーブルを初期化
    yield
    shutil.rmtree(tmpdir)

def test_save_and_load_history():
    db.save_history("user1", "summary1", "audio1.mp3", tag="A")
    db.save_history("user1", "summary2", "audio2.mp3", tag="B")
    history = db.load_history("user1")
    assert len(history) == 2
    assert history[0]["summary"] == "summary1"
    assert history[1]["audio_path"] == "audio2.mp3"

def test_delete_history_by_tag():
    db.save_history("user2", "summary3", "audio3.mp3", tag="X")
    db.save_history("user2", "summary4", "audio4.mp3", tag="Y")
    db.delete_history_by_tag("user2", "X")
    history = db.load_history("user2")
    assert len(history) == 1
    assert history[0]["tag"] == "Y"

def test_enforce_capacity_limit():
    for i in range(5):
        db.save_history("user3", f"summary{i}", f"audio{i}.mp3")
    db.enforce_capacity_limit("user3", max_items=3)
    history = db.load_history("user3")
    assert len(history) == 3

def test_delete_old_history():
    now = datetime.datetime.now()
    old = (now - datetime.timedelta(days=31)).isoformat()
    db.save_history("user4", "old_summary", "audio_old.mp3", timestamp=old)
    db.save_history("user4", "new_summary", "audio_new.mp3")
    db.delete_old_history("user4", days=30)
    history = db.load_history("user4")
    assert len(history) == 1
    assert history[0]["summary"] == "new_summary" 