from flask import Flask, request, jsonify
from repository import AccountRepository
from service import AccountService
from exceptions import AccountNotFoundError, ValidationError

app = Flask(__name__)

repo = AccountRepository()
service = AccountService(repo)

@app.errorhandler(AccountNotFoundError)
def handle_not_found(e):
    return jsonify({"error": str(e), "code": "NOT_FOUND"}), 404

@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({"error": str(e), "code": "BAD_REQUEST"}), 400

@app.route("/accounts", methods=["GET"])
def get_accounts():
    status = request.args.get("status")
    currency = request.args.get("currency")
    sort_by = request.args.get("sort")
    order = request.args.get("order", "asc")
    
    accounts = service.get_accounts(status, currency, sort_by, order)
    return jsonify(accounts), 200

@app.route("/accounts/<int:acc_id>", methods=["GET"])
def get_account(acc_id):
    account = service.get_account(acc_id)
    return jsonify(account), 200

@app.route("/accounts", methods=["POST"])
def create_account():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Нет тела запроса JSON", "code": "BAD_REQUEST"}), 400
    account = service.create_account(data)
    return jsonify(account), 201

@app.route("/accounts/<int:acc_id>", methods=["PUT"])
def update_account(acc_id):
    data = request.get_json()
    account = service.update_account_full(acc_id, data)
    return jsonify(account), 200

@app.route("/accounts/<int:acc_id>", methods=["PATCH"])
def patch_account(acc_id):
    data = request.get_json()
    account = service.update_account_partial(acc_id, data)
    return jsonify(account), 200

@app.route("/accounts/<int:acc_id>", methods=["DELETE"])
def delete_account(acc_id):
    service.delete_account(acc_id)
    return "", 204

@app.route("/accounts/total-funds", methods=["GET"])
def get_total_funds():
    result = service.calculate_total_funds()
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)