


import argparse, os,re, yaml

class Population(object):
    def __init__(self, pop):
        self.pop = pop
        
    def getInd(self, index):
        return self.pop[index][0]
    
    def getFitness(self, index):
        return self.pop[index][1]
        
    def _getBestIndex(self):
        b = 0
        for i in xrange(len(self.pop)):
            if self.getFitness(i) < self.getFitness(b):
                b = i
        return b
        
    def __len__(self):
        return len(self.pop)
        
    def getBest(self):
        i = self._getBestIndex()
        return self.pop[i]
        
    def listInd(self):
        return map(lambda x: x[0], self.pop)
        
class Statistics(object):
    def getTree(self, max_depth = 0, depth=0):
        if max_depth == 0:
            return
        
        output = self.getName() + "\n"
        
        for child in self.children:
            for d in range(depth+1):
                output += "\t"
            output += child.getTree(max_depth - 1, depth + 1)
        
        return output
        
        
class TrialStatistics(object):
    def __init__(self, parent, path, trial):
        self.parent = parent
        self.trial = trial
        self.path = path
        
        #print self.logfile_path
        
        #if not os.path.exists(self.logfile_path) or not os.path.exists(self.genfile_path):
            #self.invalid = True
            #return 
        #else:
            #self.invalid = False
            
        self.log =  None
        self.generations = None
        self.config = None
        
    def _readLogfile(self):
        logfile_path = os.path.join(self.path, "log_file-%s.txt" % self.trial)
        with open(logfile_path,"r") as f:
            r = f.readlines()
        
            return r
        
    def _readGenfile(self):
        genfile_path = os.path.join(self.path, "generations-%s.txt" % self.trial)
        with open(genfile_path,"r") as f:
            generations = []
            for line in f.readlines():
                inf = float('Inf')
                parsed = eval(line)
                generations.append(Population(parsed))
            
            return generations
        
    def __repr__(self):
        #if self.invalid:
            #return "Invalid %s" % self.__class__.__name__
        #else:
        return "%s (%s)" %(self.__class__.__name__, self.trial)
    
    def getName(self):
        return self.__class__.__name__ + " (%s)"%self.trial
        
    def __getitem__(self, index):
        return self.getGeneration(index)
        
    def listGenerations(self):
        if self.generations is None:
            self.generations = self._readGenfile()
        return self.generations
        
        
    def getGeneration(self, index):
        if self.generations is None:
            genfile_path = os.path.join(self.path, "generations-%s.txt" % self.trial)
            with open(genfile_path,"r") as f:
                generations = []
                lines = f.readlines()
                
                inf = float('Inf')
                parsed = eval(lines[index])
                del lines
                return Population(parsed)
        else:        
            return self.generations[index]
        
    def getLog(self, index):
        if self.log is None:
            self.log = self._readLogfile()
        return self.log[index]

    def _readConfigfile(self):
        config_path = os.path.join(self.path, "config-%s.txt" % self.trial)
        if not os.path.exists(config_path):
            return {}
        
        with open(config_path,"r") as f:
            r = f.readlines()
            
            return yaml.load("".join(r))

    def hasConfig(self, **kwargs):
        if self.config is None:
            self.config = self._readConfigfile()
        
        for key,value in kwargs.items():
            if value is None and self.config.get(key) is None:
                return False
            if self.config.get(key) != value:
                return False
        return True
        
    def getConfig(self):
        if self.config is None:
            self.config = self._readConfigfile()
            
        return self.config
        
class AlgorithmStatistics(Statistics):
    def __init__(self, parent, path):
        self.path = path
    
        self.parent = parent
        self.children =  self.parse(path)
        
        self.cache_path = os.path.join(path, ".cache")
        
    def parse(self, path):
        children = []
        
        p = re.compile( "-([0-9]+)\.")
        
        trials = set()
        
        for subpath in os.listdir(self.path):   
            #if not os.path.isfile(os.path.join(path,subpath)):
                #print subpath
                #print "Fatal error"
                #exit(1)
                
            m = p.findall(subpath)
            
            if m:
                trials.add(int(m[0]))
                
        for trial in trials:
            child = TrialStatistics(self, path, trial)
            children.append(child)
            
        return children

    def getName(self):
        case = os.path.split(self.path)[1]
        return case
        #return self.__class__.__name__ + " (%s)" % case
        
    def listTrials(self):
        return self.children
        
    def getTrial(self, index):
        return self.children[index]
        
    def __getitem__(self, index):
        return self.getTrial(index)
        
    def filter(self,**kwargs):
        return filter(lambda x: x.hasConfig(**kwargs), self.children)
        
    def getBestSolutions(self):
        if os.path.exists(self.cache_path):
            try:
                import cPickle    
                with open(self.cache_path,"r") as f:
                    best_solutions = cPickle.load(f)
                    return best_solutions
            except:
                print "Parsing cache failed, deleting cache"
                os.remove(self.cache_path)
            
        best_solutions = {}
        
        for trial in self.listTrials():
            conf_set = set()
            for key, value in trial.getConfig().items():
                if type(value) is list:
                    value = tuple(value)
                    
                conf_set.add((key,value))
            conf = frozenset(conf_set)
            
            conf_hashable = frozenset(conf)
            
            if best_solutions.get(conf_hashable) is None:
                best_solutions[conf_hashable] = []
                
            best = trial.getGeneration(-1).getBest()
            
            best_solutions[conf_hashable].append(best)
        
        import cPickle    
        with open(self.cache_path,"w") as f:
            cPickle.dump(best_solutions,f)
        
        return best_solutions
        
    def isAlgorithm(self, name, exact=False):
        #print name, exact
        if exact:
            return name == self.getName()
        else:
            return name in self.getName()

class CaseStatistics(Statistics):
    def __init__(self, parent, path, case_id):
        self.path = path
        self.case_id = case_id
    
        self.parent = parent
        self.children =  self.parse(path)
        
        self.config_path = os.path.join(self.path, "config.txt")
        
        try:
            self.config = self._readConfigfile()
        except:
            self.config = None
            print self.getName(), "Warning: no config file found"
            
    def parse(self, path):
        children = []
        
        for subpath in os.listdir(self.path):   
            if subpath.endswith("config.txt"):
                continue
            #if not os.path.isfile(os.path.join(path,subpath)):
            child = AlgorithmStatistics(self,os.path.join(path,subpath))
            children.append(child)
                
        return children
    
    def getName(self):
        case = os.path.split(self.path)[1]
        return case
        #return self.__class__.__name__ + " (%s)" % case
    
    def __repr__(self):
        output = self.getName() + "\n"
        for child in self.children:
            output += "\t %s \n" % child.getName()
        
        return output
        
    def listAlgorithms(self):
        return self.children
        
    def getAlgorithm(self, index):
        return self.children[index]
        
    def __getitem__(self, index):
        return self.getAlgorithm(index)
        
    def getAlgorithmByName(self, name, **kwargs):
        algs = filter(lambda x: x.isAlgorithm(name, **kwargs), self.children)
        
        assert len(algs) <= 1, "There should never be more than 1 of each algorithm"
        
        return algs[0]
    
    def _readConfigfile(self):
        with open(self.config_path,"r") as f:
            r = f.readlines()
        
            return yaml.load("".join(r))
        
    def getConfig(self):
        return self.config
        
        
class Statistics(Statistics):
    def __init__(self, path):
        self.path = path
        
        self.children =  self.parse(path)
        
    def parse(self, path):   
        children = []
        
        p = re.compile( "[0-9]+")
        
        for subpath in os.listdir(self.path):   
            case_id = int(p.findall(subpath)[0])
            child = CaseStatistics(self, os.path.join(path,subpath),case_id)
            children.append(child)
        return children
        
    def getName(self):
        return self.__class__.__name__
        
        
    def __repr__(self):
        output = self.getName() + "\n"
        
        for child in self.children:
            output += "\t %s \n" % child.getName()
        
        return output 
        
    def getCase(self,index):
        return self.children[index]
        
    def listCases(self):
        return sorted(self.children, key=lambda x: x.case_id)
        
    def __getitem__(self, index):
        return sefl.getCase(index)
    
        
def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", nargs=1, help="Folder to be parsed for statistics")
    
    return parser

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    
    stat = Statistics(args.folder[0])
    
    print stat.getCase(0).getAlgorithm(0).getTrial(4).getGeneration(0)#.getGeneration(0).getBest()
    
