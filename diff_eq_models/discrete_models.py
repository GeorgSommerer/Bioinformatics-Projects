import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class PDE_2:
    def __init__(self,a,b,x0,y0):
        self.a = a
        self.b = b
        self.xy = np.array([x0,y0])
        self.result = np.array(self.xy)
    def observe(self):
        self.result = np.vstack((self.result,self.xy))
    def update(self):
        self.xy = np.matmul(self.a,self.xy) + self.b

class Logistic:
    def __init__(self,r,K,x0):
        self.r = r
        self.K = K
        self.x = x0
        self.result = np.array([self.x])
    def observe(self):
        self.result = np.vstack((self.result,np.array([self.x])))
    def update(self):
        self.x = self.x+self.r*self.x*(1-self.x/self.K)
"""
mylog = Logistic(0.05,500,10)
n = 400
for t in range(n-1):
    mylog.update()
    mylog.observe()
plt.plot(range(n),mylog.result)
plt.show()
"""


class LV_Euler:
    def __init__(self, a,b,c,d,h,x0,y0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.x = x0
        self.y = y0
        self.h = h
        self.result = np.array([self.x,self.y])
    def observe(self):
        self.result = np.vstack((self.result,np.array([self.x,self.y])))
    def update(self):
        x_temp = self.x + h*(self.a*self.x-self.b*self.x*self.y)
        y_temp = self.y + h*(-self.d*self.y + self.c*self.x*self.y)
        self.x = x_temp
        self.y = y_temp

"""
g=9.8
L=5
thetavalues, omegavalues = np.meshgrid(np.arange(-2.0,2.0,.5),np.arange(-2.0,2.0,.5))
thetadot = omegavalues 
omegadot = -g/L*np.sin(thetavalues)
plt.streamplot(thetavalues, omegavalues, thetadot, omegadot)
plt.show()
"""


class LV_PPM_3:
    def __init__(self,a,b,c,d,e,p,h,x0,y0,z0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.p = p
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.h = h
        self.result = np.array([self.x0,self.y0,self.z0])
    def observe(self):
        self.result = np.vstack((self.result,np.array([self.x0,elf.y0,self.z0])))
    def update(self):
        self.z0 = (self.z0)/(1+self.p*self.h*self.x0)
        self.x0 = self.x0*(1+self.a*self.h*self.z0)/(1+self.b*self.h*self.y0)
        self.y0 = self.y0*(1+self.c*self.h*self.x0)/(1+self.d*self.h)

class LV_PPM:
    def __init__(self,a,b,c,d,h,x0,y0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.x0 = x0
        self.y0 = y0
        self.h = h
        self.result = np.array([self.x0,self.y0])
    def observe(self):
        self.result = np.vstack((self.result,np.array([self.x0,self.y0])))
    def update(self):
        self.x0 = self.x0*(1+self.a*self.h)/(1+self.b*self.h*self.y0)
        self.y0 = self.y0*(1+self.c*self.h*self.x0)/(1+self.d*self.h)