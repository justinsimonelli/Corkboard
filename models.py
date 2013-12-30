from app import db


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


class Todos(db.Model):
    id = db.Column(db.INTEGER, primary_key = True, autoincrement = True)
    timestamp = db.Column(db.TIMESTAMP)
    message = db.Column(db.VARCHAR(4000))
    latitude = db.Column(db.VARCHAR(20))
    longitude = db.Column(db.VARCHAR(20))

    def __repr__(self):
        return '<ToDoItem %r>' % (self.message)

    def serialize(self):
        """Return object data in easily serializeable format
        @rtype : object
        """
        return {
            'id': self.id,
            'timestame': dump_datetime(self.timestame),
            'message': self.message,
            'latitude': self.latitude,
            'longitude': self.longitude
        }