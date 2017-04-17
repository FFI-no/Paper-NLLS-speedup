import numpy as np

import random

class Environment:
    def __init__(self,emitter_position, emitter_strength, noise_stddev):
        self.setEmitterPos(emitter_position)
        self.setEmitterStrength(emitter_strength)
        self.setNoiseStddev(noise_stddev)
        self.loss_factor_a = 2.0
        
    def setEmitterPos(self,emitter_position):
        self.emitter_position = np.array(emitter_position)
        
    def setEmitterStrength(self, emitterStrength):
        self.emitter_strength = float(emitterStrength)
        
    def setNoiseStddev(self,noise_stddev):
        self.noise_stddev = float(noise_stddev)
        
    def noise(self):
        return random.gauss(0,self.noise_stddev)
        
    def emitterStrengthDbm(self):
        return 10.0*np.log10(self.emitter_strength)
        
    def actualPower(self,pos):
        n_pos = np.array(pos)
        d = np.sqrt(np.linalg.norm(n_pos-self.emitter_position))
        if d == 0: 
            return self.emitterStrengthDbm()
        else:
            return self.emitterStrengthDbm() - 10.0 * self.loss_factor_a * np.log10(d)
            
    def measuredPower(self,pos):
        a = self.actualPower(pos)
        n = self.noise()
        return a + n

if __name__=="__main__":
    env = Environment([0.0,0.0],100.0, 5.0)
    
    for d in xrange(0,1001,100):
        pos = [d, 0.0]
        print "Distance {:.2f}, signal strength {:.2f}, measured signal strength {:.2f}".format(d, env.actualPower(pos), env.measuredPower(pos))
        
        
    
