import sqlite3
import json
import requests
import os
import time

"""
Responsible for executing pending assignments.
Executes under the following conditions:
    - Computer starts (as a service)
    - A call to the /listen route is done
"""

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

config = json.load(open(os.path.join(__location__,'config.json')))

def send(data):
    """
    Sends directly back to main server without querying the database.
    
    Args:
        data (dict): Data that will be sent back as JSON.
    """
    print("Sending Assignment")
    print("[SENDING]", data)
    url = config["server_addr"]
    r = requests.post(url,json=data)
    while not r.ok:
        print("Send didn't work. Trying again in 5 seconds.","Error code", r.status_code)
        time.sleep(5)
        r = requests.post(url,json=data)
