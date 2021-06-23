import os
import sys
dir_name = os.path.dirname(__file__)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
sys.path.append(__location__)
import json
import sqlite3
import numpy as np
import database_manager
#import grequests
import time
import logging
import requests
from urllib.parse import urljoin
logging.basicConfig(filename="hanashi.log", level=logging.DEBUG)

"""
Module for communication among raspberry units
"""

config = json.load(open(os.path.join(dir_name,"config.json")))

def ping_to_children():
    """
    A get gate suffices to check the connection.
    url -> index 1
    id  -> index 0
    """
    children = database_manager.fetch_all_children()
    id_children = list(map(lambda x: x["id"], children))
    #to_ping = grequests.map([grequests.get(x[1]) for x in children])
    to_ping = []
    for x in children:
        try:
            to_ping.append(requests.get(x["url"]))
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

def create_new_batch(X,servers=False):
    """
    X: numpy.array
        Chromossome population matrix where lines are chromossomes.
    servers: bool or list
        List of reactor id's to send. Otherwise X is distributed along all online devices.
    """
    servers = servers if isinstance(servers,list) else ping_to_children().keys()
    splits = np.array_split(X,len(servers))
    #Creating assignment
    batch_id = database_manager.get_new_batch_id()
    database_manager.create_assignments(zip(servers, splits),batch_id)
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
    unresolved = check_exsiting_batch()
    data = []
    for packet in unresolved:
        packet["time"] = config["time"]
        packet["server_addr"] = config["server_addr"]
        data.append(packet)
    Requests = [requests.post(x["url"], json = x) for x in data]
    print(f"Sending packets...")
    gmap = Requests
    """
    The output will be another dictionary whose values will be used to update the database. The result is caught by a get in Flask.
    """
    success = list(filter(lambda x: x!=None and x.ok,gmap))
    notification = f"Executed batch post, {len(success)} out of {len(Requests)} returned 200."
    print(notification)
    return unresolved

def to_num(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return float('nan')

def get_best_genome_data(n=3):
    """
    Creates a set of stacked graphs.
    """
    genome_graph_names = database_manager.get_best_individual(n)
    raw = np.array([list(map(to_num,database_manager.get_genome_graph(x))) for x in genome_graph_names])
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

def arduino_command(command, servers = False, wait_return = False):
    """
    Sends a command to connected arduino to a list of servers.
    
    `servers` must be a list of urls. Otherwise it sends the command to all available servers.
    `wait_return`: If False it will just send a command. Otherwise it waits for a response.
    """
    
    servers = list(map(lambda x: x["url"],get_available_servers())) if not servers else servers
    
    packet = {
        "id": None,
        "command": command,
        "batch_id": None,
        "request_id": None,
        "server_addr": config["server_addr"],
        "return": wait_return
    }
    
    for server in servers:
        url = urljoin(server,"/command")
        r = requests.post(url, json=packet)
        if r!=None:
            print(r.status_code,url)
            print(r.json())

if __name__=="__main__":
    a = np.random.randint(0,10,(5,3))
    print(a)
    print(create_new_batch(a))
