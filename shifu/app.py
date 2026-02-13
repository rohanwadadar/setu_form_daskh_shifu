from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATABASE_URL, SECRET_KEY

# ─── APP SETUP ───────────────────────────────────────────
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)
CORS(app)

# Register controller routes
from shifu.controller import shifu_bp
app.register_blueprint(shifu_bp, url_prefix='/api/shifu')

# Create tables
with app.app_context():
    from shifu.model import ShifuForm  # noqa: F401
    db.create_all()
    print("[OK] Table 'shifu_form' created in PostgreSQL!")
