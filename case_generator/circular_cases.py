
import numpy as np

from case import Case

class CircularCases(object):
    def __init__(self, grid_size, max_evaluations):
        self.grid_size = grid_size
        self.max_evaluations = max_evaluations
        
    def _generateCase(self, name, emitter_position, center, radius, num_samples):
        positions = []
        for x in xrange(num_samples):
            pos = np.array([np.cos(0.628 *x)*radius, np.sin(0.628*x)*radius])+np.array(center)
            positions.append(pos)
            
        return Case(name, self.max_evaluations, np.array(self.grid_size),emitter_position,positions)
        
    def generateCases(self):
        x_dim, y_dim = 2,2
        step = np.array([self.grid_size[0]/(x_dim+1), self.grid_size[1]/(y_dim+1)])
        
        
        cases = []
        for x in xrange(x_dim):
            for y in xrange(y_dim):
                center = np.array([step[0]*(x+1), step[1]*(y+1)])
                
                name = "%s %sx%s" % (self.__class__.__name__, x,y)
                case = self._generateCase(name, np.array([200.0,200.0]), center, 300.0, 10)
                
                
                cases.append(case)
                
                
        return cases
                
        
        
        
            
            
        
        
