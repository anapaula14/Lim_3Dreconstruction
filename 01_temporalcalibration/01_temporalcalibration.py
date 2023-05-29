#procesamiento

import  numpy as  np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.image as mpimg 
import cv2
import os

###################
#PROCESADOR DE STRINGS
def replaceComas(string):#csv
    a=""
    v=False
    final=""
    for i,d in enumerate(string): #recorre dos variables 0 "a"... 1 "b"
        if d==" " or i==len(string)-1:
            if v==True:
                final+=a+","
                a=""
                v=False
            v=False
        else:
            a+=d
            v=True
    return final

def extractor(line):
    g=replaceComas(line[25:].strip("\n")) #hasta que termine la linea
    g=g[:-1].split(",")#separar cada item de "csv" en lista
    return g

"""
def transfCubes(txtOrg,lenB):
    with open(txtOrg,"r") as data:
        line=data.readlines()
        l1=line[0]
        rest=line[1:]
        
    l1=l1.strip("Format for each sensor is: status ")
    l1=l1.strip("\n")
    l1=l1.replace(" ", "")
    lista=l1.split(",")
    mat=[]
    for i,d in enumerate(rest):
        try: #intenta hacer y si hay error printea 
            mat.append(extractor(d))
        except:
            print(i,end=",")
    mat=np.array(mat,float)
    decim=len(mat)/lenB
    print("longitud del trakSTAR %.3d; longituf de las camaras %.3d"%(len(mat),lenB))
    print("%.3f , aproximado : %d "%(decim,round(decim)))

    mat=signal.decimate(mat,round(decim),axis=0)
    df=pd.DataFrame(mat,columns=lista)
    return df
"""

def transfCubesNoInterpol(txtOrg,lenB):
    with open(txtOrg,"r") as data:
        line=data.readlines()
        l1=line[0]
        rest=line[1:]

    l1=l1.strip("Format for each sensor is: status ")
    l1=l1.strip("\n")
    l1=l1.replace(" ", "")
    lista=l1.split(",")
    mat=[]
    for i,d in enumerate(rest):
        try:
            mat.append(extractor(d))
        except:
            print(i,end=",")
    mat=np.array(mat,float)
    decim=len(mat)/lenB
    print("longitud del trakSTAR %.3d; longituf de las camaras %.3d"%(len(mat),lenB))
    print("%.3f , aproximado : %d "%(decim,round(decim)))
    df=pd.DataFrame(mat,columns=lista)
    return df

def algorith(a,b):
    bn=b.Tiempo.copy()
    an=a.copy()
    data=[]
    ai=0
    bi=0
    errorp=100000

    while ai<=a.index[-1]:
        error=abs(bn[bi]-an.time[ai])
        if(errorp<error):
            data.append(ai-1)
            error=10000
            bi+=1
        if(a.index[-1]-ai==1):
            data.append(ai)
        errorp=error
        ai+=1
    print(len(data))
    return data    

    
###mainnn
#carpeta=input("Escriba el nombre de la carpeta interna:")
    
carpeta="video_bola" 

csv=pd.read_csv(os.path.join(carpeta,"DatosTrakSTART.csv"), index_col=0)

redireccion=os.chdir(carpeta)
cubes=transfCubesNoInterpol(carpeta, len(csv))

cubes["time"]=cubes["time"]-cubes["time"][0]
x=len(cubes)-len(csv)
print("se dropearan",x,"datos")

diff_time=cubes.time[cubes.index[-1]]-csv.Tiempo[csv.index[-1]]
cubes.drop(cubes[cubes["time"]<=diff_time].index,inplace=True)
cubes=cubes.reset_index(drop=True)
cubes["time"]=cubes["time"]-cubes["time"][0]
indices=algorith(cubes,csv)
cubes=(cubes.iloc[indices].copy())
cubes=cubes.reset_index(drop=True)

df=csv.join(cubes)
df.to_csv("data.csv")
df.head()

data_nueva=pd.read_csv("data.csv")
data_nueva=data_nueva.iloc[50:]
data_nueva=data_nueva.iloc[:-50]

data_nueva.to_csv('nuevo_data.csv', index=False)

df.head()




























        




