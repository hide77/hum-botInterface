import socketio
from prompt_toolkit.document import Document
from hummingbot.core.utils.trading_pair_fetcher import TradingPairFetcher
from hummingbot.client.settings import EXCHANGES
import asyncio

sio = socketio.AsyncClient()

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def setHummingInstance(humming):
    global hb
    hb = humming

def get_completer():
    trading_pair_fetcher = TradingPairFetcher.get_instance()
    prompt_text = hb.app.prompt_text
    if "exchange name" in prompt_text:
        return list(EXCHANGES)
    elif "trading pair" in prompt_text and trading_pair_fetcher.ready:
        market = None
        for exchange in EXCHANGES:
            if exchange in prompt_text:
                market = exchange
                break
        return trading_pair_fetcher.trading_pairs[market] if market!=None else []
    else:
        return []

async def run_command(command):
    print("command running: " + command)
    hb.app.input_field.buffer.document = Document(text=command, cursor_position=len(command))
    hb.app.input_field.buffer.validate_and_handle()
    await asyncio.sleep(0.2)

async def start_config(strategy):
    await run_command('config')
    await run_command('aaa')
    await run_command('aaa')
    await run_command(strategy)
    await run_command('create')
    await pending_config('')

async def pending_config(config_data):
    await run_command(config_data)
    prompt_text = hb.app.prompt_text
    completer = get_completer()
    print("completer : " + str(completer))
    await sio.emit('pending-config', {'sid':sio.sid,'type':'bot', 'prompt_text':prompt_text,'completer':completer})

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@sio.event
async def message(data):
    print("message received!" + str(data))
    if data['sid'] != sio.sid:
        return
    if data['command']=='start' or data['command']=='stop' or data['command']=='exit':
        await run_command(data['command'])
    elif data['command']=='config':
        await start_config(data['strategy'])
    elif data['command']=='pending-config':
        await pending_config(data['config_data'])

@sio.event
async def connect():
    print("connected!")
    print(sio.sid)
    await sio.emit('connected', {'sid':sio.sid, 'type':'bot'})

@sio.event
async def connect_error():
    print("connection error!")    

@sio.event
async def disconnect():
    print("disconnected")