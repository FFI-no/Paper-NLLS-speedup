from deap_algorithm import DeapAlgorithm

import numpy as np
import array
import random

from deap import algorithms
from deap import base
from deap import benchmarks
from deap import cma
from deap import creator
from deap import tools

class DiffEvo(DeapAlgorithm):
    def __init__(self):
        super(DiffEvo, self).__init__()
    
        self.bootstrap_deap()
    
    def bootstrap_deap(self):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMin)

        self.toolbox = base.Toolbox()
        self.toolbox.register("attr_float", random.uniform, 0, 1000)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_float, 2)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("select", tools.selRandom, k=3)
    
    def run(self, case, logger):
        self.toolbox.register("evaluate", case.fitness)
        
        # Differential evolution parameters
        CR = self.config['cr']
        F = self.config['f']
        MU = self.config['pop_size']
        NGEN = self.config['gen_count']
        
        pop = self.toolbox.population(n=MU);
        hof = tools.HallOfFame(1)
        
        # Evaluate the individuals
        fitnesses = self.toolbox.map(self.toolbox.evaluate, pop)
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
        hof.update(pop)
        
        if logger is not None:        
            logger.updateLog(pop, 0, len(pop))
        
        for g in range(1, NGEN-1):
            for k, agent in enumerate(pop):
                a,b,c = self.toolbox.select(pop)
                y = self.toolbox.clone(agent)
                index = random.randrange(2)
                for i, value in enumerate(agent):
                    if i == index or random.random() < CR:
                        y[i] = a[i] + F*(b[i]-c[i])
                y.fitness.values = self.toolbox.evaluate(y)
                if y.fitness > agent.fitness:
                    pop[k] = y
            hof.update(pop)
            
            if logger is not None:
                logger.updateLog(pop, g, len(pop))
        
        return pop, hof[0], hof[0].fitness.values[0]
        
    def get_configs(self, case):
        configs = []
        
        config = {}
        pop_sizes = [200,160,100,80,50,40,20,10]
        crs = [0.25, 0.50]
        fs = [0.5, 1.0]
        
        for pop_size in pop_sizes:
            for cr in crs:
                for f in fs:
                    config['pop_size'] = pop_size
                    config['gen_count'] = case.getMaxEvalutions()/pop_size
                    if config['gen_count'] < 1:
                        continue
                    config['cr'] = cr
                    config['f'] = f
                    configs.append(config.copy())
        
        config['pop_size'] = case.getMaxEvalutions()
        config['gen_count'] = 1
        config['cr'] = 0.25
        config['f'] = 1.0
        configs.append(config.copy())
        
        return configs
