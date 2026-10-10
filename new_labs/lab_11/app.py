from flask import Flask, request, jsonify, send_from_directory
from service import BankService

app = Flask(__name__)
service = BankService()

@app.route("/accounts", methods=["GET"])
def get_accounts():
    return jsonify(service.get_all_accounts()), 200

@app.route("/transfer", methods=["POST"])
def transfer():
    data = request.get_json()
    try:
        service.process_transfer(data["from_id"], data["to_id"], data["amount"])
        return jsonify({"status": "Транзакция (COMMIT) успешно завершена"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ошибка транзакции (ROLLBACK)"}), 500

#redis эндпоинты
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    try:
        token = service.login_user(data["client_id"])
        return jsonify({"token": token, "message": "Сессия сохранена в Redis на 60 секунд"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/session/<token>", methods=["GET"])
def get_session(token):
    try:
        client_id = service.check_session(token)
        return jsonify({"client_id": client_id, "status": "Активна"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

#имитация cdn контента, статические файлы раздаются без БД
@app.route("/cdn/ads/<filename>")
def cdn_ads(filename):
    response = send_from_directory('static/cdn', filename)
    response.headers['Cache-Control'] = 'public, max-age=3600'
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5000)