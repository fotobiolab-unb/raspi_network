import sys
sys.path.append("../main_server/")
import numpy as np
import json
import hanashi

def uniform(alpha):
    with open("../data/spectra/neutral_spectrum_components.json") as f:
        coefficients = json.load(f)["coefficients"]
        coefficients = np.array(coefficients)
        coefficients = alpha*coefficients
        hanashi.create_new_batch(coefficients.reshape((1,coefficients.shape[0])))
        hanashi.step()