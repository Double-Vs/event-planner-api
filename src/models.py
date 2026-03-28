import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Host(db.Model):
    __tablename__ = 'host'
    host_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))

    def serialize(self):
        return {
            "host_id": self.host_id,
            "name": self.name,
            "email": self.email
        }

class Guest(db.Model):
    __tablename__ = 'guest'
    guest_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    phone = db.Column(db.String(50))

    def serialize(self):
        return {
            "guest_id": self.guest_id,
            "name": self.name,
            "phone": self.phone
        }

class Vendor(db.Model):
    __tablename__ = 'vendor'
    vendor_id = db.Column(db.Integer, primary_key=True)
    vendor_name = db.Column(db.String(255))
    service_type = db.Column(db.String(255))

    def serialize(self):
        return {
            "vendor_id": self.vendor_id,
            "vendor_name": self.vendor_name,
            "service_type": self.service_type
        }

class Event(db.Model):
    __tablename__ = 'event'
    event_id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer)
    event_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    location = db.Column(db.String(255))
    total_budget = db.Column(db.Numeric)

    def serialize(self):
        return {
            "event_id": self.event_id,
            "host_id": self.host_id,
            "event_date": str(self.event_date),
            "start_time": str(self.start_time),
            "end_time": str(self.end_time),
            "location": self.location,
            "total_budget": float(self.total_budget) if self.total_budget else None
        }
class EventDetails(db.Model):

    __tablename__ = 'event_details'
    details_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer)
    theme = db.Column(db.String(255))
    decorations = db.Column(db.String(255))
    dessert = db.Column(db.String(255))

    def serialize(self):
        return {
            "details_id": self.details_id,
            "event_id": self.event_id,
            "theme": self.theme,
            "decorations": self.decorations,
            "dessert": self.dessert
        }

class EventGuest(db.Model):
    __tablename__ = 'event_guest'

    event_id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, primary_key=True)

class EventVendor(db.Model):
    __tablename__ = 'event_vendor'
    event_id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, primary_key=True)


