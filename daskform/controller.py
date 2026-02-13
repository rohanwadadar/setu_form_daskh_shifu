from flask import Blueprint, request, jsonify
from daskform.app import db
from daskform.model import DakshForm

daskform_bp = Blueprint('daskform', __name__)


# ─── 1) SUBMIT FORM (POST) ──────────────────────────────
@daskform_bp.route('', methods=['POST'])
def submit_form():
    """
    Submit the 'Let's Connect' form.
    POST JSON body:
    {
        "your_email": "you@gmail.com",
        "what_best_describes_you": "Developer",
        "what_are_you_hoping_to_achieve": "Build products",
        "tell_us_more": "Optional details here"
    }
    """
    try:
        data = request.get_json()

        # Validate required fields
        required = ['your_email', 'what_best_describes_you', 'what_are_you_hoping_to_achieve']
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing)}'
            }), 400

        entry = DakshForm(
            your_email=data['your_email'].strip(),
            what_best_describes_you=data['what_best_describes_you'].strip(),
            what_are_you_hoping_to_achieve=data['what_are_you_hoping_to_achieve'].strip(),
            tell_us_more=data.get('tell_us_more', '').strip() or None,
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
@daskform_bp.route('', methods=['GET'])
def get_all():
    """Get all form submissions."""
    try:
        entries = DakshForm.query.order_by(DakshForm.created_at.desc()).all()
        return jsonify({
            'success': True,
            'total': len(entries),
            'data': [e.to_dict() for e in entries]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ─── 3) GET ONE BY ID (GET) ─────────────────────────────
@daskform_bp.route('/<int:id>', methods=['GET'])
def get_one(id):
    """Get a single form submission by ID."""
    try:
        entry = DakshForm.query.get(id)
        if not entry:
            return jsonify({'success': False, 'error': 'Entry not found'}), 404
        return jsonify({'success': True, 'data': entry.to_dict()}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ─── 4) UPDATE BY ID (PUT) ──────────────────────────────
@daskform_bp.route('/<int:id>', methods=['PUT'])
def update_form(id):
    """Update an existing form submission."""
    try:
        entry = DakshForm.query.get(id)
        if not entry:
            return jsonify({'success': False, 'error': 'Entry not found'}), 404

        data = request.get_json()

        if 'your_email' in data:
            entry.your_email = data['your_email'].strip()
        if 'what_best_describes_you' in data:
            entry.what_best_describes_you = data['what_best_describes_you'].strip()
        if 'what_are_you_hoping_to_achieve' in data:
            entry.what_are_you_hoping_to_achieve = data['what_are_you_hoping_to_achieve'].strip()
        if 'tell_us_more' in data:
            entry.tell_us_more = data['tell_us_more'].strip() or None

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
@daskform_bp.route('/<int:id>', methods=['DELETE'])
def delete_form(id):
    """Delete a form submission by ID."""
    try:
        entry = DakshForm.query.get(id)
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
