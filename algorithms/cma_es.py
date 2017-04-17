from deap_algorithm import DeapAlgorithm

import numpy as np
import os
import random

from deap import algorithms
from deap import base
from deap import benchmarks
from deap import cma
from deap import creator
from deap import tools

class CMAES(DeapAlgorithm):
    def __init__(self):
        super(CMAES, self).__init__()
    
        self.bootstrap_deap()
    
    def bootstrap_deap(self):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        self.toolbox = base.Toolbox()
        
    def run(self, case, logger):
        self.toolbox.register("evaluate", case.fitness)
        # The cma module uses the numpy random number generator
        np.random.seed(random.randint(0,10000))
        self.config['centroid'] = np.multiply(np.random.rand(1,2), np.array(case.config['grid_size'])).flatten().tolist()

        # The CMA-ES algorithm takes a population of one individual as argument
        # The centroid is set to a vector of 5.0 see http://www.lri.fr/~hansen/cmaes_inmatlab.html
        # for more details about the rastrigin and other tests for CMA-ES    
        strategy = cma.Strategy(centroid=self.config['centroid'], sigma=self.config['sigma'], lambda_=self.config['pop_size'])
        self.toolbox.register("generate", strategy.generate, creator.Individual)
        
        self.gen = 0
        def hook(*args, **kwargs):
            pop = args[0]
            self.gen += 1
            
            logger.updateLog(pop, self.gen, len(pop))
            return strategy.update(*args, **kwargs)
            
        self.toolbox.register("update", hook)

        hof = tools.HallOfFame(1)
       
        # The CMA-ES algorithm converge with good probability with those settings
        pop, logger.logbook = algorithms.eaGenerateUpdate(self.toolbox, ngen=self.config['gen_count'], stats=logger.stats, halloffame=hof, verbose=not logger.silent)
        
        return pop, hof[0], hof[0].fitness.values[0]

    def get_configs(self, case):
        configs = []
        
        config = {}
        
        sigmas = [100.0, 125.0, 150.0, 200.0]
        pop_sizes = [200,160,100,80,50,40,20,10]
        
        for pop_size in pop_sizes:
            for sigma in sigmas:
                config['pop_size'] = pop_size
                config['gen_count'] = case.getMaxEvalutions()/pop_size
                config['sigma'] = sigma
                if config['gen_count'] < 1:
                    continue
                configs.append(config.copy())
        
        
        config['pop_size'] = case.getMaxEvalutions()
        config['gen_count'] = 1
        config['sigma'] = 125.0
        configs.append(config.copy())
        
        return configs
