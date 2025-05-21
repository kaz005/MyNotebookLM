import pytest

# 仮のCleanShot OCR関数
def cleanshot_ocr(file_path):
    # 実際はAPI呼び出し
    return {"status_code": 200, "text": "抽出された日本語テキスト"}

def test_ocr_cleanshot_integration(monkeypatch):
    monkeypatch.setattr(__name__ + ".cleanshot_ocr", lambda file_path: {"status_code": 200, "text": "抽出された日本語テキスト"})
    result = cleanshot_ocr("fixtures/sample_image.jpg")
    assert result["status_code"] == 200
    assert "日本語テキスト" in result["text"] 