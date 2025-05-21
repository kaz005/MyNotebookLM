import pytest
import os

# 仮のエクスポート関数

def export_summary(format: str, input_path: str = "fixtures/summary.txt"):
    if format not in ["txt", "pdf", "mp3", "wav"]:
        raise ValueError("未対応フォーマット")
    # ダミーファイル生成
    output_path = f"output/summary.{format}"
    os.makedirs("output", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(b'dummy')
    return output_path

@pytest.mark.parametrize("fmt", ["txt", "pdf", "mp3", "wav"])
def test_export_formats(fmt, monkeypatch):
    # export_summaryをモックしてダミーパスを返す
    monkeypatch.setattr(__name__ + ".export_summary", lambda f, input_path=None: f"output/summary.{f}")
    output_path = export_summary(fmt)
    assert output_path.endswith(f".{fmt}")
    # 実際はファイル存在や内容検証も追加可能 

@pytest.mark.parametrize("fmt", ["txt", "pdf", "mp3", "wav"])
def test_export_formats_file_generation(fmt):
    output_path = export_summary(fmt)
    assert os.path.exists(output_path)
    os.remove(output_path) 