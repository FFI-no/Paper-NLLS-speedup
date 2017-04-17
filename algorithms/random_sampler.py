from deap_algorithm import DeapAlgorithm

import numpy as np
import random


from deap import base
from deap import creator
from deap import tools

####Parameter
#Num_evaluations



class RandomSampler(DeapAlgorithm):
    def __init__(self):
        super(RandomSampler, self).__init__()
        
        self.bootstrap_deap()

    def _generate_individual(self):
        ind = creator.Individual(random.uniform(0,self.config['grid_size'][i]) for i in range(2)) 
        return ind

    def bootstrap_deap(self):
        creator.create("FitnessMinError", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMinError)

        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", self._generateIndividual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("select", tools.selBest)
    
    def run(self, case, logger):
        self.config['grid_size'] = case.config['grid_size']
        
        self.toolbox.register("evaluate", case.fitness)
        
        #Create a population of random individuals
        pop = self.toolbox.population(n=case.getMaxEvalutions())
        
        # Evaluate the individuals
        fitnesses = self.toolbox.map(self.toolbox.evaluate, pop)
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
            
        #Pick the best individual
        best_ind = tools.selBest(pop, 1)[0]
        
        if logger is not None:
            logger.updateLog( pop, 0, len(pop))
        
        return pop, best_ind, best_ind.fitness.values[0]
        

    def get_configs(self, case):
        configs = []
        
        config = {}
        configs.append(config)
        
        return configs
