from flask import Blueprint, jsonify, abort, request
from ..models import Guest, db

bp = Blueprint('guests', __name__, url_prefix='/guests')

@bp.route('', methods=['GET'])

def index():
    guests = Guest.query.all()
    return jsonify([g.serialize() for g in guests])

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    g = Guest.query.get_or_404(id)
    return jsonify(g.serialize())

@bp.route('', methods=['POST'])

def create():

    if 'name' not in request.json or 'phone' not in request.json:
        return abort(400)

    g = Guest(
        name=request.json['name'],
        phone=request.json['phone']
    )

    db.session.add(g)
    db.session.commit()
    return jsonify(g.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    g = Guest.query.get_or_404(id)
    db.session.delete(g)
    db.session.commit()
    return jsonify(True)
