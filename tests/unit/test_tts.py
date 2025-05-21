import pytest
from notebooklm import tts
import os

def test_tts_synthesize_speech_speed_pitch_voice(monkeypatch):
    # gTTSは速度・ピッチ・声種未対応だが、将来拡張用にパラメータを渡してもエラーにならないことを確認
    text = "パラメータテスト"
    config = {'tts': {'lang': 'ja', 'speed': 1.2, 'pitch': 2, 'voice_type': 'male'}}
    # gTTS.saveをモックしてファイル生成をシミュレート
    class DummyTTS:
        def __init__(self, text, lang):
            self.text = text
            self.lang = lang
        def save(self, path):
            with open(path, 'wb') as f:
                f.write(b'dummy')
    monkeypatch.setattr('gtts.gTTS', DummyTTS)
    output_path = tts.synthesize_speech(text, config)
    assert os.path.exists(output_path)
    os.remove(output_path)
    # パラメータ違いでも同様に生成される
    config2 = {'tts': {'lang': 'ja', 'speed': 0.8, 'pitch': -2, 'voice_type': 'female'}}
    output_path2 = tts.synthesize_speech(text, config2)
    assert os.path.exists(output_path2)
    os.remove(output_path2)

def test_tts_google_cloud(monkeypatch):
    """
    Google Cloud TTS本番APIのE2Eテスト。
    GOOGLE_APPLICATION_CREDENTIALS未設定時はスキップ。
    """
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        pytest.skip("GOOGLE_APPLICATION_CREDENTIALS未設定のためスキップ")
    monkeypatch.setenv("TTS_ENGINE", "google_cloud")
    config = {'tts': {'lang': 'ja', 'engine': 'google_cloud'}}
    text = "これはGoogle Cloud TTSのテスト音声です。"
    output_path = tts.synthesize_speech(text, config)
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 1000  # 1KB以上のMP3が生成される
    os.remove(output_path) 