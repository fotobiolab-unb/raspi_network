#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import logging
# import listener
from logging import Formatter, FileHandler
logging.basicConfig(filename="server.log", level=logging.DEBUG)
import os
import simplejson as json
import database_manager
import hanashi
import numpy as np
import time
from gevent.pywsgi import WSGIServer
import memcache
import time

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.debug = True

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

config = json.load(open(os.path.join(__location__,'config.json')))

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
        #data = hanashi.get_home_data()#
        data = database_manager.get_home_data()
        #online = hanashi.get_available_servers()
        #online = list(map(lambda x: list(x.values()), online))
        online=[]
        try:
            genome_names, genome_graph = hanashi.get_best_genome_data()
        except:
            genome_names, genome_graph = [], [[[0]]]
        columns = database_manager.get_column_names()
        return render_template('pages/home.html', children=list(online), graph=data["graph"], genome_name=genome_names, genome_graph=genome_graph, columns=columns)
    elif request.method == "POST":
        data = request.json
        print("[RECEIVED]", data)
        database_manager.update_assignment(fitness=data, request_id=data["request_id"])
        r = database_manager.get_exsiting_batch()
        if len(r)==0:
            #Updating status on cached memory
            set_response = shared_memory.set('batch_done', True)
            if set_response==0:
                logging.warn('set_response error')
        return "ok", 200

@app.route('/graph')
def graph():
    column = request.args.get("column")
    limit = int(request.args.get("limit"))
    reactor_id = int(request.args.get("reactor_id"))
    data = database_manager.get_graph(column=column, limit=limit, reactor_id=reactor_id)
    print("DATA GRAPH", data)
    return json.dumps({'graph':data}, ignore_nan=True), 200, {'ContentType':'application/json'}

@app.route('/update_home_data')
def update_home_data():
    data = database_manager.get_home_data()["graph"]
    print("DATA", data)
    #online = hanashi.get_available_servers()
    #online = list(map(lambda x: list(x.values()), online))
    online = []
    try:
        genome_names, genome_graph = hanashi.get_best_genome_data()
    except:
        genome_names, genome_graph = [], [[[0]]]
    response = {
        "fitness_graph":data,
        "online_servers":online,
        "genome_names":genome_names,
        "genome_graph":genome_graph
    }
    return json.dumps(response, ignore_nan=True), 200, {'ContentType':'application/json'}

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
    http_server = WSGIServer(("0.0.0.0", 5000), app)
    print("Open on port 5000")
    http_server.serve_forever()
