import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.sqlite"))

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


if __name__ == "__main__":
	from socket_events import *
	from routes import *
	db.create_all()
	socketio.run(app, debug=False)
	# app.run(debug=True)
