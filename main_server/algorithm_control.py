"""
Path for gapy module must be specified in the config.json file
gapy: https://github.com/icarosadero/gapy
"""

import sys
import json
import hanashi
config = json.load(open("config.json"))
sys.path.append(config["gapy_path"])
from gapy import GA
from gapy2 import GA as GA2
from tools import hypercube_to_simplex
import numpy as np
import memcache
from waiting import wait
import logging
logging.basicConfig(filename="ga.log", level=logging.DEBUG)
shared_memory = memcache.Client(['localhost'])
np.set_printoptions(precision=3)

def fitness(X_cube, mode="volume", high=None, low=None, E=1):
        """
        mode: str
            -volume: expects the energy constranint to be smaller than a threshold
            -surface: expects the energy constraint to be equal to a threshold
        """
        high = np.ones(X_cube.shape[1]) if not high else high
        low = np.zeros(X_cube.shape[1]) if not low else low
        scale = np.array([high,low])
        if mode=="volume":
            X = hypercube_to_simplex(X_cube.copy(),scale)
        elif mode=="surface":
            #In this case there is a dimension reduction
            X = hypercube_to_simplex(X_cube.copy(),scale)
            u = E - X.sum(axis=1)
            u = u.reshape((u.shape[0], 1))
            X = np.hstack([u,X])
        print(X)
        shared_memory.set('batch_done', False)
        batch = hanashi.create_new_batch(X)
        R = hanashi.step()
        wait(lambda : shared_memory.get('batch_done'))
        id = batch["id"]
        Y = hanashi.get_from_id(id, return_request_id=True)
        Y = {u[1]:u[0] for u in Y}
        y = [Y[k] for k in np.array(R)[:,2].astype(int)]
        return np.array(y).ravel()

mask = np.array([[0,1.] for i in range(4)])
#mask = np.array([[-10.,10.] for i in range(4)])
def evolve(mode, *args, **kwargs):
    ga = GA(
            population_size=8,
            chromosome_size=4,
            resolution=8,
            iterations=10,
            elitism=True,
            mutation=0.2,
            fitness=lambda x: fitness(x, mode),
            range_mask=mask,
            has_mask=True,
            time_print=.5,
            logging=True,
            maximize=True
            )
    ga.G[0]=np.zeros(ga.G[0].shape)
    ga.run()

def evolve2(mode, *args, **kwargs):
    ga = GA2(
        population_size = 8,
        mutation_probability = 0.2,
        generations = 10,
        resolution = 8,
        ranges = mask,
        elitism = 1
    )
    ga.f = lambda x: fitness(x, mode)
    ga.run()



if __name__=="__main__":
    # X = np.random.random_sample((4,3))
    # print(fitness(X))
    #evolve(mode="surface")
    #evolve2(mode="surface")
