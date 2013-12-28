from app import db

class TODOS(db.Model):
	message = db.Column(db.VARCHAR(4000))
	latitude = db.Column(db.VARCHAR(20))
	longitude = db.Column(db.VARCHAR(20))

	def __repr__(self):
		return '<ToDoItem %r>' % (self.message)