import json
import sqlite3
import numpy as np
import database_manager
import grequests
import os
import time
import logging
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
logging.basicConfig(filename="hanashi.log", level=logging.DEBUG)

"""
Module for communication among raspberry units
"""

config = json.load(open("config.json"))

def ping_to_children():
    """
    A get gate suffices to check the connection.
    url -> index 1
    id  -> index 0
    """
    children = database_manager.fetch_all_children()
    id_children = list(map(lambda x: x[0], children))
    to_ping = grequests.map([grequests.get(x[1]) for x in children])
    online = dict(filter(lambda x: x[1]!=None and x[1].ok,zip(id_children,to_ping)))
    return online

def get_from_id(id):
    """
    Returns processed fitness in ascending order
    """
    return database_manager.fitness_from_batch_id(id)

def create_new_batch(X):
    """
    X: numpy.array
        Chromossome population matrix where lines are chromossomes.
    """
    online_devices = ping_to_children()
    splits = np.array_split(X,len(online_devices))
    #Creating assignment
    batch_id = database_manager.get_new_batch_id()
    database_manager.create_assignments(zip(online_devices.keys(), splits),batch_id)
    return {'batch': database_manager.get_exsiting_batch(), 'id':batch_id}


def check_exsiting_batch():
    """
    If an assignment already exists, returns tuple of remaining items. Otherwise returns False.
    Never allow batch_id to be zero.
    """
    return database_manager.get_exsiting_batch()
    #This should already return a list of json elements or tuple

def update_assignment(request_id, fitness):
    """
    request_id is automatic on table assignment.
    """
    database_manager.update_assignment(request_id,fitness)

def step():
    """
    Used on push
    """
    #What in the absolute fuck I did here?
    unresolved = check_exsiting_batch()
    columns = ["id","batch_id","request_id","fitness","url","IP","chromossome_data"]
    data = []
    for packet in unresolved:
        p_dict = dict(zip(columns,packet))
        p_dict["time"] = config["time"]
        p_dict["server_addr"] = config["server_addr"]
        data.append(p_dict)
    requests = [grequests.post(x["url"], json = x) for x in data]
    logging.info(f"Sending packet: {data}")
    gmap = grequests.map(requests)
    """
    The output will be another dictionary whose values will be used to update the database. The result is caught by a get in Flask.
    """
    success = list(filter(lambda x: x!=None and x.ok,gmap))
    notification = f"Executed batch post, {len(success)} out of {len(requests)} returned 200."
    logging.info(notification)
    return notification

def get_home_data():
    data = database_manager.get_home_data()
    #plot
    y = data["graph"]
    fig = go.Figure(data=go.Scatter(y=y))
    fig.update_layout(template="plotly_dark")
    data["graph"] = plot(fig,include_plotlyjs=False, output_type='div')
    return data

if __name__=="__main__":
    a = np.random.randint(0,10,(5,3))
    print(a)
    print(create_new_batch(a))
