from flask import Flask, request, jsonify
import secrets, string, json, os
from datetime import datetime
app = Flask(__name__)
DB_FILE = "immortal_keys.json"
BOT_NAME = "Immortal Breakthrough"
ADMIN_PASSWORD = "Immortal2026!"
def load_keys():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE) as f:
        return json.load(f)
def save_keys(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)
def make_key():
    chars = string.ascii_uppercase + string.digits
    return f"IMMORTAL-{''.join(secrets.choice(chars) for _ in range(4))}-{''.join(secrets.choice(chars) for _ in range(4))}"
@app.route("/")
def home():
    return {"bot": BOT_NAME, "status": "Server is running"}
@app.route("/admin/create_key", methods=["POST"])
def create_key():
    if request.json.get("admin_password") != ADMIN_PASSWORD:
        return jsonify({"error": "Wrong password"}), 403
    keys = load_keys()
    new_key = make_key()
    keys[new_key] = {"bot": BOT_NAME, "created": str(datetime.now()), "used": False, "account": None, "buyer_name": request.json.get("buyer_name", "")}
    save_keys(keys)
    return jsonify({"bot": BOT_NAME, "key": new_key, "status": "created"})
@app.route("/admin/create_my_key", methods=["POST"])
def create_my_key():
    if request.json.get("admin_password") != ADMIN_PASSWORD:
        return jsonify({"error": "Wrong password"}), 403
    keys = load_keys()
    my_key = "IMMORTAL-ME-0001"
    keys[my_key] = {"bot": BOT_NAME, "created": str(datetime.now()), "used": False, "account": None, "buyer_name": "OWNER - ME"}
    save_keys(keys)
    return jsonify({"bot": BOT_NAME, "key": my_key})
@app.route("/validate", methods=["POST"])
def validate():
    data = request.json
    key = data.get("license_key")
    account = data.get("account_id")
    keys = load_keys()
    if key not in keys:
        return jsonify({"valid": False, "message": "Invalid Immortal Breakthrough key"}), 404
    k = keys[key]
    if k["used"] and k["account"] != account:
        return jsonify({"valid": False, "message": "KEY ALREADY USED on another account"}), 403
    if not k["used"]:
        k["used"] = True
        k["account"] = account
        k["used_date"] = str(datetime.now())
        save_keys(keys)
    return jsonify({"valid": True, "message": f"Welcome to {BOT_NAME}", "strategy": "Gold 1.0 + 2.0 Auto DST"})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
