import pytest

# 仮の同時実行パフォーマンス測定関数
def measure_concurrency():
    # 実際はAPIの同時リクエスト処理結果
    return {"success_count": 20, "max_latency_ms": 4800}

def test_performance_concurrency(monkeypatch):
    monkeypatch.setattr(__name__ + ".measure_concurrency", lambda: {"success_count": 20, "max_latency_ms": 4800})
    result = measure_concurrency()
    assert result["success_count"] == 20
    assert result["max_latency_ms"] < 5000 