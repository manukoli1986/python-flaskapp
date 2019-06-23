#!/usr/bin/env python3

from flask import Flask, request, jsonify
import requests, random, json

app = Flask(__name__)

@app.route('/api', methods=['POST'])

def api():
    user_data = request.get_json()
    data = user_data['message']
    r = requests.post('http://localhost:5000/reverse', json={'message': data })
    json_resp = r.json()
    a = random.random()
    return jsonify({"rand": a, "message": json_resp.get("message")})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
