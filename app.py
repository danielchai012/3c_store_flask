from application import create_app
from flask_cors import CORS
app = create_app(config_filename='local.py')
CORS(app, resources={r"/*": {"origins": "*"}})