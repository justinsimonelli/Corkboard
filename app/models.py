from app import db

class Todos(db.Model):
	__tablename__ = 'TODOS'
	id = db.Column(db.INTEGER, primary_key = True, autoincrement = True)
	timestamp = db.Column(db.TIMESTAMP)
	message = db.Column(db.VARCHAR(4000))
	latitude = db.Column(db.VARCHAR(20))
	longitude = db.Column(db.VARCHAR(20))

	def __repr__(self):
		return '<ToDoItem %r>' % (self.message)