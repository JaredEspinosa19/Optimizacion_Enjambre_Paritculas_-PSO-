#Minimización de la función x^2+y^2 en el intervalo de valores (-5,5) para x y y.
import generation as gn
from animation import animation

PARTICLES = 20
ITER = 50
MIN = -5
MAX = 5

V_A = 0.8
V_B1 = 0.7
V_B2 = 1

if __name__ == "__main__":


    animations = animation(PARTICLES,ITER,MIN,MAX)
    
    gen = 0
    
    generation = gn.Generation(PARTICLES,MIN,MAX)
    
    #Primera generacion
    generation.createParticles()
    #generation.chooseBest(sel=1)

    generation.printGeneration()
    generation.printBestPositions()
    generation.printBest()


    animations.addGeneration(gen,generation.particles[:,:2],generation.bestPositions[:,:2],generation.best[:2])

    gen+=1

    while gen<ITER:
        generation.updateVelocities(V_A,V_B1,V_B2) 
        generation.updatePositions()

        #Se calculan las aptitudes
        generation.calculateOP()

        #actualizar mejores posioiones
        generation.chooseBestPositions()

        generation.chooseBest(sel=1)

        #Agregar la generacion a la animacion
        animations.addGeneration(gen,generation.particles[:,:2],generation.bestPositions[:,:2],generation.best[:2])

        print(f"{gen} ITERATION")
        generation.printGeneration()
        generation.printBestPositions()
        generation.printBest()
        gen+=1
        # print(gen)

    animations()