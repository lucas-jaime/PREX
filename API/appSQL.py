from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Tablas
class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50), nullable=False)
    os_name = db.Column(db.String(100))
    os_version = db.Column(db.String(100))
    processor = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    processes = db.relationship('Process', backref='server', lazy=True)
    users = db.relationship('User', backref='server', lazy=True)

class Process(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)
    pid = db.Column(db.Integer)
    name = db.Column(db.String(100))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)
    username = db.Column(db.String(100))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/collect', methods=['POST'])
def collect_data():
    data = request.json
    client_ip = request.remote_addr

    server = Server(
        ip=client_ip,
        os_name=data.get("os_name"),
        os_version=data.get("os_version"),
        processor=data.get("processor")
    )
    db.session.add(server)
    db.session.commit()

    for process in data.get("processes", []):
        db.session.add(Process(server_id=server.id, pid=process["pid"], name=process["name"]))

    for username in data.get("users", []):
        db.session.add(User(server_id=server.id, username=username))

    db.session.commit()
    return jsonify({"Mensaje": "Datos almacenados correctamente"}), 200

@app.route('/query', methods=['GET'])
def query_data():
    ip = request.args.get('ip')
    if not ip:
        return jsonify({"Error": "El parámetro IP es requerido"}), 400

    server = Server.query.filter_by(ip=ip).first()
    if not server:
        return jsonify({"Error": "No se encontraron datos sobre esta IP"}), 404

    result = {
        "ip": server.ip,
        "os_name": server.os_name,
        "os_version": server.os_version,
        "processor": server.processor,
        "timestamp": server.timestamp,
        "processes": [{"pid": p.pid, "name": p.name} for p in server.processes],
        "users": [{"username": u.username} for u in server.users]
    }

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
