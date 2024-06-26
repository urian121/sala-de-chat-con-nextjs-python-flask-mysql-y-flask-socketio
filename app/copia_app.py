from flask import Flask, request, jsonify
import requests
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# Configuración del secreto para JWT
# Cambia esta clave secreta por una más segura en producción
app.config['JWT_SECRET_KEY'] = 'super-secret'

# Inicializar el JWTManager
jwt = JWTManager(app)


@app.route('/welcome', methods=['GET'])
def welcome():
    return jsonify({"message": "¡Bienvenido a la API de Flask!"})


@app.route('/sum', methods=['POST'])
def sum_numbers():
    data = request.get_json()
    a = data.get('a')
    b = data.get('b')
    result = a + b
    return jsonify({"result": result})

# Endpoint de autenticación para obtener el token JWT


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Aquí deberías verificar el nombre de usuario y la contraseña con tu base de datos
    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    # Crear el token de acceso
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# Ruta protegida con JWT


@app.route('/usuarios', methods=['GET'])
@jwt_required()
def api():
    URL_API = 'https://jsonplaceholder.typicode.com/users/'
    solic_req = requests.get(URL_API)
    data_API = solic_req.json()  # Este método es conveniente cuando la API devuelve JSON

    if solic_req.status_code == 200:
        print(data_API)
        return jsonify({'resp': data_API})
    else:
        return jsonify({'resp': 'No hay datos'}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)
