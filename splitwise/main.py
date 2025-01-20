from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import uuid
from db_init import db
from users import user_bp
app = Flask(__name__)

# MongoDB Configuration
db = db

users_collection = db.users
expenses_collection = db.expenses
balances_collection = db.balances

# Register the Blueprint
app.register_blueprint(user_bp)

# Helper Functions
def update_balances(payer_id, amount, participants):
    split_amount = amount / len(participants)
    for participant in participants:
        if participant != payer_id:
            # Update payer's balance with the participant
            balances_collection.update_one(
                {"user_id": payer_id},
                {"$inc": {f"balances.{participant}": split_amount}},
                upsert=True
            )
            # Update participant's balance with the payer
            balances_collection.update_one(
                {"user_id": participant},
                {"$inc": {f"balances.{payer_id}": -split_amount}},
                upsert=True
            )



@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.json
    expense_id = str(uuid.uuid4())
    payer_id = data["payer_id"]
    amount = data["amount"]
    participants = data["participants"]

    # Add expense to the collection
    expenses_collection.insert_one({
        "_id": expense_id,
        "payer_id": payer_id,
        "amount": amount,
        "participants": participants,
        "description": data.get("description", ""),
        "created_at": datetime.utcnow()
    })

    # Update balances
    update_balances(payer_id, amount, participants)

    return jsonify({"message": "Expense added", "expense_id": expense_id}), 201


@app.route('/balances/<user_id>', methods=['GET'])
def get_balances(user_id):
    balance = balances_collection.find_one({"user_id": user_id}, {"_id": 0, "balances": 1})
    if not balance:
        return jsonify({"message": "No balances found for the user"}), 404
    return jsonify(balance), 200


@app.route('/settle', methods=['POST'])
def settle_debts():
    user_id = request.json["user_id"]
    balances = balances_collection.find_one({"user_id": user_id}, {"_id": 0, "balances": 1})
    if not balances or not balances.get("balances"):
        return jsonify({"message": "No debts to settle"}), 404

    creditors = [(uid, amt) for uid, amt in balances["balances"].items() if amt > 0]
    debtors = [(uid, -amt) for uid, amt in balances["balances"].items() if amt < 0]

    transactions = []

    while creditors and debtors:
        creditor_id, credit_amount = creditors.pop()
        debtor_id, debt_amount = debtors.pop()

        settled_amount = min(credit_amount, debt_amount)
        transactions.append({
            "from": debtor_id,
            "to": creditor_id,
            "amount": settled_amount
        })

        if credit_amount > debt_amount:
            creditors.append((creditor_id, credit_amount - settled_amount))
        elif debt_amount > credit_amount:
            debtors.append((debtor_id, debt_amount - settled_amount))

    return jsonify({"transactions": transactions}), 200


if __name__ == '__main__':
    app.run(debug=True)
