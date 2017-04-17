from tasks import test_algorithm, solve_case

import random
import numpy as np
import sys
import yaml
import argparse
import matplotlib as plt
from time import sleep

from deap import tools

from algorithms.brute import BruteForce
from algorithms.ga import GA
from algorithms.cma_es import CMAES
from algorithms.random_sampler import RandomSampler
from algorithms.pso import PSO
from algorithms.de import DiffEvo
from algorithms.nm import NM
from algorithms.random_nm import RandomNM

from case_generator.environment import Environment
from case_generator.circular_cases import CircularCases
from case_generator.random_cases import RandomCases

from visualizations.case_visualizer import visualizeCase

from logger import Logger

def main(grid_size, num_trials, num_cases, max_evaluations, silent=True, visualize=True, find_opt=True, parallel=False):
    logging_folder = "Results %s" % max_evaluations
    
    solution_generator = BruteForce()
    slow_config, fast_config = solution_generator.get_solver_configs()
    
    solution_config = fast_config
    solution_generator.set_config(solution_config)
    
    #Test brute force solvers
    #solvers = [BruteForce()]
    
    #Test heuristics
    solvers = [RandomNM()]#RandomNM()]#, NM()], GA(), RandomSampler(), PSO(), DiffEvo(), CMAES()]
    
    cases = []
    
    print "Generating test cases"
    
    random.seed(0)
    
    c = CircularCases(grid_size, max_evaluations)
    t = c.generateCases()
    #cases.extend(t)   
     
    c = RandomCases(grid_size, num_cases, max_evaluations)
    t = c.generateCases()
    cases.extend(t)  
   
    print "Test cases generated"  
    print
    
    print "Solving test cases by brute force"
    
    results_inprogress = []
    
    for i, case in enumerate(cases):
        if parallel:
            if find_opt:
                r = solve_case.delay(logging_folder, case.getConfig(), solution_config)
                results_inprogress.append(r)
        else:
            logger = Logger(case, solution_generator, 0, logging_folder)
            logger.setSilent(silent)
            
            if visualize:
                case.setVisualization(visualizeCase(case))
                
            if find_opt:
                case.setSolution(solution_generator.run(case, logger)[1])
                print case.getSolution()
            
            logger.saveCaseConfig(case.getConfig())
            
            print "\t {:.2%} percent complete".format(float(i+1)/len(cases))
            
    print
    
    
    
    
    print "Testing solvers"
    i = 0
    for solver_instance in solvers:
        random.seed(0)
        
        print "\t Running solver %s" % solver_instance.__class__.__name__
        for case in cases:
            
            configs = solver_instance.get_configs(case)
            for config_i, config in enumerate(configs):
                if parallel:
                    r = test_algorithm.delay(logging_folder, config_i*num_trials, num_trials, case.getConfig(),  solver_instance.__class__.__name__, config)
                    results_inprogress.append(r)
                else:
                    for trial in range(num_trials):        
                        logger = Logger(case, solver_instance, trial+config_i*num_trials, logging_folder)
                        logger.saveConfig(config)
                        logger.setSilent(silent)
                        
                        solver_instance.set_config(config)
                        pop, best, fit = solver_instance.run(case, logger)
                        #print "Best:", best
                        #d = np.linalg.norm(np.array(best)-np.array([500,500]))
                        #print "Distance", d
                    
                        #percent_complete = float(i+1)/(len(solvers)*len(cases)*num_trials)
                        #print "\t\t {:.2%} percent complete".format(percent_complete)
                        i += 1
                        
        
    if parallel:
        finished = 0
        while len(results_inprogress) > 0:
            try:
                statuses = map(lambda x: x.status, results_inprogress)
                started = len(filter(lambda x: x == "STARTED", statuses))
                pending = len(filter(lambda x: x == "PENDING", statuses))
                finished = len(filter(lambda x: x == "SUCCESS", statuses))
                failed =  len(filter(lambda x: x == "FAILURE", statuses))
                print "Started: %s" % started
                print "Pending: %s" % pending
                print "Finished: %s" % finished
                print "Failed: %s" % failed
                print
                
                f = filter(lambda x: x == "SUCCESS", results_inprogress)
                nf = filter(lambda x: x != "SUCCESS", results_inprogress)
                results_inprogress = nf
                
                while len(f) > 0:
                    t = f.pop()
                    del t
                
                sleep(1)
                
                assert failed==0, "Some tasks failed, aborting"
                
                if pending == 0 and started == 0: 
                    print "All tasks completed"
                    break
                    
            except (AssertionError, KeyboardInterrupt, SystemExit), e:
                print e
                for task in results_inprogress:
                    task.revoke()
                print "Exiting."
                break
                
def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid_size", nargs=2, type=float, default=[1000.0,1000.0])
    parser.add_argument("--num_trials", nargs=1, type=int, default=[50])
    parser.add_argument("--num_cases", nargs=1, type=int, default=[50])
    parser.add_argument("--max_evaluations", nargs=1, type=int, default=[400])
    parser.add_argument('--no_find_opt', dest='find_opt', action='store_false')
    parser.set_defaults(find_opt=True)
    parser.add_argument('--no_parallel', dest='no_parallel', action='store_true')
    parser.set_defaults(no_parallel=False)
    parser.add_argument('--no_gui', dest='no_gui', action='store_true')
    parser.set_defaults(no_gui=False)
    return parser

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    
    
    main(args.grid_size,args.num_trials[0],args.num_cases[0],args.max_evaluations[0],visualize=not args.no_gui, find_opt=args.find_opt, parallel=not args.no_parallel)
    
    
