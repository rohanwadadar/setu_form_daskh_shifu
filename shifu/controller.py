from flask import Blueprint, request, jsonify
from shifu.app import db
from shifu.model import ShifuForm, ShifuOption

shifu_bp = Blueprint('shifu', __name__)


# ─── 1) SUBMIT FORM (POST) ──────────────────────────────
@shifu_bp.route('', methods=['POST'])
def submit_form():
    """
    Submit the 'Let's Get Started' form.
    POST JSON body:
    {
        "name": "Prem Kumar",
        "work_email": "prem18@gmail.com",
        "company": "Acme Corporation",
        "role": "Head of L&D",
        "looking_for": "Request a Demo",
        "goals": "Scale training across teams"
    }
    """
    try:
        data = request.get_json()

        # Validate required fields
        required = ['name', 'work_email', 'company', 'looking_for']
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing)}'
            }), 400

        # Validate looking_for value against DB
        looking_for = data['looking_for'].strip()
        valid_option = ShifuOption.query.filter_by(label=looking_for, is_active=True).first()
        
        if not valid_option:
            return jsonify({
                'success': False,
                'error': f'Invalid or inactive "looking_for" option: {looking_for}'
            }), 400

        entry = ShifuForm(
            name=data['name'].strip(),
            work_email=data['work_email'].strip(),
            company=data['company'].strip(),
            role=data.get('role', '').strip() or None,
            looking_for=looking_for,
            goals=data.get('goals', '').strip() or None,
        )

        db.session.add(entry)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Form submitted successfully!',
            'data': entry.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ─── 2) GET ALL SUBMISSIONS (GET) ───────────────────────
@shifu_bp.route('', methods=['GET'])
def get_all():
    """Get all form submissions."""
    try:
        entries = ShifuForm.query.order_by(ShifuForm.created_at.desc()).all()
        return jsonify({
            'success': True,
            'total': len(entries),
            'data': [e.to_dict() for e in entries]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ─── 3) GET ONE BY ID (GET) ─────────────────────────────
@shifu_bp.route('/<int:id>', methods=['GET'])
def get_one(id):
    """Get a single form submission by ID."""
    try:
        entry = ShifuForm.query.get(id)
        if not entry:
            return jsonify({'success': False, 'error': 'Entry not found'}), 404
        return jsonify({'success': True, 'data': entry.to_dict()}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ─── 4) UPDATE BY ID (PUT) ──────────────────────────────
@shifu_bp.route('/<int:id>', methods=['PUT'])
def update_form(id):
    """Update an existing form submission."""
    try:
        entry = ShifuForm.query.get(id)
        if not entry:
            return jsonify({'success': False, 'error': 'Entry not found'}), 404

        data = request.get_json()

        if 'name' in data:
            entry.name = data['name'].strip()
        if 'work_email' in data:
            entry.work_email = data['work_email'].strip()
        if 'company' in data:
            entry.company = data['company'].strip()
        if 'role' in data:
            entry.role = data['role'].strip() or None
        if 'looking_for' in data:
            looking_for = data['looking_for'].strip()
            valid_option = ShifuOption.query.filter_by(label=looking_for, is_active=True).first()
            if not valid_option:
                return jsonify({
                    'success': False,
                    'error': f'Invalid or inactive "looking_for" option: {looking_for}'
                }), 400
            entry.looking_for = looking_for
        if 'goals' in data:
            entry.goals = data['goals'].strip() or None

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Entry updated successfully!',
            'data': entry.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ─── 5) DELETE BY ID (DELETE) ────────────────────────────
@shifu_bp.route('/<int:id>', methods=['DELETE'])
def delete_form(id):
    """Delete a form submission by ID."""
    try:
        entry = ShifuForm.query.get(id)
        if not entry:
            return jsonify({'success': False, 'error': 'Entry not found'}), 404

        db.session.delete(entry)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Entry {id} deleted successfully!'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
# ─── 6) GET ALL OPTIONS (GET) ───────────────────────────
@shifu_bp.route('/options', methods=['GET'])
def get_options():
    """Get all active form options."""
    try:
        options = ShifuOption.query.filter_by(is_active=True).all()
        return jsonify({
            'success': True,
            'data': [o.to_dict() for o in options]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
