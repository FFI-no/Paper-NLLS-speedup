from celery import Celery
from time import sleep

import traceback,sys
import random

from algorithms.brute import BruteForce
from algorithms.ga import GA
from algorithms.cma_es import CMAES
from algorithms.random_sampler import RandomSampler
from algorithms.pso import PSO
from algorithms.de import DiffEvo
from algorithms.nm import NM
from algorithms.random_nm import RandomNM

from case_generator.case import Case

from logger import Logger

app = Celery("tasks")
#app.config_from_object('assist_workstation')
app.config_from_object('celeryconfig')

#A task is a Case, a Solver and a Config
    
@app.task
def test_algorithm(logging_folder, i_offset, num_trials, case_dict, solver_name, config):
    
    case = Case.__new__(Case)
    case.setConfig(case_dict)
    
    solver_instance = eval(solver_name)()
    solver_instance.set_config(config)

    results = []
    
    for trial in range(num_trials):    
        logger = Logger(case, solver_instance, trial+i_offset, logging_folder)
        logger.saveConfig(config)
        logger.setSilent(True)
        
        random.seed(trial)
        r = solver_instance.run(case, logger)
        results.append(r)
        
    return 
    
    
@app.task
def solve_case(logging_folder, case_dict, config):
    case = Case.__new__(Case)
    case.setConfig(case_dict)
    
    solver_instance = BruteForce()
    solver_instance.set_config(config)

    logger = Logger(case, solver_instance, 0, logging_folder)
    logger.saveConfig(config)
    logger.setSilent(True)
    
    res = solver_instance.run(case, logger)
    
    case.setSolution(res[1])
    logger.saveCaseConfig(case.getConfig())
    
    return 
