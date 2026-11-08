"""Integration test alur utama Phase 6 (P6-22).

Menguji register–login–cari–detail–preferensi–bookmark–feed–event–hapus data,
otorisasi admin, serta validitas kontrak OpenAPI.
"""

from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from openapi_spec_validator import validate
from openapi_spec_validator.readers import read_from_filename

from app.database import SessionLocal
from app.main import app
from app.models import InteractionEvent, User

client = TestClient(app)

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "AdminPass123!"


@pytest.fixture(scope="module")
def admin_token() -> str:
    response = client.post(
        "/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture()
def user_account():
    email = f"test-{uuid4().hex}@example.com"
    password = "TestPass123!"
    response = client.post(
        "/auth/register",
        json={"email": email, "password": password, "full_name": "Test User"},
    )
    assert response.status_code == 201
    token = response.json()["access_token"]

    yield {"email": email, "password": password, "token": token}

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            db.delete(user)
            db.commit()
    finally:
        db.close()


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


EMPTY_PREFERENCES = {
    "categories": [],
    "locations": [],
    "employment_types": [],
    "experience_levels": [],
    "keywords": [],
}


def test_search_and_detail() -> None:
    response = client.get("/api/jobs/search", params={"q": "data analyst", "limit": 5})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] > 0
    assert len(body["results"]) <= 5
    assert all(result["match_level"] != "Standar" for result in body["results"])
    assert all(result["reason"] for result in body["results"])
    assert all("score" not in result for result in body["results"])
    assert all("employment_type" in result for result in body["results"])

    filtered = client.get(
        "/api/jobs/search",
        params={"q": "data analyst", "employment_type": "Full-Time", "limit": 5},
    )
    assert filtered.status_code == 200
    assert all(
        "full-time" in (result["employment_type"] or "").lower()
        for result in filtered.json()["results"]
    )

    job_id = body["results"][0]["job_id"]
    detail = client.get(f"/api/jobs/{job_id}")
    assert detail.status_code == 200
    detail_body = detail.json()
    assert detail_body["job_id"] == job_id
    assert detail_body["title"]
    assert isinstance(detail_body["skills"], list)
    assert "employment_type" in detail_body
    assert "experience_level" in detail_body
    assert detail_body["is_active"] is True
    assert detail_body["source"]


def test_search_empty_state() -> None:
    response = client.get(
        "/api/jobs/search", params={"q": "zzzz-tidak-ada-lowongan"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 0
    assert body["results"] == []
    assert "message" in body


def test_main_user_flow(user_account) -> None:
    token = user_account["token"]
    headers = auth_headers(token)

    # Login dengan kredensial benar.
    login = client.post(
        "/auth/login",
        json={"email": user_account["email"], "password": user_account["password"]},
    )
    assert login.status_code == 200

    # Login dengan kredensial salah menghasilkan pesan generik.
    bad_login = client.post(
        "/auth/login",
        json={"email": user_account["email"], "password": "SalahPass123!"},
    )
    assert bad_login.status_code == 401
    assert bad_login.json()["detail"] == "Invalid credentials"

    # Preferensi awal kosong, lalu diperbarui.
    initial_prefs = client.get("/api/me/preferences", headers=headers)
    assert initial_prefs.status_code == 200
    assert initial_prefs.json()["preferences"] == EMPTY_PREFERENCES

    payload = {
        "categories": ["Data & Analitik"],
        "locations": ["Remote"],
        "employment_types": ["Full-Time"],
        "experience_levels": ["Mid-Level"],
        "keywords": ["data analyst"],
    }
    updated = client.put("/api/me/preferences", headers=headers, json=payload)
    assert updated.status_code == 200
    assert updated.json()["preferences"] == payload

    # Bookmark idempoten: simpan dua kali hanya menghasilkan satu baris.
    first = client.post(
        "/api/me/bookmarks", headers=headers, json={"job_id": "syn-id-0096"}
    )
    assert first.status_code == 201
    assert first.json()["created"] is True

    second = client.post(
        "/api/me/bookmarks", headers=headers, json={"job_id": "syn-id-0096"}
    )
    assert second.status_code == 200
    assert second.json()["created"] is False

    bookmarks = client.get("/api/me/bookmarks", headers=headers)
    assert bookmarks.status_code == 200
    assert bookmarks.json()["count"] == 1
    assert bookmarks.json()["items"][0]["title"]

    # Feed mengecualikan bookmark dan memakai sumber personalisasi.
    feed = client.get("/api/me/recommendations", headers=headers)
    assert feed.status_code == 200
    feed_body = feed.json()
    assert feed_body["results"]
    assert all(item["job_id"] != "syn-id-0096" for item in feed_body["results"])
    assert feed_body["results"][0]["source"] == "profile"
    assert feed_body["results"][0]["reason"]

    # Event normal tidak boleh ditandai simulasi oleh pengguna biasa.
    event = client.post(
        "/api/events",
        headers=headers,
        json={
            "job_id": "syn-id-0096",
            "event_type": "view",
            "is_simulated": True,
        },
    )
    assert event.status_code == 200
    assert event.json()["is_simulated"] is False

    # Hapus bookmark dua kali tetap 204.
    assert (
        client.delete("/api/me/bookmarks/syn-id-0096", headers=headers).status_code
        == 204
    )
    assert (
        client.delete("/api/me/bookmarks/syn-id-0096", headers=headers).status_code
        == 204
    )

    # Hapus seluruh data pengguna, idempoten.
    assert client.delete("/api/me/data", headers=headers).status_code == 204
    assert (
        client.get("/api/me/preferences", headers=headers).json()["preferences"]
        == EMPTY_PREFERENCES
    )
    assert client.get("/api/me/bookmarks", headers=headers).json()["count"] == 0
    assert client.delete("/api/me/data", headers=headers).status_code == 204


def test_admin_authorization(admin_token: str, user_account) -> None:
    user_response = client.get(
        "/api/admin/eval/summary", headers=auth_headers(user_account["token"])
    )
    assert user_response.status_code == 403

    admin_response = client.get(
        "/api/admin/eval/summary", headers=auth_headers(admin_token)
    )
    assert admin_response.status_code == 200
    body = admin_response.json()
    assert "queries" in body
    assert "judgments" in body
    assert "runs" in body
    assert body["config_hash"]
    assert body["dataset_hash"]

    simulated = client.post(
        "/api/events",
        headers=auth_headers(admin_token),
        json={
            "job_id": "syn-id-0096",
            "event_type": "click",
            "is_simulated": True,
        },
    )
    assert simulated.status_code == 200
    assert simulated.json()["is_simulated"] is True

    db = SessionLocal()
    try:
        db.query(InteractionEvent).filter(
            InteractionEvent.id == simulated.json()["event_id"]
        ).delete()
        db.commit()
    finally:
        db.close()


def test_bookmark_ownership(user_account) -> None:
    other_email = f"other-{uuid4().hex}@example.com"
    other_password = "OtherPass123!"
    registration = client.post(
        "/auth/register",
        json={"email": other_email, "password": other_password},
    )
    assert registration.status_code == 201
    other_token = registration.json()["access_token"]

    try:
        created = client.post(
            "/api/me/bookmarks",
            headers=auth_headers(user_account["token"]),
            json={"job_id": "syn-id-0097"},
        )
        assert created.status_code == 201

        other_list = client.get(
            "/api/me/bookmarks", headers=auth_headers(other_token)
        )
        assert other_list.status_code == 200
        assert other_list.json()["count"] == 0

        # Hapus dari akun lain bersifat idempoten dan tidak menghapus milik pemilik.
        assert (
            client.delete(
                "/api/me/bookmarks/syn-id-0097",
                headers=auth_headers(other_token),
            ).status_code
            == 204
        )
        owner_list = client.get(
            "/api/me/bookmarks", headers=auth_headers(user_account["token"])
        )
        assert owner_list.json()["count"] == 1
    finally:
        client.delete(
            "/api/me/data", headers=auth_headers(user_account["token"])
        )
        client.delete("/api/me/data", headers=auth_headers(other_token))
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == other_email).first()
            if user:
                db.delete(user)
                db.commit()
        finally:
            db.close()


def test_openapi_spec_is_valid() -> None:
    spec, base_uri = read_from_filename(Path("docs/api/openapi.yaml"))
    validate(spec)
    assert base_uri
