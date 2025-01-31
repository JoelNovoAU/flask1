from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://joelnp:joel16@cluster0.qcsid.mongodb.net/rober?retryWrites=true&w=majority"
mongo = PyMongo(app)

CORS(app, resources={r"/api/*": {"origins": "https://frontflask.vercel.app"}})
     methods=["GET", "POST", "PUT", "DELETE"],
     allow_headers=["Content-Type", "Authorization"])

@app.route('/api', methods=['GET'])
def welcome():
    return jsonify({"message": "Bienvenido a la API"})

@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    try:
        usuarios = mongo.db.usuarios.find()
        return jsonify(dumps(usuarios)), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener usuarios"}), 500

@app.route('/api/usuarios1', methods=['GET'])
def get_primer_usuario():
    try:
        primer_usuario = mongo.db.usuarios.find_one()
        return jsonify(dumps(primer_usuario)), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener el usuario"}), 500

@app.route('/api/usuarios/<id>', methods=['GET'])
def get_usuario_by_id(id):
    try:
        usuario = mongo.db.usuarios.find_one({"id": int(id)})
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify(dumps(usuario)), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener usuario"}), 500

@app.route('/api/crear', methods=['POST'])
def crear_usuario():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No se enviaron datos"}), 400

        nombre = data.get('nombre')
        apellido = data.get('apellido')
        if not nombre or not apellido:
            return jsonify({"error": "Faltan campos obligatorios: 'nombre' y 'apellido'"}), 400

        nuevo_usuario = {"nombre": nombre, "apellido": apellido}
        resultado = mongo.db.usuarios.insert_one(nuevo_usuario)
        nuevo_usuario["_id"] = str(resultado.inserted_id)

        return jsonify(nuevo_usuario), 201
    except Exception as e:
        print(f"Error en /api/crear: {e}")  
        return jsonify({"error": f"Error al crear usuario: {str(e)}"}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ruta no encontrada"}), 404

@app.errorhandler(Exception)
def internal_server_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    app.run(debug=True)
