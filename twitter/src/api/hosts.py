from flask import Blueprint, jsonify, abort, request
from ..models import Host, db
bp = Blueprint('hosts', __name__, url_prefix='/hosts')

@bp.route('', methods=['GET'])
def index():
    hosts = Host.query.all()
    return jsonify([h.serialize() for h in hosts])

@bp.route('/<int:id>', methods=['GET'])

def show(id: int):
    h = Host.query.get_or_404(id)
    return jsonify(h.serialize())

@bp.route('', methods=['POST'])

def create():
    if 'name' not in request.json or 'email' not in request.json:
        return abort(400)

    h = Host(
        name=request.json['name'],
        email=request.json['email']
    )

    db.session.add(h)
    db.session.commit()
    return jsonify(h.serialize())

@bp.route('/<int:id>', methods=['DELETE'])

def delete(id: int):
    h = Host.query.get_or_404(id)
    db.session.delete(h)
    db.session.commit()
    return jsonify(True)

