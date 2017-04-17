

import os
import numpy as np
import yaml

from deap import tools

class Logger(object):
    def __init__(self, case, solver, trial, parent_folder="results"):
        self.log_folder = os.path.join(parent_folder,case.config['name'], solver.__class__.__name__)
        
        self.file_prefix = ""
        self.file_postfix = "-%s" % trial
        
        self.case = case
        self.trial = trial
        
        
        if not os.path.exists(self.log_folder):
            try:
                os.makedirs(self.log_folder)
            except:
                print "Someone beat us to it, damn"
        
        self.case_config_path = os.path.join(parent_folder, case.config['name'], "config.txt")
        
        
        filename = os.path.join(self.log_folder, self.file_prefix + "generations" + self.file_postfix + ".txt")
        self.generation_file = open(filename, "w")
        
        filename = os.path.join(self.log_folder, self.file_prefix + "log_file" + self.file_postfix + ".txt")
        self.output_file = open(filename, "w")
        
        
        self._initStatsLogbook()
        
        self.silent = False
        
    def __del__(self):
        self.generation_file.close()
        self.output_file.close()
    
    def setSilent(self, silent):
        self.silent = silent
        
    def _initStatsLogbook(self):
        self.stats = tools.Statistics(lambda ind: ind.fitness.values)
        self.stats.register("avg", np.mean)
        self.stats.register("std", np.std)
        self.stats.register("min", np.min)
        self.stats.register("max", np.max)

        self.logbook = tools.Logbook()
        self.logbook.header = ["gen", "pop", "evals"] + self.stats.fields
    
    def redrawPop(self, pop):
        viz = self.case.getVisualization()
        if viz is not None:
        
            xs = []
            ys = []
            zs = []
            
            for ind in pop:
                x,y = ind[:]
                
                z = self.case.fitness(np.array([x,y]))[0]+500.0
                
                xs.append(x)
                ys.append(y)
                zs.append(z)
            
            viz._updateSolutions((xs,ys,zs))
            
    def _dumpPopulation(self, pop):
        output = []
        for ind in pop:
            output.append((list(ind[:]), ind.fitness.values[0]))
        
        self.generation_file.write(str(output) +"\n")
        self.generation_file.flush()
            
    def updateLog(self, pop, gen, evals):
        print "Updating log"
        record = self.stats.compile(pop)
        self.logbook.record(gen=gen, pop=len(pop), evals=evals, **record)
        
        self.redrawPop(pop)
        self._dumpPopulation(pop)
        if not self.silent:
            print(self.logbook.stream)
            
        self.output_file.write(self.logbook.stream + "\n")
        self.output_file.flush()
        
        from time import sleep
        sleep(0.5)
        
    def saveConfig(self, config):
        filename = os.path.join(self.log_folder, self.file_prefix + "config" + self.file_postfix + ".txt")
        config_file = open(filename, "w")
        
        dump =  yaml.dump(config, default_flow_style=False)
        config_file.write(dump)
        
        config_file.close()
        
        
    def saveCaseConfig(self, config):        
        config_file = open(self.case_config_path, "w")
        dump =  yaml.dump(config, default_flow_style=False)
        config_file.write(dump)
        config_file.close()
    
