from flask import request, jsonify
from models import Bot
from app import app, db, socketio
import subprocess
import os
import json


@app.route('/')
def index():
	return "Hello, world!"

@app.route('/getBots', methods=['GET'])
def getBots():
	return jsonify([i.serialize for i in Bot.query.all()])

@app.route('/getBotsByStrategy', methods=['GET','POST'])
def getBotsByStrategy():
	data = request.json
	# bots = Bot.query.filter_by(strategy=data['strategy']).all()
	# bots = db.session.query(Bot).filter(Bot.strategy==data['strategy']).all()
	# print(bots)
	return jsonify([i.serialize for i in Bot.query.filter_by(strategy=data['strategy']).all()])

@app.route('/create', methods=['GET','POST'])
def create():
	data = request.json
	bot = Bot(name=data['name'],strategy=data['strategy'],notation=data['notation'])
	db.session.add(bot)
	db.session.commit()
	os.system("gnome-terminal -e 'sh scripts/create_bot.sh %r'"%bot.id)
	return json.dumps(bot.to_dict())

@app.route('/updateBot', methods=['GET','POST'])
def updateBot():
	data = request.json
	bot = Bot.query.filter_by(id=data['bot_id']).first()
	bot.socketId = data['socketId']
	db.session.commit()
	return json.dumps(bot.to_dict())

@app.route('/botConfigured', methods=['GET','POST'])
def botConfigured():
	data = request.json
	bot = Bot.query.filter_by(id=data['id']).first()
	bot.isConfigured = True
	db.session.commit()
	return json.dumps(bot.to_dict())

@app.route('/delete',methods=['GET','POST'])
def delete():
	data = request.json
	socketio.send({'command':'exit','sid':data['socketId']})
	os.system("gnome-terminal -e 'sh scripts/delete_bot.sh %r'"%data['id'])
	bot = Bot.query.filter_by(id=data['id']).first()
	db.session.delete(bot)
	db.session.commit()
	return "a bot was removed!"

@app.route('/start', methods=['GET','POST'])
def start():
	data = request.json
	print('============send a command : start,  sid: ' + data['socketId'])
	socketio.send({'command':'start','sid':data['socketId']})
	bot = Bot.query.filter_by(id=data['id']).first()
	bot.isRunning = True
	db.session.commit()
	return json.dumps(bot.to_dict())

@app.route('/stop',methods=['GET','POST'])
def stop():
	data = request.json
	print('============send a command : stop  sid: ' + data['socketId'])
	socketio.send({'command':'stop','sid':data['socketId']})
	bot = Bot.query.filter_by(id=data['id']).first()
	bot.isRunning = False
	db.session.commit()
	return json.dumps(bot.to_dict())

@app.route('/config',methods=['GET','POST'])
def config():
	data = request.json
	print('============send a command : config  sid: ' + data['socketId'],str(data))
	socketio.send({'command':'config','sid':data['socketId'],'strategy':data['strategy']})
	return "config command has been sent!"

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST','GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'