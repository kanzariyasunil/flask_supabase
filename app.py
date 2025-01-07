import psycopg2
from flask import Flask, jsonify, request
import os
from supabase import create_client, Client

url: str = (
    "postgres://postgres.kbgnupozmknbfphdcuhn:h5evZx4qUJhNgNOl@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require&supa=base-pooler.x"
)
key: str = ""
supabase: Client = create_client(url, key)


# Initialize the Flask app
app = Flask(__name__)

# PostgreSQL connection parameters
DB_HOST = "117.248.251.91"
DB_NAME = "dummy_database"
DB_USER = "postgres"
DB_PASSWORD = "bsre@1234"
DB_PORT = 5432


# Database connection function
def get_db_connection():
    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        password=DB_PASSWORD,
        port=DB_PORT,
    )

    return connection


# Routes
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Flask app with psycopg2!"})


@app.route("/users", methods=["GET"])
def get_users():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, email FROM users;")
    users = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(
        [{"id": user[0], "name": user[1], "email": user[2]} for user in users]
    )


@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;",
        (data["name"], data["email"]),
    )
    user_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": f"User added successfully!", "user_id": user_id}), 201


if __name__ == "__main__":
    app.run(debug=True, port=8000)
