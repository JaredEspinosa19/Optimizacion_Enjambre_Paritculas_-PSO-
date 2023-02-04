import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class animation():

    def __init__(self, particles, generations, min, max):
        #donde se guardan las particulas
        self.values = np.zeros((particles,2,generations),np.float64)
        self.best = np.zeros((2,generations),np.float64)
        #Mejores posiciones
        self.pvalues = np.zeros((particles,2,generations),np.float64)
        #RANGOS DE VALORES
        self.min = min
        self.max = max
        #Numero de iteraciones
        self.iter = generations

    def addGeneration(self,n,values, pvalues, best):
        #filas, columnas, profundidad
        self.values[:,0,n] = values[:,0]
        self.values[:,1,n] = values[:,1]

        self.pvalues[:,0,n] = pvalues[:,0]
        self.pvalues[:,1,n] = pvalues[:,1]

        self.best[0,n] = best[0]
        self.best[1,n] = best[1]


    def __call__(self):

        fig = plt.figure(figsize=(10,10))

        xx = np.linspace(-5, 5)
        yy = xx.copy()
        X, Y = np.meshgrid(xx, yy)
        Z = X**2 + Y**2

        fig, ax = plt.subplots(figsize=(10,10))
        fig.set_tight_layout(True)
        img = ax.imshow(Z, extent=[-5, 5, -5, 5], origin='lower', cmap='viridis', alpha=0.5)
        fig.colorbar(img, ax=ax)
        ax.plot([0], [0], marker='x', markersize=5, color="white")
        contours = ax.contour(X, Y, Z, 10, colors='black', alpha=0.4)
        ax.clabel(contours, inline=True, fontsize=8, fmt="%.0f")
        pbest_plot = ax.scatter(self.pvalues[:,0,0], self.pvalues[:,1,0], marker='^', color='black', alpha=0.3)
        p_plot = ax.scatter(self.values[:,0,0], self.values[:,1,0], marker='^', color='blue', alpha=0.5)
        #p_arrow = ax.quiver(X[0], X[1], V[0], V[1], color='blue', width=0.005, angles='xy', scale_units='xy', scale=1)
        gbest_plot = plt.scatter(self.best[0,0], self.best[1,0], marker='^', s=100, color='red', alpha=0.5)
        ax.set_xlim([-5,5])
        ax.set_ylim([-5,5])

        def animate(i):
            "Steps of PSO: algorithm update and show in plot"
            title = 'Iteration {:02d}'.format(i)
            #Set picture
            ax.set_title(title)
            pbest_plot.set_offsets(self.pvalues[:,:,i])
            p_plot.set_offsets(self.values[:,:,i])
            #p_arrow.set_offsets(X.T)
            #p_arrow.set_UVC(V[0], V[1])
            gbest_plot.set_offsets(self.best[:,i])
            return ax, p_plot, pbest_plot, gbest_plot

        anim = FuncAnimation(fig, animate, frames=list(range(0,self.iter)), interval=500, blit=False, repeat=False)
        anim.save("PSO.gif", dpi=120, writer="pillow")