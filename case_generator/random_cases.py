
import numpy as np
import random

from case import Case

class RandomCases(object):
    def __init__(self, grid_size, num_cases, max_evaluations):
        self.grid_size = np.array(grid_size)
        self.num_cases = num_cases
        self.max_evaluations = max_evaluations
    def generateCases(self):
        np.random.seed(random.randint(0,1000000))
        
        cases = []
        for i in xrange(self.num_cases):
            num_samples = 10
            positions = []
            for x in xrange(num_samples):
                pos = np.multiply(np.random.rand(1,2), self.grid_size)
                positions.append(pos)
                
            name = "%s %s" % (self.__class__.__name__, i)
            case = Case(name, self.max_evaluations, self.grid_size,self.grid_size/2.0,positions)
            
            cases.append(case)
                
        return cases
                
        
        
        
            
            
        
        
