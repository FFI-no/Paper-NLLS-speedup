
import  numpy as np

from sample import Sample
from environment import Environment
from nlls import NonLinearLeastSquares

import random

class Case(object):
    def __init__(self, name, max_evalutions, grid_size, emitter_position, positions):
        self.config = {}
        
        self.config["emitter_position"] = emitter_position.tolist()
        self.config["grid_size"] = grid_size.tolist()
        self.config["positions"] = map(lambda x: x.tolist(),positions)
        self.config["max_evalutions"] = max_evalutions
        self.config['name'] = name
        
        self.parseConfig()
        
    def parseConfig(self):
        env = Environment(self.config["emitter_position"],100,3.0)
        
        self.samples = []
        if self.config.get("measurements") is None:
            self.config["measurements"] = []
            for pos in self.config["positions"]:
                m = env.measuredPower(pos)
                s = Sample(pos, m)
                self.config["measurements"].append(float(m))
                self.samples.append(s)
        else:
            for pos, measurement in zip(self.config["positions"],self.config["measurements"]):
                s = Sample(pos, measurement)
                self.samples.append(s)
            
        self.nlls = NonLinearLeastSquares(self.config["grid_size"])
        self.nlls.setSamples(self.samples)
        
        self.name = None
        self.viz = None
        
    def setConfig(self, config):
        self.config = config
        self.parseConfig()
    
    def getConfig(self):
        return self.config
        
    def getSamples(self):
        return self.samples
        
    def getMaxEvalutions(self):
        return self.config["max_evalutions"]
        
    def fitness(self, position):
        x,y = position
        if x < 0.0 or y < 0.0 or x > self.config["grid_size"][0] or y > self.config["grid_size"][1]:
            return float("inf"),
        
        return self.nlls.qxy(np.array(position)),
        
        
    def setVisualization(self, viz):
        self.viz = viz
        
    def getVisualization(self):
        return self.viz
        
    def setSolution(self, solution):
        self.config["solution"] = ([map(float,solution[:]), float(solution.fitness.values[0])])
    
    def getSolution(self):
        return self.config["solution"]
    
    def __getstate__(self):
        return self.getConfig()
        
    def __setstate__(self,state):
        self.setConfig(state)
        
