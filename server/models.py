from app import db


class Bot(db.Model):
	__tablename__ = 'tb_bots'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	strategy = db.Column(db.String(100))
	notation = db.Column(db.String(100))
	socketId = db.Column(db.String(100))
	isConfigured = db.Column(db.Boolean)
	isRunning = db.Column(db.Boolean)
	value = db.Column(db.Float)
	started_at = db.Column(db.DateTime)
	stopped_at = db.Column(db.DateTime)

	def __init__(
		self, 
		name="bot1", 
		strategy="", 
		notation="",
		socketId="",
		isConfigured=False,
		isRunning=False,
		value=0,
		started_at=None,
		stopped_at=None
		):
		self.name = name
		self.strategy = strategy
		self.notation = notation
		self.socketId = socketId
		self.isConfigured = isConfigured
		self.isRunning = isRunning
		self.value = value
		self.started_at = started_at
		self.stopped_at = stopped_at
	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'strategy': self.strategy,
			'notation': self.notation,
			'socketId': self.socketId,
			'isConfigured': self.isConfigured,
			'isRunning': self.isRunning,
			'value': self.value,
			'started_at': self.started_at,
			'stopped_at': self.stopped_at,
		}

	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'strategy': self.strategy,
			'notation': self.notation,
			'socketId': self.socketId,
			'isConfigured': self.isConfigured,
			'isRunning': self.isRunning,
			'value': self.value,
			'started_at': self.started_at,
			'stopped_at': self.stopped_at,
		}