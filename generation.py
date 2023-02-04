import numpy as np
import random
import pandas as pd

class Generation():

    def __init__(self,N,min1,max2) -> None:
        

        #Particulas
        self.n = N
        self.minx = min1
        self.maxx = max2

        #Se inicializan particulas y velocidad
        self.particles = np.zeros((N,3), np.float32)
        self.velocities = np.zeros((N,2), np.float32)

        #Mejor particula de la generacion
        self.best = np.zeros(3,np.float64)

        #Mejores posiciones de cada particula
        self.bestPositions = np.zeros((N,3), np.float32)

    def createParticles(self):
        for i in range(self.particles.shape[0]):
            for j in range(2):
                
                self.particles[i,j] = random.uniform(self.minx,self.maxx)
                self.velocities[i,j] = random.uniform(self.minx,self.maxx)


        self.calculateOP()

        for i in range(self.particles.shape[0]):
            self.bestPositions[i] = self.particles[i]

        #Escogemos al mejor
        values = self.particles[:,-1].tolist()
        min_value = min(values)
        index_min = values.index(min_value)
        aux_best1 = self.particles.item(index_min,0)
        aux_best2 = self.particles.item(index_min,1)
        aux_best3 = self.particles.item(index_min,2)
        #Copiar los valores
        
        self.best[0] = aux_best1
        self.best[1] = aux_best2
        self.best[2] = aux_best3
    
    def calculateOP(self):

        particles = self.particles[:,:2]

        values = []
        for i in range(particles.shape[0]):

                value = (particles[i,0])**2 + (particles[i,1])**2                   
                values.append(value)
                #Guardar el valor en
        
        self.particles[:,-1] = values

    def chooseBest(self,sel=1):
        prueba = self.best.copy()
        values = self.particles[:,-1].tolist()

        # # if sel==1: #Se busca el minimo
        min_value = min(values)
        index_min = values.index(min_value)
        aux_best = self.particles[index_min].copy()
        aux_Fit = aux_best[2]
        
        if aux_Fit < prueba[2]:
            self.best = aux_best


    def printGeneration(self):
        df = pd.DataFrame({ 'X': self.particles[:,0],
                 'Y': self.particles[:,1],
                 'Velocity X' : self.velocities[:,0],
                 'Velocity Y' : self.velocities[:,1],
                 'Fitness' : self.particles[:,-1]
        })
        return df

    def printBestPositions(self):
        df = pd.DataFrame({ 'X': self.bestPositions[:,0],
                 'Y': self.bestPositions[:,1],
                 'Fitness' : self.bestPositions[:,-1]
        })
        return df

    def updateVelocities(self,a,b1,b2):
        
        for i in range(self.n):

            r1 = random.uniform(0,1)
            r2 = random.uniform(0,1)
    
            vx = self.velocities[i,0]
            vy = self.velocities[i,1]

            px = self.particles[i,0]
            py = self.particles[i,1]

            aux1 = self.best[0]
            aux2 = self.best[1]

            new_vx = a*vx + b1*r1*(aux1-px) + b2*r2*(aux1 - px)
            new_vy = a*vy + b1*r1*(aux2-py) + b2*r2*(aux2 - py)

            self.velocities[i,0] = new_vx
            self.velocities[i,1] = new_vy
    
    def updatePositions(self):
      
        for i in range(self.n):

            px = self.particles[i,0]
            py = self.particles[i,1]

            vx = self.velocities[i,0]
            vy = self.velocities[i,1]

            new_px = px + vx
            new_py = py + vy

            #Checar que se mantengan en el rango

            if new_px <= 0:
                self.particles[i,0] = new_px if abs(new_px)<abs(self.minx) else self.minx 
            else:
                self.particles[i,0] = new_px if abs(new_px)<abs(self.maxx) else self.maxx
            
            if new_py <= 0:
                self.particles[i,1] = new_py if abs(new_py)<abs(self.minx) else self.minx 
            else:
                self.particles[i,1] = new_py if abs(new_py)<abs(self.maxx) else self.maxx 

       
    def chooseBestPositions(self):

        for i in range(self.n):

            op_a = self.particles[i,-1]
            op_n = self.bestPositions[i,-1]

            #Si el valor de aptitud es menor
            if op_a<op_n:
                self.bestPositions[i,0] = self.particles[i,0]
                self.bestPositions[i,1] = self.particles[i,1]
                self.bestPositions[i,2] = self.particles[i,2]

    ###Print Functions

    def printGeneration(self):
        print("-----PARTICLES-----")
        print(f"X\tY\tVX\tVY\tFitness")
        for i in range(self.n):
            print("{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}".format(self.particles[i,0],self.particles[i,1],self.velocities[i,0],self.velocities[i,1],self.particles[i,2]))

    def printBestPositions(self):
        print("-----BEST POSITIONS-----")
        print(f"X\tY\tFitness")
        for i in range(self.n):
           print("{:.4f}\t{:.4f}\t{:.4f}".format(self.bestPositions[i,0],self.bestPositions[i,1],self.bestPositions[i,2]))

    def printBest(self):
        print("-----BEST PARTICLE-----")
        print(f"X\tY\tFitness")
        print("{:.4f}\t{:.4f}\t{:.4f}".format(self.best[0],self.best[1],self.best[2]))