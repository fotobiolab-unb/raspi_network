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
from tools import hypercube_to_simplex
import numpy as np
import memcache
from waiting import wait
import logging
logging.basicConfig(filename="ga.log", level=logging.DEBUG)
shared_memory = memcache.Client(['localhost'])

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
        print(X.sum(axis=1))
        print("X", X)
        shared_memory.set('batch_done', False)
        batch = hanashi.create_new_batch(X)
        hanashi.step()
        wait(lambda : shared_memory.get('batch_done'))
        id = batch["id"]
        y = np.matrix(hanashi.get_from_id(id))
        print("Y", y)
        return np.array(y).ravel()

mask = np.array([[0.,1.] for i in range(4)])
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
            logging=True
            )
    ga.G[0]=np.zeros(ga.G[0].shape)
    ga.run()

if __name__=="__main__":
    # X = np.random.random_sample((4,3))
    # print(fitness(X))
    evolve(mode="surface")
