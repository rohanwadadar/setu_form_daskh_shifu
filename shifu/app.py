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

# Create tables and seed data
with app.app_context():
    from shifu.model import ShifuForm, ShifuOption
    db.create_all()
    
    # SEED INITIAL OPTIONS
    initial_options = [
        'Request a Demo',
        'Start a Pilot Program',
        'General Inquiry',
        'Schedule a Briefing'
    ]
    
    for opt_label in initial_options:
        exists = ShifuOption.query.filter_by(label=opt_label).first()
        if not exists:
            db.session.add(ShifuOption(label=opt_label))
    
    db.session.commit()
    print("[OK] Shifu tables created and data seeded!")
