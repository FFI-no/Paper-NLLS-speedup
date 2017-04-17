import numpy as np
import random

class NonLinearLeastSquares(object):
    samples = []
    grid_size = None

    alpha = 2.0

    def __init__(self, grid_size):
        self.grid_size = np.array(grid_size)
        
    def setSamples(self,samples):
        self.samples = samples

    def pkl(self,k,l):
        return self.samples[k].strength- self.samples[l].strength
        
    def qxy(self,position):
        error = 0.0
        for k in xrange(len(self.samples)):
            for l in xrange(k+1,len(self.samples)):
                p = self.pkl(k,l) - 5.0 * self.alpha * np.log10(np.linalg.norm(position-self.samples[l].position)**2/np.linalg.norm(position-self.samples[k].position)**2)
                error += p**2
        return error

#if __name__=="__main__":
    #from environment import Environment

    #random.seed(64)
    #env = Environment([200,200],100,2.0)

    #samples = []
    #for x in xrange(10):
        #pos = np.array([random.randint(0,1000),random.randint(0,1000)])
        #s = Sample(pos, env.measuredPower(pos))
        #samples.append(s)
        
    #grid_size = np.array([1000,1000])
    #nlls = NonLinearLeastSquares(grid_size)
    #nlls.setSamples(samples)

    #print nlls.minimizeQxy(10.0)
	
