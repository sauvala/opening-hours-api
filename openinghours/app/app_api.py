from flask import Flask, request, jsonify

import openinghours.app.opening_hours

app = Flask(__name__)


@app.route('/api/format', methods=['POST'])
def format_schedule():
    json_data = request.get_json()
    formatted_schedule = openinghours.app.opening_hours.format_opening_hours(json_data)
    return jsonify(formatted_schedule)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
