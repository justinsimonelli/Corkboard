from app import db

class To_Do(db.Model):
	id = db.Column(db.Integer, primary_key = True )
	timestame = db.Column(db.Timestamp)
	message = db.Column(db.Varchar(4000))
	latitude = db.Column(db.Varchar(20))
	longitude = db.Column(db.Varchar(20))

	def __repr__(self):
		return '<ToDoItem %r>' % (self.message)