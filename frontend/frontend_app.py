# Front End Full-Stack App
from flask import Flask, render_template, request
import requests

frontend_app = Flask(__name__)
backend_url = "http://127.0.0.1:5001"

def valid_text(value):
    return isinstance(value, str) and 1 <= len(value.strip()) <= 20

def valid_cost(value):
    try:
        cost = float(value)
        return cost > 0 and cost < 100000
    except:
        return False

@frontend_app.route("/")
@frontend_app.route("/home")
def home():
    response = requests.get(backend_url + "/api")
    return render_template('bucketlist.html', places=response.json()[:5])

@frontend_app.route("/new_destination", methods=["GET", "POST"])
def new_destination():
    if request.method == "GET":
        return render_template('new_destination.html')

    if request.method == "POST":
        dest_name = request.form.get('dest_name')
        country = request.form.get("country")
        cost = request.form.get("cost")

        if not valid_text(dest_name):
            return "<h3>Invalid destination name. Must be 1-20 characters.</h3><a href='/new_destination'>Go Back</a>"

        if not valid_text(country):
            return "<h3>Invalid country. Must be 1-20 characters.</h3><a href='/new_destination'>Go Back</a>"

        if not valid_cost(cost):
            return "<h3>Invalid cost. Must be a positive number less than 100000.</h3><a href='/new_destination'>Go Back</a>"

        new_dest = {
            "name": dest_name.strip(),
            "country": country.strip(),
            "cost": float(cost)
        }

        response = requests.post(backend_url + "/api/new", json=new_dest)

        if response.status_code != 201:
            return f"<h3>Backend rejected the data: {response.text}</h3><a href='/new_destination'>Go Back</a>"

        return f'<h1>Your form was submitted to add {dest_name}. <a href="/home">Continue</a></h1>'

if __name__ == "__main__":
    frontend_app.run(port=5000, debug=True)
