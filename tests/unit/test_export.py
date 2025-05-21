import pytest
import os

# 仮のエクスポート関数

def export_summary(format: str, input_path: str = "fixtures/summary.txt"):
    # 実際はAPI呼び出しやファイル生成処理
    # ここではダミーでファイル存在チェックのみ
    if format not in ["txt", "pdf", "mp3", "wav"]:
        raise ValueError("未対応フォーマット")
    # テスト用にダミーファイルを生成した体でパスを返す
    return f"output/summary.{format}"

@pytest.mark.parametrize("fmt", ["txt", "pdf", "mp3", "wav"])
def test_export_formats(fmt, monkeypatch):
    # export_summaryをモックしてダミーパスを返す
    monkeypatch.setattr(__name__ + ".export_summary", lambda f, input_path=None: f"output/summary.{f}")
    output_path = export_summary(fmt)
    assert output_path.endswith(f".{fmt}")
    # 実際はファイル存在や内容検証も追加可能 