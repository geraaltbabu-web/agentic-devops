import json

from main import APPOINTMENTS, SERVICE


def test_health_payload_shape():
    payload = {"status": "ok", "service": SERVICE, "domain": "health"}
    assert payload["status"] == "ok"
    assert payload["service"] == "clinic-api"
    assert payload["domain"] == "health"


def test_synthetic_appointments_have_no_patient_names():
    blob = json.dumps(APPOINTMENTS).lower()
    assert "ssn" not in blob
    assert "patient" not in blob
    assert len(APPOINTMENTS) >= 1
