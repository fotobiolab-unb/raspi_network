import sys
sys.path.append("../")
sys.path.append("../testing")
import spectra
import hanashi
import database_manager
import numpy as np
import json
import os

def stage_0_set(reactor_id,parameters="uniform"):
    """
    Sends a initial set of parameters and only reads thereafter.
    reactor_id: list of urls to ractors.
    parameters: list of parameters or string to parameter profile
    """
    
    children = database_manager.fetch_children_subset(id=reactor_id)

    #Setting parameters
    for child in children:
        if isinstance(parameters,list):
            hanashi.shadow_send(parameters,child["url"],0)
        elif parameters=="uniform":
            spectra.shadow_uniform(1,child["url"],0)

def stage_0_read(reactor_id):
    children = database_manager.fetch_children_subset(id=reactor_id)
    hanashi.create_new_batch(np.array([None for i in range(reactor_id)]),servers=reactor_id)

def set_time(t):
    config = {}
    with open("../config.json") as c_file:
        config = json.load(c_file)
    config["time"] = t
    with open("../config.json","w") as c_file:
        json.dump(config,c_file)

if __name__=="__main__":
    reactor_id = [2]
    if os.path.exists("init.dat"):
        stage_0_read(reactor_id)
    else:
        set_time(0)
        stage_0_set(0)    
    
    
