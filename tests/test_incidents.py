import json

import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture()
def api():
    return APIClient()


def test_create_incident_201_and_defaults(api):
    payload = {"text": "Самокат оффлайн", "source": "operator"}
    resp = api.post(
        "/api/v1/incidents/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == 201, resp.content

    data = resp.json()
    assert data["id"] > 0
    assert data["text"] == payload["text"]
    assert data["source"] == payload["source"]
    assert data["status"] == "new"
    assert "created_at" in data


def test_list_filter_by_status(api):
    for status in ("new", "investigating", "resolved"):
        payload = {"text": f"{status}", "source": "partner", "status": status}
        r = api.post(
            "/api/v1/incidents/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        assert r.status_code == 201

    r = api.get("/api/v1/incidents/?status=new")
    assert r.status_code == 200

    items = r.json()
    assert all(x["status"] == "new" for x in items)
    assert len(items) == 1


def test_update_status_ok_and_404(api):
    r = api.post(
        "/api/v1/incidents/",
        data=json.dumps({"text": "X", "source": "partner", "status": "new"}),
        content_type="application/json",
    )
    assert r.status_code == 201

    item_id = r.json()["id"]

    # ok update
    r = api.patch(
        f"/api/v1/incidents/{item_id}/status/",
        data=json.dumps({"status": "resolved"}),
        content_type="application/json",
    )
    assert r.status_code == 200
    assert r.json()["status"] == "resolved"

    # 404
    r = api.patch(
        "/api/v1/incidents/999999/status/",
        data=json.dumps({"status": "resolved"}),
        content_type="application/json",
    )
    assert r.status_code == 404
