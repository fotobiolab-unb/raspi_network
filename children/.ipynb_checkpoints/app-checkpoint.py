#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify, send_from_directory
import logging
# import listener
from logging import Formatter, FileHandler
import os
import json
import database_manager
import hanashi
import asyncio
from sync import sync
from multiprocessing import Process
from gevent.pywsgi import WSGIServer

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.debug = True

config = json.load(open('config.json'))

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    GET: Loads a homepage to control children raspberries.
    POST: Receives info from children.
    """
    if request.method == "GET":
        return "ok", 200
    elif request.method == "POST":
        """
        Update information to arduino and save to database.
        """
        print(request)
        batch = request.json
        #Do whatever with the data
        id = batch["id"]
        data = batch["chromossome_data"]
        batch_id = batch["batch_id"]
        request_id = batch["request_id"]
        #updating constants
        server_url = batch["server_addr"]
        time = batch["time"]
        try:
            """
            Trying to update config from main_server.
            Otherwise, use old configuration.
            """
            config = json.load(open("config.json"))
            #updating config in case it changes on the main server
            config["time"] = time
            config["server_addr"] = server_url
            json.dump(config,open("config.json", "w"))
        except:
            pass
        #-----------------
        if request_id != None:
            database_manager.create_assignment(id,data,batch_id,request_id)
        #p = Process(target=sync())
        #p.start()
        #hanashi.static_set((id,batch_id,request_id,0,data))
        hanashi.static_set(batch)
        return "ok", 200

@app.route('/listen', methods=['GET', 'POST'])
def listen():
    """
    Update information to arduino and save to database.
    """
    if request.method == "POST":
        batch = request.json()
        #Do whatever with the data
        id = batch["id"]
        data = batch["chromossome"]
        batch_id = batch["batch_id"]
        request_id = batch["request_id"]
        #updating constants
        server_url = batch["server_addr"]
        time = batch["time"]
        config = json.load(open("config.json"))
        config["time"] = time
        config["server_addr"] = server_url
        json.dump(config,open("config.json", "w"))
        #-----------------
        database_manager.create_assignment(id,data,batch_id,request_id)
        p = Process(target=sync)
        p.start()
        return "ok", 200



if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#


if __name__ == '__main__':
    def serve_forever(s):
        s.serve_forever()
    virt = json.load(open('virtual_server_config.json'))
    if virt["run_virtual"]:
        servers = [WSGIServer(('', port), app) for port in virt["ports"]]
        for server in servers:
            Process(target=serve_forever, args=(server,)).start()
    else:
        http_server = WSGIServer(('', 2001), app)
        http_server.serve_forever()
