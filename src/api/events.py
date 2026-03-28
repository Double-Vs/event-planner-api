from flask import Blueprint, jsonify, abort, request

from ..models import Event, db

import datetime

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
    required = ['host_id', 'event_date', 'start_time', 'end_time']

    for field in required:
        if field not in request.json:
            return abort(400)

    e = Event(

        host_id=request.json['host_id'],
        event_date=datetime.datetime.strptime(request.json['event_date'], '%Y-%m-%d').date(),
        start_time=datetime.datetime.strptime(request.json['start_time'], '%H:%M:%S').time(),
        end_time=datetime.datetime.strptime(request.json['end_time'], '%H:%M:%S').time(),
        location=request.json.get('location'),
        total_budget=request.json.get('total_budget')
    )


    db.session.add(e)
    db.session.commit()
    return jsonify(e.serialize())

@bp.route('/<int:id>', methods=['PUT', 'PATCH'])

def update(id: int):

    e = Event.query.get_or_404(id)


    if 'host_id' in request.json:

        e.host_id = request.json['host_id']

    if 'event_date' in request.json:

        e.event_date = datetime.datetime.strptime(request.json['event_date'], '%Y-%m-%d').date()

    if 'start_time' in request.json:

        e.start_time = datetime.datetime.strptime(request.json['start_time'], '%H:%M:%S').time()

    if 'end_time' in request.json:

        e.end_time = datetime.datetime.strptime(request.json['end_time'], '%H:%M:%S').time()

    if 'location' in request.json:

        e.location = request.json['location']

    if 'total_budget' in request.json:

        e.total_budget = request.json['total_budget']



