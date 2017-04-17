
import numpy as np

from landscapes import FitnessLandscape




def visualizeCase(case):
    
    @np.vectorize
    def fn(x,y) :
        return case.fitness(np.array([x,y]))[0]

    fland = FitnessLandscape(case.config["grid_size"], [20,20], fn, None)
    
    return fland
