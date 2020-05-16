# from models import Bot
from app import db, socketio


@socketio.on('message')
def handle_message(data):
	print('===================== received message: ' + str(data))

@socketio.on('pending-config')
def pending_config(data):
	print('================  pending-config : ' + str(data))
	if data['type']=='bot':
		socketio.emit('pending-config',{'sid':data['sid'],'prompt_text':data['prompt_text'],'completer':data['completer']})
	elif data['type']=='app':
		socketio.send({'command':'pending-config','sid':data['sid'] ,'config_data': data['config_data']})

@socketio.on('connect')
def connect():
	print('==================== new client is connected! ')

@socketio.on('connected')
def connected(data):
	print('==================== sid: ' + str(data['sid']))
	if data['type']=='bot':
		socketio.emit('bot-connected',{'sid':data['sid']})
	elif data['type']=='app':
		electron_sid = data['sid']
@socketio.on('disconnect')
def disconnect():
	print('==================== a client is disconnected!')