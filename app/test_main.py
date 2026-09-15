import json


def test_health_payload_shape():
    payload = json.loads('{"status":"ok","service":"agentic-devops-demo"}')
    assert payload["status"] == "ok"
    assert payload["service"] == "agentic-devops-demo"
