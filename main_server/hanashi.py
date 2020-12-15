import json
import sqlite3
import numpy as np
import database_manager
#import grequests
import os
import time
import logging
import requests
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
    #to_ping = grequests.map([grequests.get(x[1]) for x in children])
    to_ping = []
    for x in children:
        try:
            to_ping.append(requests.get[x[1]])
        except:
            to_ping.append(None)
    online = dict(filter(lambda x: x[1]!=None and x[1].ok,zip(id_children,to_ping)))
    return online

def get_available_servers():
    online = ping_to_children()
    online = list(filter(lambda x: online[x].ok,online.keys()))
    return database_manager.fetch_children_subset(online)

def get_from_id(id,**kwargs):
    """
    Returns processed fitness in ascending order
    """
    return database_manager.fitness_from_batch_id(id, **kwargs)

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
    #Requests = [grequests.post(x["url"], json = x) for x in data]
    Requests = [requests.post(x["url"], json = x) for x in data]
    logging.info(f"Sending packet: {data}")
    #gmap = grequests.map(requests)
    gmap = Requests
    """
    The output will be another dictionary whose values will be used to update the database. The result is caught by a get in Flask.
    """
    success = list(filter(lambda x: x!=None and x.ok,gmap))
    notification = f"Executed batch post, {len(success)} out of {len(requests)} returned 200."
    logging.info(notification)
    return unresolved

def get_best_genome_data(n=3):
    """
    Creates a set of stacked graphs.
    """
    genome_graph_names = database_manager.get_best_individual(n)
    raw = np.array([database_manager.get_genome_graph(x) for x in genome_graph_names])
    genome_graph = np.array([[raw[j,:,:i].sum(axis=1) for i in range(1,len(raw[0][0])+1)] for j in range(len(raw))])
    # maximum, minimum = genome_graph.max(axis=1), genome_graph.min(axis=1)
    # maximum = np.repeat(maximum[:,np.newaxis,:],genome_graph.shape[1],axis=1)
    # minimum = np.repeat(minimum[:,np.newaxis,:],genome_graph.shape[1],axis=1)
    # genome_graph = (genome_graph-minimum)/(maximum-minimum) if (maximum-minimum).sum()!=0 else genome_graph
    genome_graph = genome_graph.tolist()
    genome_graph_names = ["R"+str(x) for x in genome_graph_names]
    return genome_graph_names, genome_graph

def shadow_send(chromossome, address, time):
    """
    Sends paramaters directly to target reactor without saving data to a queue.
    """
    packet = {
        "id": None,
        "chromossome_data": list(chromossome),
        "batch_id": None,
        "time": time,
        "request_id": None,
        "server_addr": config["server_addr"]
        
    }
    requests.post(address, json=packet)

if __name__=="__main__":
    a = np.random.randint(0,10,(5,3))
    print(a)
    print(create_new_batch(a))
