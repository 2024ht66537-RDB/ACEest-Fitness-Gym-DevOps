import pytest
import json
import sys
import os

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, members, classes


# ── Fixtures ──────────────────────────────────────────────────────────────────
@pytest.fixture
def client():
    """Create a fresh test client and reset shared state before each test."""
    app.config["TESTING"] = True
    members.clear()
    for c in classes:
        c["enrolled"] = 0
    with app.test_client() as client:
        yield client


# ── Home & Health ─────────────────────────────────────────────────────────────
class TestHome:
    def test_home_returns_200(self, client):
        res = client.get("/")
        assert res.status_code == 200

    def test_home_contains_welcome(self, client):
        res = client.get("/")
        data = json.loads(res.data)
        assert "ACEest Fitness" in data["message"]

    def test_home_status_operational(self, client):
        res = client.get("/")
        data = json.loads(res.data)
        assert data["status"] == "operational"


class TestHealth:
    def test_health_returns_200(self, client):
        res = client.get("/health")
        assert res.status_code == 200

    def test_health_status_healthy(self, client):
        res = client.get("/health")
        data = json.loads(res.data)
        assert data["status"] == "healthy"


# ── Members ───────────────────────────────────────────────────────────────────
class TestGetMembers:
    def test_empty_members_list(self, client):
        res = client.get("/members")
        data = json.loads(res.data)
        assert res.status_code == 200
        assert data["members"] == []
        assert data["total"] == 0

    def test_members_count_after_add(self, client):
        client.post("/members", json={"name": "Ravi", "age": 25, "plan": "basic"})
        res = client.get("/members")
        data = json.loads(res.data)
        assert data["total"] == 1


class TestAddMember:
    def test_add_valid_member(self, client):
        res = client.post("/members", json={"name": "Priya", "age": 28, "plan": "premium"})
        assert res.status_code == 201
        data = json.loads(res.data)
        assert data["member"]["name"] == "Priya"
        assert data["member"]["plan"] == "premium"

    def test_add_member_no_data(self, client):
        res = client.post("/members", content_type="application/json", data="")
        assert res.status_code == 400

    def test_add_member_missing_name(self, client):
        res = client.post("/members", json={"age": 22, "plan": "basic"})
        assert res.status_code == 400

    def test_add_member_missing_age(self, client):
        res = client.post("/members", json={"name": "Sam", "plan": "basic"})
        assert res.status_code == 400

    def test_add_member_invalid_age_zero(self, client):
        res = client.post("/members", json={"name": "Sam", "age": 0, "plan": "basic"})
        assert res.status_code == 400

    def test_add_member_invalid_plan(self, client):
        res = client.post("/members", json={"name": "Sam", "age": 25, "plan": "gold"})
        assert res.status_code == 400

    def test_add_member_vip_plan(self, client):
        res = client.post("/members", json={"name": "CEO", "age": 40, "plan": "vip"})
        assert res.status_code == 201

    def test_member_id_auto_increments(self, client):
        client.post("/members", json={"name": "A", "age": 20, "plan": "basic"})
        client.post("/members", json={"name": "B", "age": 21, "plan": "basic"})
        res = client.get("/members")
        data = json.loads(res.data)
        assert data["members"][0]["id"] == 1
        assert data["members"][1]["id"] == 2


class TestGetMemberById:
    def test_get_existing_member(self, client):
        client.post("/members", json={"name": "Ankit", "age": 30, "plan": "basic"})
        res = client.get("/members/1")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["name"] == "Ankit"

    def test_get_nonexistent_member(self, client):
        res = client.get("/members/999")
        assert res.status_code == 404


# ── Classes ───────────────────────────────────────────────────────────────────
class TestGetClasses:
    def test_classes_returns_200(self, client):
        res = client.get("/classes")
        assert res.status_code == 200

    def test_classes_has_three_entries(self, client):
        res = client.get("/classes")
        data = json.loads(res.data)
        assert data["total"] == 3

    def test_classes_contains_yoga(self, client):
        res = client.get("/classes")
        data = json.loads(res.data)
        names = [c["name"] for c in data["classes"]]
        assert "Yoga" in names


class TestEnrollClass:
    def test_enroll_valid_class(self, client):
        res = client.post("/classes/1/enroll")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["class"]["enrolled"] == 1

    def test_enroll_nonexistent_class(self, client):
        res = client.post("/classes/99/enroll")
        assert res.status_code == 404

    def test_enroll_full_class(self, client):
        # Fill class 3 (CrossFit, capacity=10)
        for _ in range(10):
            client.post("/classes/3/enroll")
        res = client.post("/classes/3/enroll")
        assert res.status_code == 400
        data = json.loads(res.data)
        assert "full" in data["error"]


# ── BMI Calculator ────────────────────────────────────────────────────────────
class TestBMI:
    def test_normal_weight(self, client):
        res = client.post("/bmi", json={"weight": 70, "height": 1.75})
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["category"] == "Normal weight"
        assert data["bmi"] == 22.86

    def test_underweight(self, client):
        res = client.post("/bmi", json={"weight": 45, "height": 1.75})
        data = json.loads(res.data)
        assert data["category"] == "Underweight"

    def test_overweight(self, client):
        res = client.post("/bmi", json={"weight": 85, "height": 1.75})
        data = json.loads(res.data)
        assert data["category"] == "Overweight"

    def test_obese(self, client):
        res = client.post("/bmi", json={"weight": 120, "height": 1.75})
        data = json.loads(res.data)
        assert data["category"] == "Obese"

    def test_missing_weight(self, client):
        res = client.post("/bmi", json={"height": 1.75})
        assert res.status_code == 400

    def test_missing_height(self, client):
        res = client.post("/bmi", json={"weight": 70})
        assert res.status_code == 400

    def test_zero_height(self, client):
        res = client.post("/bmi", json={"weight": 70, "height": 0})
        assert res.status_code == 400

    def test_negative_weight(self, client):
        res = client.post("/bmi", json={"weight": -10, "height": 1.75})
        assert res.status_code == 400

    def test_no_data(self, client):
        res = client.post("/bmi", content_type="application/json", data="")
        assert res.status_code == 400
