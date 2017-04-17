
import operator
import random

import numpy as np

from deap import base
from deap import benchmarks
from deap import creator
from deap import tools

from deap_algorithm import DeapAlgorithm

#####Parameters#####
#Speed_max, speed_min
#Random_step
#Num_particles
#Num_itterations

class PSO(DeapAlgorithm):
    def __init__(self):
        super(PSO, self).__init__()
        
        self.bootstrap_deap()
            
    def bootstrap_deap(self):
        creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
        creator.create("Particle", list, fitness=creator.FitnessMax, speed=list, 
            smin=None, smax=None, best=None)

        self.toolbox = base.Toolbox()
        self.toolbox.register("particle", self.generate, size=2, pmin=0.0, pmax=1000.0)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.particle)
        self.toolbox.register("update", self.updateParticle)
    
    def generate(self, size, pmin, pmax):
        part = creator.Particle(random.uniform(pmin, pmax) for _ in range(size)) 
        part.speed = [random.uniform(-self.config['smax'], self.config['smax']) for _ in range(size)]
        return part

    def updateParticle(self, part, best):        
        u1 = (random.uniform(0, self.config['phi1']) for _ in range(len(part)))
        u2 = (random.uniform(0, self.config['phi2']) for _ in range(len(part)))
        v_u1 = map(operator.mul, u1, map(operator.sub, part.best, part))
        v_u2 = map(operator.mul, u2, map(operator.sub, best, part))
        part.speed = list(map(operator.add, part.speed, map(operator.add, v_u1, v_u2)))
        for i, speed in enumerate(part.speed):
            if speed < -self.config['smax']:
                part.speed[i] = -self.config['smax']
            elif speed > self.config['smax']:
                part.speed[i] = self.config['smax']
        part[:] = list(map(operator.add, part, part.speed))

    def run(self, case, logger):
        self.toolbox.register("evaluate", case.fitness)
        
        GEN = self.config['gen_count']
        POP_SIZE = self.config['pop_size']
        
        pop = self.toolbox.population(n=POP_SIZE)

        best = None
        for g in range(GEN):
            for part in pop:
                part.fitness.values = self.toolbox.evaluate(part)
                if not part.best or part.best.fitness < part.fitness:
                    part.best = creator.Particle(part)
                    part.best.fitness.values = part.fitness.values
                if not best or best.fitness < part.fitness:
                    best = creator.Particle(part)
                    best.fitness.values = part.fitness.values
            for part in pop:
                self.toolbox.update(part, best)

            if logger is not None:
                logger.updateLog(pop, g, len(pop))
    
        return pop,  best, best.fitness.values[0]
        
        
    def get_configs(self, case):
        configs = []
        
        config = {}
        
        pop_sizes = [200,160,100,80,50,40,20,10]
        phi1s = [1.0, 2.0]
        phi2s = [1.0, 2.0]
        smaxs = [20.0, 50.0]
        
        
        for pop_size in pop_sizes:
            for phi1 in phi1s:
                for phi2 in phi2s:
                    for smax in smaxs:
                        config['pop_size'] = pop_size
                        config['gen_count'] = case.getMaxEvalutions()/pop_size
                        if config['gen_count'] < 1:
                            continue
                        config['phi1'] = phi1
                        config['phi2'] = phi2
                        config['smax'] = smax
                        configs.append(config.copy())
                        
                    
        config['pop_size'] = case.getMaxEvalutions()
        config['gen_count'] = 1
        config['phi1'] = 2.0
        config['phi2'] = 2.0
        config['smax'] = 20.0
        configs.append(config.copy())
        
        return configs
