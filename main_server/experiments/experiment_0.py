import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
import sys
sys.path.append("../")
sys.path.append("../../testing")
sys.path.append(os.path.join(__location__,"../"))
sys.path.append(os.path.join(__location__,"../../testing"))
import spectra
import hanashi
import database_manager
import numpy as np
import json
import threading
import time
import datetime

"""
Used to check if reactors have identical responses.
"""

class setInterval:
    def __init__(self,interval,action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()):
            nextTime+=self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()

def stage_0_set(reactor_id,parameters="uniform",brightness=1):
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
            spectra.shadow_uniform(brightness,child["url"],0)

def arduino(command):
    hanashi.arduino_command(command)

def stage_0_read(reactor_id):
    children = None
    if reactor_id==None:
        children = database_manager.fetch_children()
    elif isinstance(reactor_id,list):
        children = database_manager.fetch_children_subset(id=reactor_id)
    hanashi.create_new_batch(np.array([[None] for i in range(len(reactor_id))]),servers=reactor_id)
    hanashi.step()

def set_time(t):
    config = {}
    with open("config.json") as c_file:
        config = json.load(c_file)
    config["time"] = t
    with open("config.json","w") as c_file:
        json.dump(config,c_file)

class control:
    def __init__(self):
        #Reactor
        self._reactors = None
        self.urls = None
        #Brilho
        self.obrilho = 0
        self.brilho = 0
        self.db = 1
        self.time_brilho = 15
        self.brilho_thread = None
        self.increase = True
        #Readings
        self.time_read = 15
        self.read_thread = None
    @property
    def reactors(self):
        return self._reactors
    @reactors.setter
    def reactors(self,value):
        if isinstance(value,list):
            self._reactors = value
            data = database_manager.fetch_children_subset(id=self._reactors)
            self.urls = {d["id"]:d["url"] for d in data}
            self.url_list = list(self.urls.values())
        else:
            print("Unrecognized format. Use a list of reactor id's.")
            self._reactors = None
            self.urls = None
    def set_brilho(self):
        hanashi.arduino_command(f"set(brilho,{self.brilho})",self.url_list)
    def set_brilho_inc(self):
        if self.brilho >= 100:
            self.increase = False
        elif self.brilho <= self.obrilho:
            self.increase = True
        self.brilho = self.brilho + self.db if self.increase else self.brilho - self.db
        self.set_brilho()
        print("Variable brilho updated:", self.brilho)
    def start_brilho_ladder(self):
        print("Brilho ladder start")
        self.obrilho = self.brilho
        self.brilho_thread = setInterval(self.time_brilho,self.set_brilho_inc)
    def read(self):
        print(datetime.datetime.now().strftime("[%D - %H:%M:%S]") + "Reading")
        stage_0_read(self.reactors)
        print(datetime.datetime.now().strftime("[%D - %H:%M:%S]") + "Read completed")
    def start_read(self):
        print("Read start", self.time_read)
        self.read_thread = setInterval(self.time_read,self.read)

def main():
    print("Booting")
    reactor_id = [2,3]
    hanashi.arduino_command("set(ar,50)")
    hanashi.arduino_command("set(brilho,10)")
    hanashi.arduino_command("set(cor,3)")

    

if __name__=="__main__":
    main()
    
    
