from flask import Blueprint, jsonify, abort, request

from ..models import Host, db



bp = Blueprint('hosts', __name__, url_prefix='/hosts')





# GET all hosts

@bp.route('', methods=['GET'])

def index():

    hosts = Host.query.all()

    return jsonify([h.serialize() for h in hosts])





# GET one host

@bp.route('/<int:id>', methods=['GET'])

def show(id: int):

    h = Host.query.get_or_404(id)

    return jsonify(h.serialize())





# CREATE host

@bp.route('', methods=['POST'])

def create():

    if not request.json or 'name' not in request.json or 'email' not in request.json:

        return abort(400)



    h = Host(

        name=request.json['name'],

        email=request.json['email']

    )



    db.session.add(h)

    db.session.commit()



    return jsonify(h.serialize())





# UPDATE host

@bp.route('/<int:id>', methods=['PUT'])

def update(id: int):

    h = Host.query.get_or_404(id)



    if not request.json:

        return abort(400)



    if 'name' in request.json:

        h.name = request.json['name']

    if 'email' in request.json:

        h.email = request.json['email']



    db.session.commit()

    return jsonify(h.serialize())





# DELETE host

@bp.route('/<int:id>', methods=['DELETE'])

def delete(id: int):

    h = Host.query.get_or_404(id)



    db.session.delete(h)

    db.session.commit()



    return jsonify({"message": "Deleted"})

