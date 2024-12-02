from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = "data"

os.makedirs(DATA_DIR, exist_ok=True)


# Definimos el json sobre el cual se almacenaran los datos de manera tal que se guarden como: "{client_ip}_{date}.json"


@app.route('/collect', methods=['POST'])
def collect_data():
    data = request.json
    client_ip = request.remote_addr
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{DATA_DIR}/{client_ip}_{date}.json"
    
    with open(filename, 'w') as file:
        json.dump(data, file)
    
    return jsonify({"message": "Data stored successfully"}), 200


# Query para realizar un GET de los datos sobre el endpoint mediante la IP


@app.route('/query', methods=['GET'])
def query_data():
    ip = request.args.get('ip')
    if not ip:  
        return jsonify({"error": "El parámetro IP es requerido"}), 400
    
    files = [f for f in os.listdir(DATA_DIR) if f.startswith(ip)]
    if not files:
        return jsonify({"error": "No se encontraron datos sobre esta IP"}), 404
    
    data = []
    for file in files:
        with open(f"{DATA_DIR}/{file}", 'r') as f:
            data.append(json.load(f))
    
    return jsonify(data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
