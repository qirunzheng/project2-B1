# Back End Full_Stack App
from flask import Flask, request, jsonify
import sqlite3
import json

# create the backend application, which only works with the database
backend_app = Flask(__name__)

# function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('../backend/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def valid_text(value):
    return isinstance(value, str) and 1 <= len(value.strip()) <= 20

def valid_cost(value):
    try:
        cost = float(value)
        return cost > 0 and cost < 100000
    except:
        return False

# ENDPOINTS
@backend_app.route("/api", methods=["GET"])
def get_all():
    # retrieve list from the database
    # connect to DB, run the SQL statement, close the connection
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM destinations').fetchall()
    conn.close()
    # the variable rows now contains a list of sqlite Row objects,
    # which needs to be converted to a list of dictionaries (i.e. json)
    result_list = [dict(row) for row in rows]
    # now we can send it to the json library to convert it to a string
    json_output = json.dumps(result_list, indent=4)
    return(json_output), 200  # creates response json, returns HTTP response 200

# create a new destination
@backend_app.route("/api/new", methods=["POST"])
def create_dest():
    # get info from POST request
    data = request.get_json()  # parses incoming json
    # TODO: Input validation on all fields prior to database insertion!
    if not data:
        return jsonify({"error": "No data"}), 400

    name = data.get("name")
    country = data.get("country")
    cost = data.get("cost")

    if not valid_text(name):
        return jsonify({"error": "Invalid name"}), 400

    if not valid_text(country):
        return jsonify({"error": "Invalid country"}), 400

    if not valid_cost(cost):
        return jsonify({"error": "Invalid cost"}), 400


    # Connect to DB and insert information
    conn = get_db_connection()
    conn.execute(
    "INSERT INTO destinations (name, country, cost) VALUES (?, ?, ?)",
    (name, country, float(cost))
)
    conn.commit()
    conn.close()
    return jsonify({
    "name": name,
    "country": country,
    "cost": float(cost)
}), 201 
 # creates response json, returns HTTP response 201、
if __name__ == "__main__":
    backend_app.run(port=5001, debug=True)