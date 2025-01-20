from pymongo import MongoClient
import os
# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017")
db = client['splitwise']

# Drop existing collections if they exist (for clean setup)
db.users.drop()
db.expenses.drop()
db.balances.drop()

# Create Collections
users_collection = db.users
expenses_collection = db.expenses
balances_collection = db.balances

# Add Indexes for better query performance
users_collection.create_index("email", unique=True)  # Unique emails
expenses_collection.create_index("payer_id")
balances_collection.create_index("user_id", unique=True)

print("Database and collections initialized successfully.")

def dbConnection():
    return db
