#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import logging
# import listener
from logging import Formatter, FileHandler
logging.basicConfig(filename="server.log", level=logging.DEBUG)
import os
import json
import database_manager
import hanashi
import numpy as np
import time
from gevent.pywsgi import WSGIServer
import memcache

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.debug = True

config = json.load(open('config.json'))

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

shared_memory = memcache.Client(['localhost'])
@app.route('/', methods=['GET', 'POST'])
def home():
    """
    GET: Loads a homepage to control children raspberries.
    POST: Receives info from children.
    """
    if request.method == "GET":
        database_manager.get_exsiting_batch()
        data = hanashi.get_home_data()
        online = hanashi.get_available_servers()
        genome_graph = hanashi.get_genome_graph()
        return render_template('pages/home.html', children=list(online), graph=data["graph"], genome=genome_graph)
    elif request.method == "POST":
        data = request.json
        database_manager.update_assignment(fitness=data["fitness"], request_id=data["request_id"])
        r = database_manager.get_exsiting_batch()
        if len(r)==0:
            #Updating status on cached memory
            set_response = shared_memory.set('batch_done', True)
            if set_response==0:
                logging.warn('set_response error')
        return "ok", 200

@app.route('/assignments', methods=['GET', 'POST'])
def assignments():
    if request.method == "GET":
        database_manager.get_exsiting_batch()
        assignments = database_manager.fetch_assignments()
        return render_template('pages/assignments.html', assignments=assignments)
    elif request.method == "POST":
        """
        Manually add new data.
        """
        data = request.json["matrix"] #list of lists
        hanashi.create_new_batch(np.array(data))
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/push', methods=['GET', 'POST'])
def push():
    """
    Pushes all assignments to the children servers.
    """
    if request.method == "GET":
        notification = hanashi.step()
        return notification, 200

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
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
