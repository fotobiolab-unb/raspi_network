#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import logging
# import listener
from logging import Formatter, FileHandler
import os
import json
import database_manager
import hanashi
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
        children = database_manager.fetch_children()
        recent_data = database_manager.fetch_recent_data()
        database_manager.get_exsiting_batch()
        return render_template('pages/home.html', children=children, recent_data=recent_data)
    elif request.method == "POST":
        data = request.json
        database_manager.update_assignment(fitness=data["fitness"], request_id=data["request_id"])
        database_manager.get_exsiting_batch()
        return "ok", 200

@app.route('/assignments', methods=['GET', 'POST'])
def assignments():
    if request.method == "GET":
        database_manager.get_exsiting_batch()
        assignments = database_manager.fetch_assignments()
        return render_template('pages/assignments.html', assignments=assignments)

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

# # Default port:
# if __name__ == '__main__':
#     app.run()


if __name__ == '__main__':
    http_server = WSGIServer(('', 2000), app)
    http_server.serve_forever()
