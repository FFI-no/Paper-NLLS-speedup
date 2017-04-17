import numpy as np

from deap_algorithm import DeapAlgorithm

from deap import base
from deap import creator
from deap import tools


class BruteForce(DeapAlgorithm):
    def __init__(self):
        super(BruteForce, self).__init__()
        self.state = None
        
        self.bootstrap_deap()
        
    def _generate_individual(self):
        i= creator.Individual(self.grid[self.state])
        self.state += 1
        return i
        
    def bootstrap_deap(self):
        creator.create("FitnessMinError", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMinError)

        self.toolbox = base.Toolbox()
        self.toolbox.register("population", tools.initRepeat, list, self._generate_individual)
        self.toolbox.register("select", tools.selBest)
    
    def run(self, case, logger):
        x = np.linspace(0, case.config['grid_size'][0], self.config["grid_steps"][0])
        y = np.linspace(0, case.config['grid_size'][1], self.config["grid_steps"][1])
        self.grid = zip(*(x.flat for x in np.meshgrid(x, y)))
        self.state = 0
        
        self.toolbox.register("evaluate", case.fitness)
        
        #Create a population of random individuals
        pop = self.toolbox.population(n=len(self.grid))
        
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
        
        
        config['grid_steps'] = [40, 40]
        configs.append(config.copy())
        
        config['grid_steps'] = [34, 34]
        configs.append(config.copy())
        
        config['grid_steps'] = [28, 28]
        configs.append(config.copy())
        
        config['grid_steps'] = [24, 24]
        configs.append(config.copy())
        
        config['grid_steps'] = [20, 20]
        configs.append(config.copy())
        
        config['grid_steps'] = [18, 18]
        configs.append(config.copy())
        
        config['grid_steps'] = [16, 16]
        configs.append(config.copy())
        
        config['grid_steps'] = [14, 14]
        configs.append(config.copy())
        
        config['grid_steps'] = [10, 10]
        configs.append(config.copy())
        
        return configs
        
    def get_solver_configs(self):
        configs = []
        
        config = {}
        config['grid_steps'] = [200, 200]
        configs.append(config.copy())
        
        config['grid_steps'] = [20, 20]
        configs.append(config.copy())
        
        return configs
        
        
        
        
    
