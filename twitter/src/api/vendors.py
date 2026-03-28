from flask import Blueprint, jsonify, abort, request

from ..models import Vendor, db

# Create routes for vendors
bp = Blueprint('vendors', __name__, url_prefix='/vendors')

# GET /vendors → get all vendors
@bp.route('', methods=['GET'])
def index():

    vendors = Vendor.query.all()  # get all vendors from DB
    result = []

    for v in vendors:
        result.append(v.serialize())  # convert each vendor to JSON

    return jsonify(result)

# GET /vendors/<id> → get one vendor
@bp.route('/<int:id>', methods=['GET'])
def show(id):
    vendor = Vendor.query.get(id)  # find vendor by id

    if not vendor:
        abort(404)  # return error if not found

    return jsonify(vendor.serialize())

# POST /vendors → create a new vendor

@bp.route('', methods=['POST'])

def create():
    name = request.json['name']  # get name from request

    # simple validation (name should not be empty)
    if len(name) < 1:
        abort(400)

    v = Vendor(name=name)  # create vendor

    db.session.add(v)     # add to database
    db.session.commit()   # save changes

    return jsonify(v.serialize())  # return new vendor

@bp.route('/<int:id>', methods=['DELETE'])

def delete(id: int):
    v = Vendor.query.get_or_404(id)
    db.session.delete(v)
    db.session.commit()
    return jsonify(True)

