from flask import Flask, jsonify, request, make_response
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)

# 🔹 Configuración de la base de datos MongoDB
app.config["MONGO_URI"] = "mongodb+srv://joelnp:joel16@cluster0.qcsid.mongodb.net/rober?retryWrites=true&w=majority"
mongo = PyMongo(app)

# 🔥 Configuración correcta de CORS
CORS(app, resources={r"/api/*": {"origins": "https://frontflask.vercel.app"}})

# 🔹 Ruta de bienvenida
@app.route('/api', methods=['GET'])
def welcome():
    return jsonify({"message": "Bienvenido a la API"}), 200

# 🔹 Obtener todos los usuarios
@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    try:
        usuarios = list(mongo.db.usuarios.find())  # Convertimos a lista
        for usuario in usuarios:
            usuario["_id"] = str(usuario["_id"])  # Convertimos ObjectId a string
        
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener usuarios: {str(e)}"}), 500

# 🔹 Obtener el primer usuario
@app.route('/api/usuarios1', methods=['GET'])
def get_primer_usuario():
    try:
        primer_usuario = mongo.db.usuarios.find_one()
        if not primer_usuario:
            return jsonify({"error": "No hay usuarios"}), 404
        
        primer_usuario["_id"] = str(primer_usuario["_id"])  # Convertimos ObjectId a string
        response = make_response(jsonify(primer_usuario), 200)

        # 🔥 Encabezados CORS adicionales
        response.headers["Access-Control-Allow-Origin"] = "https://frontflask.vercel.app"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response
    except Exception as e:
        return jsonify({"error": f"Error al obtener el usuario: {str(e)}"}), 500

# 🔹 Obtener usuario por ID
@app.route('/api/usuarios/<id>', methods=['GET'])
def get_usuario_by_id(id):
    try:
        print(f"Recibido ID: {id}") 

        # Buscar usuario por el campo "id" (asumiendo que "id" es un número)
        usuario = mongo.db.usuarios.find_one({"id": int(id)})

        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        usuario["_id"] = str(usuario["_id"])  # Convertir _id a string si es necesario
        return jsonify(usuario), 200
    except ValueError:
        return jsonify({"error": "ID inválido, debe ser un número"}), 400
    except Exception as e:
        return jsonify({"error": f"Error al obtener usuario: {str(e)}"}), 500



# 🔹 Crear un usuario
@app.route('/api/crear', methods=['POST'])
def crear_usuario():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No se enviaron datos"}), 400

        id_usuario = data.get('id')  # Obtener el ID manual
        nombre = data.get('nombre')
        apellido = data.get('apellido')

        if not nombre or not apellido or id_usuario is None:
            return jsonify({"error": "Faltan campos obligatorios: 'id', 'nombre', 'apellido'"}), 400

        # Verificar si ya existe un usuario con el mismo ID
        if mongo.db.usuarios.find_one({"id": id_usuario}):
            return jsonify({"error": f"Ya existe un usuario con el ID {id_usuario}"}), 400

        nuevo_usuario = {"id": id_usuario, "nombre": nombre, "apellido": apellido}
        resultado = mongo.db.usuarios.insert_one(nuevo_usuario)
        nuevo_usuario["_id"] = str(resultado.inserted_id)

        return jsonify(nuevo_usuario), 201
    except Exception as e:
        print(f"Error en /api/crear: {e}")  
        return jsonify({"error": f"Error al crear usuario: {str(e)}"}), 500


# 🔹 Manejar solicitudes OPTIONS para CORS
@app.route("/api/usuarios1", methods=["OPTIONS"])
def options_usuarios():
    response = make_response()
    response.headers["Access-Control-Allow-Origin"] = "https://frontflask.vercel.app"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

# 🔹 Manejo de errores 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ruta no encontrada"}), 404

# 🔹 Manejo de errores generales
@app.errorhandler(Exception)
def internal_server_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500

# 🔹 Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
