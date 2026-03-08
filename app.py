from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store
members = []
classes = [
    {"id": 1, "name": "Yoga", "trainer": "Alice", "capacity": 20, "enrolled": 0},
    {"id": 2, "name": "Zumba", "trainer": "Bob", "capacity": 15, "enrolled": 0},
    {"id": 3, "name": "CrossFit", "trainer": "Charlie", "capacity": 10, "enrolled": 0},
]


# ── Home ────────────────────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to ACEest Fitness & Gym!",
        "status": "operational",
        "version": "1.0.0"
    })


# ── Health Check ─────────────────────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


# ── Members ──────────────────────────────────────────────────────────────────
@app.route("/members", methods=["GET"])
def get_members():
    return jsonify({"members": members, "total": len(members)}), 200


@app.route("/members", methods=["POST"])
def add_member():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get("name", "").strip()
    age  = data.get("age")
    plan = data.get("plan", "basic").strip().lower()

    if not name:
        return jsonify({"error": "Name is required"}), 400
    if age is None or not isinstance(age, int) or age <= 0:
        return jsonify({"error": "Valid age is required"}), 400
    if plan not in ("basic", "premium", "vip"):
        return jsonify({"error": "Plan must be basic, premium, or vip"}), 400

    member = {
        "id":   len(members) + 1,
        "name": name,
        "age":  age,
        "plan": plan,
    }
    members.append(member)
    return jsonify({"message": "Member added successfully", "member": member}), 201


@app.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id):
    member = next((m for m in members if m["id"] == member_id), None)
    if not member:
        return jsonify({"error": "Member not found"}), 404
    return jsonify(member), 200


# ── Classes ───────────────────────────────────────────────────────────────────
@app.route("/classes", methods=["GET"])
def get_classes():
    return jsonify({"classes": classes, "total": len(classes)}), 200


@app.route("/classes/<int:class_id>/enroll", methods=["POST"])
def enroll_class(class_id):
    gym_class = next((c for c in classes if c["id"] == class_id), None)
    if not gym_class:
        return jsonify({"error": "Class not found"}), 404
    if gym_class["enrolled"] >= gym_class["capacity"]:
        return jsonify({"error": "Class is full"}), 400

    gym_class["enrolled"] += 1
    return jsonify({
        "message": f"Successfully enrolled in {gym_class['name']}",
        "class": gym_class
    }), 200


# ── BMI Calculator ────────────────────────────────────────────────────────────
@app.route("/bmi", methods=["POST"])
def calculate_bmi():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    weight = data.get("weight")   # kg
    height = data.get("height")   # metres

    if weight is None or height is None:
        return jsonify({"error": "Weight and height are required"}), 400
    if not isinstance(weight, (int, float)) or weight <= 0:
        return jsonify({"error": "Weight must be a positive number"}), 400
    if not isinstance(height, (int, float)) or height <= 0:
        return jsonify({"error": "Height must be a positive number"}), 400

    bmi = round(weight / (height ** 2), 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return jsonify({"bmi": bmi, "category": category}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
