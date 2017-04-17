

from algorithm import Algorithm

import numpy as np
import random

from deap import creator

class DeapAlgorithm(Algorithm):
    def __init__(self):
        super(DeapAlgorithm, self).__init__()
        self.config = {}
        
    def _generateIndividual(self):
        ind = creator.Individual(random.uniform(0,self.config['grid_size'][i]) for i in range(2)) 
        return ind
        
    def set_config(self, config):
        self.config = config.copy()
