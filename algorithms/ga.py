
import random
import numpy as np
#import multiprocessing

from deap import base
from deap import creator
from deap import tools

from deap_algorithm import DeapAlgorithm

#Parameters:

#Crossoverprob.
#Mutation prob.
#Number of generations
#Population size

class GA(DeapAlgorithm):
    def __init__(self):
        super(GA, self).__init__()
        
        #Initialized DEAP for GA optimization
        self.bootstrap_deap()
        

    def bootstrap_deap(self):
        creator.create("FitnessMinError", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMinError)

        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", self._generateIndividual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        #self.toolbox.register("mate", tools.cxOnePoint)
        self.toolbox.register("mate", self.mate)
        #self.toolbox.register("mutate", tools.mutGaussian, mu=0.0, sigma=50.0 , indpb=0.5)
        self.toolbox.register("select", tools.selTournament, tournsize=2)
        
    def mate(self, first, second):
        u1 = random.random()
        u2 = random.random()
        delta = np.array(second) - np.array(first)
        
        child1 = np.array(first) + u1 * delta
        child2 = np.array(first) + u2 * delta
        
        return creator.Individual(child1), creator.Individual(child2)
        
        
    def run(self, case, logger):
        self.config['grid_size'] = case.config['grid_size']
        
        self.toolbox.register("evaluate", case.fitness)
        self.toolbox.register("mutate", tools.mutGaussian, mu=0.0, sigma=self.config['mut_sigma'], indpb=0.5)
        
        
        #Load config parameters
        POP_SIZE = self.config['pop_size']
        CXPB = self.config['cxpb']
        MUTPB = self.config['mutpb']
        NGEN = self.config['gen_count']
        ELITES = self.config['elites']
        
        #Conduct optimization
        pop = self.toolbox.population(n=POP_SIZE)
        
        # Evaluate the entire population
        fitnesses = list(map(self.toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
        
        if logger is not None:
            logger.updateLog(pop, 0, len(pop))
            
        eval_count = len(pop)
        
        # Begin the evolution
        for g in range(NGEN-1):
            
            # Select the next generation individuals
            offspring = self.toolbox.select(pop, len(pop)-ELITES)
            # Clone the selected individuals
            offspring = list(map(self.toolbox.clone, offspring))
        
            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    self.toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < MUTPB:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values
        
            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            
            elites = list(map(self.toolbox.clone, tools.selBest(pop, ELITES)))
            
            if logger is not None:
                logger.updateLog(pop, g, len(invalid_ind))
                
            if eval_count+len(invalid_ind) > case.getMaxEvalutions():
                break
            
            # The population is entirely replaced by the offspring (- elites)
            pop[:ELITES] = elites
            pop[ELITES:] = offspring
                
        
        best_ind = tools.selBest(pop, 1)[0]

        return pop, best_ind, best_ind.fitness.values[0]
        

    #def get_configs(self, case):
        #configs = []
        
        #config = {}
        #config['cxpb'] = 0.6
        #config['mutpb'] = 0.1
   
        
        
        #pop_sizes = [200,160,100,80,50,40,20,10]
        #for pop_size in pop_sizes:
            #config['pop_size'] = pop_size
            #config['gen_count'] = case.getMaxEvalutions()/pop_size
            #config['elites'] = max(2, int(pop_size*0.05))
            #configs.append(config.copy())
        
        #return configs
    def get_configs(self, case):
        configs = []
        
        config = {}
        
        pop_sizes = [200,160,100,80,50,40,20,10]
        cx_probs = [0.4, 0.6]
        mut_probs = [0.1,0.2]
        mut_sigmas = [25.0, 50.0]
        
        
    
        for pop_size in pop_sizes:
            for cxpb in cx_probs:
                for mutpb in mut_probs:
                    for mut_sigma in mut_sigmas:
                        config['pop_size'] = pop_size
                        config['gen_count'] = case.getMaxEvalutions()/pop_size
                        if config['gen_count'] < 1:
                            continue
                        config['elites'] = max(2, int(pop_size*0.05))
                        config['cxpb'] = cxpb
                        config['mutpb'] = mutpb
                        config['mut_sigma'] = mut_sigma
                        configs.append(config.copy())
                    
        pop_size = case.getMaxEvalutions()
        config['pop_size'] = pop_size
        config['gen_count'] = case.getMaxEvalutions()/pop_size
        config['elites'] = max(2, int(pop_size*0.05))
        config['cxpb'] = 0.6
        config['mutpb'] = 0.1
        configs.append(config.copy())
        
        return configs
