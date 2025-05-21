import pytest
from notebooklm import extractor
from notebooklm import tts

# 無効なURL

def test_err_invalid_url():
    with pytest.raises(Exception):
        extractor.extract_article_text("http://invalid-url")

# OCR失敗（文字なし画像）

def test_err_ocr_fail():
    with pytest.raises(Exception):
        extractor.extract_article_text("fixtures/blank_image.png")

# TTSタイムアウト（モックで例外発生を模擬）

def test_err_tts_timeout(mocker):
    mocker.patch("notebooklm.tts.gTTS.save", side_effect=TimeoutError("TTS APIタイムアウト"))
    with pytest.raises(TimeoutError):
        tts.synthesize_speech("テスト音声", {'tts': {'lang': 'ja'}}) 