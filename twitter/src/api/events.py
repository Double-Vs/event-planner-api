from flask import Blueprint, jsonify, abort, request
from ..models import Event, db

bp = Blueprint('events', __name__, url_prefix='/events')

@bp.route('', methods=['GET'])

def index():
    events = Event.query.all()
    return jsonify([e.serialize() for e in events])

@bp.route('/<int:id>', methods=['GET'])

def show(id: int):
    e = Event.query.get_or_404(id)
    return jsonify(e.serialize())
@bp.route('', methods=['POST'])

def create():
    required = ['host_id', 'event_date', 'start_time', 'end_time', 'location', 'total_budget']

    for field in required:
        if field not in request.json:
            return abort(400)


    e = Event(
        host_id=request.json['host_id'],
        event_date=request.json['event_date'],
        start_time=request.json['start_time'],
        end_time=request.json['end_time'],
        location=request.json['location'],
        total_budget=request.json['total_budget']
    )

    db.session.add(e)
    db.session.commit()

    return jsonify(e.serialize())

@bp.route('/<int:id>', methods=['DELETE'])

def delete(id: int):
    e = Event.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    return jsonify(True)
