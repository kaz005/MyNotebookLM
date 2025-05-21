import sqlite3
import os
import datetime
from typing import Optional, List, Dict

# SQLite用の初期化

def init_db():
    db_path = os.environ.get("NOTEBOOKLM_DB_PATH", "notebooklm_history.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            summary TEXT,
            audio_path TEXT,
            tag TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# 履歴保存

def save_history(user_id: str, summary: str, audio_path: str, tag: Optional[str] = None, timestamp: Optional[str] = None):
    db_path = os.environ.get("NOTEBOOKLM_DB_PATH", "notebooklm_history.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    if timestamp is None:
        c.execute('''INSERT INTO history (user_id, summary, audio_path, tag) VALUES (?, ?, ?, ?)''',
                  (user_id, summary, audio_path, tag))
    else:
        c.execute('''INSERT INTO history (user_id, summary, audio_path, tag, timestamp) VALUES (?, ?, ?, ?, ?)''',
                  (user_id, summary, audio_path, tag, timestamp))
    conn.commit()
    conn.close()

# 履歴取得

def load_history(user_id: str) -> List[Dict]:
    db_path = os.environ.get("NOTEBOOKLM_DB_PATH", "notebooklm_history.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''SELECT summary, audio_path, tag, timestamp FROM history WHERE user_id = ? ORDER BY id ASC''', (user_id,))
    rows = c.fetchall()
    conn.close()
    result = []
    for row in rows:
        result.append({
            "summary": row[0],
            "audio_path": row[1],
            "tag": row[2],
            "timestamp": row[3]
        })
    return result

# タグ指定で履歴削除

def delete_history_by_tag(user_id: str, tag: str):
    db_path = os.environ.get("NOTEBOOKLM_DB_PATH", "notebooklm_history.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''DELETE FROM history WHERE user_id = ? AND tag = ?''', (user_id, tag))
    conn.commit()
    conn.close()

# 容量超過時の自動削除

def enforce_capacity_limit(user_id: str, max_items: int = 100):
    db_path = os.environ.get("NOTEBOOKLM_DB_PATH", "notebooklm_history.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # 残すべき最新max_items件のidを取得
    c.execute('''SELECT id FROM history WHERE user_id = ? ORDER BY id DESC LIMIT ?''', (user_id, max_items))
    ids = [row[0] for row in c.fetchall()]
    if ids:
        # それより古いidを削除
        min_id = min(ids)
        c.execute('''DELETE FROM history WHERE user_id = ? AND id < ?''', (user_id, min_id))
    conn.commit()
    conn.close()

# 30日超の自動削除

def delete_old_history(user_id: str, days: int = 30):
    db_path = os.environ.get("NOTEBOOKLM_DB_PATH", "notebooklm_history.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    threshold = (datetime.datetime.now() - datetime.timedelta(days=days)).isoformat()
    c.execute('''DELETE FROM history WHERE user_id = ? AND timestamp < ?''', (user_id, threshold))
    conn.commit()
    conn.close()

# DB初期化（起動時に呼ぶ想定）
init_db() 