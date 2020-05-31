from flask import Flask, request, jsonify

from src.opening_hours import format_opening_hours

app = Flask(__name__)


@app.route('/api/convert', methods=['POST'])
def hello_world():
    json_data = request.get_json()
    formatted_schedule = format_opening_hours(json_data)
    return jsonify(formatted_schedule)
