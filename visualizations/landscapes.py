

import numpy as np
import pylab as p
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import random

class BasicFigure(object):
    def __init__(self):
        self.figure_id = random.randint(0,1000000000)
        self.figure = p.figure(self.figure_id)
    def _selectSelf(self):
        p.figure(self.figure_id)
        
    def _generateGrid(self, grid_size, grid_steps):
        self.grid_size = np.array(grid_size)
        self.grid_steps = np.array(grid_steps)
        
        x = np.linspace(0, grid_size[0], grid_steps[0])
        y = np.linspace(0, grid_size[1], grid_steps[1])
        self.xv, self.yv = p.meshgrid(x, y)

class RFLandscape(BasicFigure):
    def __init__(self, grid_size, grid_steps, rf_strengths):
        super(RFLandscape, self).__init__()
        
        self._generateGrid(grid_size, grid_steps)
        
        self.update(rf_strengths)
        
        p.ion()
        p.show()
        
    def update(self, rf_strengths):
        self._selectSelf()
        
        zv = rf_strengths
        
        ax = p3.Axes3D(self.figure)
        ax.contourf3D(self.xv,self.yv,zv, 20)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        self.figure.add_axes(ax)

class FitnessLandscape(BasicFigure):
    def __init__(self, grid_size, grid_steps, nlls_error_grid, solutions):
        super(FitnessLandscape, self).__init__()
        
        self._generateGrid(grid_size, grid_steps)
        
        self.scatter_handle = None
        
        
        self._initFigure()
        self.update(nlls_error_grid, solutions)
        
        p.ion()
        p.show()
        
    
    
    def _updateSolutions(self, solutions):
        
        xv,yv,zv = solutions
        
        if self.scatter_handle is not None:
            self.scatter_handle.remove()
        
        self._selectSelf()
        self.scatter_handle = self.ax.scatter([0],[0],[5000],s=500)#xv,yv,zv, c='r',s=30)
        
        self.ax.set_xlim([0,self.grid_size[0]])
        self.ax.set_ylim([0,self.grid_size[1]])
        p.draw()
        
    def _updateContours(self, fitness_function):
        zv = fitness_function(self.xv,self.yv)
        assert self.xv.shape == zv.shape, "Grid shape incorrect"
        
        self._selectSelf()
        self.ax.contourf3D(self.xv,self.yv,zv, 40)
        self.ax.set_xlim([0,self.grid_size[0]])
        self.ax.set_ylim([0,self.grid_size[1]])
        p.draw()
        
    
    def _initFigure(self):
        self.figure.clf()
        self.scatter_handle = None
        
        self.ax = p3.Axes3D(self.figure)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.figure.add_axes(self.ax)
        
        
    def update(self, fitness_function, solutions):
        
        if fitness_function is not None:
            self._initFigure()
            self._updateContours(fitness_function)
            
        if solutions is  not None:
            self._updateSolutions(solutions)
        
        
            
            
