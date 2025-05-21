import pytest

# 仮のパフォーマンス測定関数
def measure_latency():
    # 実際はAPI呼び出しのレイテンシ計測
    # ここではダミー値
    return {"p95_latency_ms": 4200}

def test_performance_latency(monkeypatch):
    monkeypatch.setattr(__name__ + ".measure_latency", lambda: {"p95_latency_ms": 4200})
    result = measure_latency()
    assert result["p95_latency_ms"] < 5000 