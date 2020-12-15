import sqlite3
import hanashi
import database_manager
import logging
import json
import requests

"""
Responsible for executing pending assignments.
Executes under the following conditions:
    - Computer starts (as a service)
    - A call to the /listen route is done
"""

logging.basicConfig(filename="operator.log", level=logging.DEBUG)
config = json.load(open("config.json"))

def sync():
    print("sync running")
    for assignment in database_manager.get_exsiting_batch_gen():
        #order: id,batch_id,request_id,fitness,chromossome_data
        print(f"Executing {assignment}")
        logging.info(f"Executing {assignment}")
        hanashi.static_set(assignment)
        logging.info("ok")

    #Attempting to send done assignments
    for assignment in database_manager.to_be_sent():
        print(f"Sending {assignment}")
        logging.info(f"Sending {assignment}")
        #Posting back to main server
        data = dict(zip(["id","batch_id", "request_id", "fitness", "chromossome_data"], assignment))
        url = config["server_addr"]
        r = requests.post(url,json=data)
        if r.ok:
            logging.info("ok")
            database_manager.update_assignment(fitness=data["fitness"],request_id=data["request_id"], sync=1)

def sync_send():
    print("Sending Assignments")
    #Attempting to send done assignments
    for assignment in database_manager.to_be_sent():
        print(f"Sending {assignment}")
        logging.info(f"Sending {assignment}")
        #Posting back to main server
        data = dict(zip(["id","batch_id", "request_id", "fitness", "chromossome_data"], assignment))
        url = config["server_addr"]
        r = requests.post(url,json=data)
        if r.ok:
            logging.info("ok")
            database_manager.update_assignment(fitness=data["fitness"],request_id=data["request_id"], sync=1)

if __name__ == "__main__":
    sync()
