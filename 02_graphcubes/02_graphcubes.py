#graficos del transductor

import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
#from Ipython import display

#funciones

def animate_func(num):
    #limpar la figura
    #actualizar lines, punto, ejes, titulo
    ax.clear()

    #linea de trayectoria, actuliza por iteracion
    #se itera desde 0 hasta num+1, por indexacion en python
    ax.plot(x[:num+1],y[:num+1],z[:num+1], c="blue")
    #ubicacion del punto en el paso num
    ax.scatter(x[num],y[num],z[num], c="blue", marker="o")
    #origen, constante
    ax.plot3D(x[0],y[0],z[0], c="red", marker="o")

    #definir limites en ejes

    ax.set_xlim3d([x_min,x_max])
    ax.set_ylim3d([y_min,y_max])
    ax.set_zlim3d([z_min,z_max])

    #añadir etiquetas a lafigura
    ax.set_title("Trayectoria del transductor")
    ax.set_xlabel("Eje x")
    ax.set_ylabel("Eje y")
    ax.set_zlabel("Eje z")

    
  


#abrir csv
df = pd.read_csv('data.csv')
# npoin=400
# df=df[-npoin:]
x=np.array(df["x"].tolist())
y=np.array(df["y"].tolist())
z=np.array(df["z"].tolist())
numData=len(x)
# print(x)



x_min,x_max=x.min(),x.max()
y_min,y_max=y.min()-5,y.max()+5
z_min,z_max=z.min()-3,z.max()+3

#grafica estatica

fig=plt.figure(figsize=(7,7))
ax=plt.axes(projection="3d")
ax.plot3D(x,y,z,"gray")
ax.set_xlim3d([min(x),max(x)])
ax.set_ylim3d([min(y)-5,max(y)+5])
ax.set_zlim3d([min(z)-3,max(z)+3])
ax.set_xlabel("eje x")
ax.set_xlabel("eje y")
ax.set_xlabel("eje z")
fig.tight_layout()

plt.show()
# animacion

fig=plt.figure(figsize=(7,7))
ax=plt.axes(projection="3d")
anim=animation.FuncAnimation(fig,animate_func,interval=4,frames=len(x))
plt.tight_layout()

plt.show()
print("saving")
# Saving the Animation
f = r"animate_func.gif"
writergif = animation.PillowWriter(fps=len(x)/6)
anim.save(f, writer=writergif)
