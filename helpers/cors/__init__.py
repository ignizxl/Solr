from flask_cors import CORS

# Inicializando o CORS
cors = CORS(resources={r"/api/*": {"origins": "*"}})