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
    GET: Loads a homepage to controll children raspberries.
    POST: Receives info from children.
    """
    if request.method == "GET":
        children = database_manager.fetch_children()
        recent_data = database_manager.fetch_recent_data()
        return render_template('pages/home.html', children=children, recent_data=recent_data)

@app.route('/assignments', methods=['GET', 'POST'])
def assignments():
    if request.method == "GET":
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
