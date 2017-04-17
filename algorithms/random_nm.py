from deap_algorithm import DeapAlgorithm

import numpy as np
import random


from deap import base
from deap import creator
from deap import tools

####Parameter
#Num_evaluations



class RandomNM(DeapAlgorithm):
    def __init__(self):
        super(RandomNM, self).__init__()
        
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
        alpha = self.config['alpha']
        gamma = self.config['gamma']
        phi = self.config['phi']
        sigma = self.config['sigma']
        
        nm_evaluations = self.config['nm_evaluations']
        
        self.config['grid_size'] = case.config['grid_size']
        self.toolbox.register("evaluate", case.fitness)
        
        #Create a population of random individuals
        pop = self.toolbox.population(n=case.getMaxEvalutions()-nm_evaluations)
        
        # Evaluate the individuals
        fitnesses = self.toolbox.map(self.toolbox.evaluate, pop)
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        
        if logger is not None:
            logger.updateLog( pop, 0, len(pop))
            
        evaluations = len(pop)
        g = 1
        pop = tools.selBest(pop, 3)
        
        while evaluations < case.getMaxEvalutions():
            l_sorted = sorted(pop, key=lambda i: i.fitness.values[0])
            
            best = l_sorted[0]
            worst = l_sorted[-1]
            
            centroid = reduce(lambda x, y: x+y, map(lambda i: np.array(i), l_sorted[:-1]), np.zeros(2))/float(len(pop)-1)
            
            reflected_point = centroid + alpha * (centroid - np.array(worst))
            reflected_fitness = self.toolbox.evaluate(reflected_point)
            evaluations += 1
            
            if reflected_fitness < best.fitness.values[0]:
                expansion_point = centroid + gamma * (centroid - np.array(worst))
                expansion_fitness = self.toolbox.evaluate(expansion_point)
                
                pop = list(l_sorted[:-1])
                if expansion_fitness[0] < reflected_fitness[0]:
                    ind = creator.Individual(expansion_point)
                    ind.fitness.values = self.toolbox.evaluate(ind)
                    evaluations += 1
                    pop.append(ind)
                else:
                    ind = creator.Individual(reflected_point)
                    ind.fitness.values = self.toolbox.evaluate(ind)
                    evaluations += 1
                    pop.append(ind)
                
            else:
                contraction_point = centroid + phi * (centroid - np.array(worst))
                contraction_fitness = case.fitness(contraction_point)
            
                if contraction_fitness[0] < worst.fitness.values[0]:
                    pop = list(l_sorted[:-1])
                    
                    ind = creator.Individual(contraction_point)
                    ind.fitness.values = self.toolbox.evaluate(ind)
                    evaluations += 1
                    pop.append(ind)
                else:
                    new_pop = list()
                    
                    for i in range(1, len(pop)):
                        xi = np.array(best) + sigma * (np.array(l_sorted[i] - np.array(best)))

                        ind = creator.Individual(xi)
                        ind.fitness.values = self.toolbox.evaluate(ind)
                        evaluations += 1
                        new_pop.append(ind)
                        
                    new_pop.append(best)
                    pop = new_pop
            
            g += 1
            if logger is not None:
                logger.updateLog(pop, g, len(pop))
                
        best = tools.selBest(pop, 1)[0]
    
        return pop,  best, best.fitness.values[0]
        

    def get_configs(self, case):
        configs = []
        
        
        alphas = [0.8, 1.0, 1.2]
        gammas = [1.8, 2.0, 2.2]
        phis = [-0.4, -0.5, -0.6]
        sigmas = [0.4, 0.5, 0.6]
        nm_evals = [0.10, 0.20]
        
        config = {}
        for alpha in alphas:
            for gamma in gammas:
                for phi in phis:
                    for sigma in sigmas:
                        for nm_eval in nm_evals:
                            config['alpha'] = alpha
                            config['gamma'] = gamma
                            config['phi'] = phi
                            config['sigma'] = sigma
                            config['nm_evaluations'] = int(case.getMaxEvalutions()*nm_eval)
        
                            configs.append(config.copy())
        
        
        #config = {}
        #config['alpha'] = 1.0
        #config['gamma'] = 2.0
        #config['phi'] = -0.5
        #config['sigma'] = 0.5
        
        #config['nm_evaluations'] = int(case.getMaxEvalutions()*0.1)
        
        #configs.append(config.copy())
        
        return configs

