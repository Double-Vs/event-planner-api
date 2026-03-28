from flask import Blueprint, jsonify, abort, request

from ..models import Vendor, db

bp = Blueprint('vendors', __name__, url_prefix='/vendors')


@bp.route('', methods=['GET'])

def index():

    vendors = Vendor.query.all()

    return jsonify([v.serialize() for v in vendors])

@bp.route('/<int:id>', methods=['GET'])

def show(id: int):

    v = Vendor.query.get_or_404(id)
    return jsonify(v.serialize())


@bp.route('', methods=['POST'])

def create():

    if 'vendor_name' not in request.json or 'service_type' not in request.json:
        return abort(400)

    v = Vendor(
        vendor_name=request.json['vendor_name'],
        service_type=request.json['service_type']
    )


    db.session.add(v)
    db.session.commit()

    return jsonify(v.serialize())

@bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id: int):

    v = Vendor.query.get_or_404(id)
    if 'vendor_name' in request.json:
        v.vendor_name = request.json['vendor_name']
    if 'service_type' in request.json:
        v.service_type = request.json['service_type']


    db.session.commit()
    return jsonify(v.serialize())

@bp.route('/<int:id>', methods=['DELETE'])

def delete(id: int):

    v = Vendor.query.get_or_404(id)

    db.session.delete(v)

    db.session.commit()

    return jsonify(True)

