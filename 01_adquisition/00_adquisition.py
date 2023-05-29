import cv2
from os import *
import pandas as pd
import time
import mouse
import pyautogui

def CrearVideo(nombre,ruta):
    mkdir(nombre)
    chdir(path.join(ruta,nombre))
    ecografo=nombre+"_eco"
    camara=nombre+"_video" 
#d:\Users\u_imagenes\Desktop\reconstruccion
#"C:\Program Files (x86)\Ascension\3D Guidance (Rev D)\Cubes\"
    startfile(r'd:\Users\u_imagenes\Desktop\reconstruccion\cubes.lnk')
    mouse.move(490, 725, absolute=True, duration=10)
    mouse.click('left')
    mouse.move(70, 820, absolute=True, duration=1)
    mouse.click('left')

    time.sleep(3)
    pyautogui.write(nombre)

    time.sleep(2)
    mouse.move(830, 520, absolute=True, duration=1)
    mouse.click('left')

    time.sleep(1)
    mouse.move(830, 460, absolute=True, duration=1)
    mouse.click('left')


    time.sleep(3)
    pyautogui.write(nombre+'.txt')

    time.sleep(2)
    mouse.move(830, 520, absolute=True, duration=1)
    mouse.click('left')

    
    #time.sleep(1)
    mouse.move(50, 50, absolute=True, duration=1)

    
    captura1 = cv2.VideoCapture(0)
    mouse.click('left')
    captura2 = cv2.VideoCapture(1)
    

    salida1 = cv2.VideoWriter(ecografo+".avi",cv2.VideoWriter_fourcc(*'XVID'),20.0,(640,480))
    salida2 = cv2.VideoWriter(camara+".avi",cv2.VideoWriter_fourcc(*'XVID'),20.0,(640,480))
    contador=0


    list_time=list()
    tiempoin=time.time()
    
    while (captura1.isOpened() and captura2.isOpened()):
          
      ret1, imagen1 = captura1.read()
      ret2, imagen2 = captura2.read()
      
      if ret1 == True and ret2==True:
        cv2.imshow('video1', imagen1)
        cv2.imshow('video2', imagen2)
        
        salida1.write(imagen1)
        salida2.write(imagen2)
        list_time.append(time.time()-tiempoin)
        if cv2.waitKey(1) & 0xFF == ord('s'):
          break
          mouse.move(70, 820, absolute=True, duration=1)
          mouse.click('left')
            
      else:
        break
        #time.sleep(sampling_time)
    
    mouse.move(50, 50, absolute=True)
    mouse.click('left')
        
    captura1.release()
    salida1.release()
    salida2.release()
    cv2.destroyAllWindows()
    return list_time

def CrearCSV(nombre,ruta,l):
    ecografo=nombre+"_eco"
    camara=nombre+"_video"
    
    videoB=ecografo+".avi"
    videoA=camara+".avi"
    
    rootA = path.join(ruta,nombre, videoA)
    rootB = path.join(ruta,nombre, videoB)
    
    cam1=cv2.VideoCapture(rootA)
    cam2=cv2.VideoCapture(rootB)
    
    currentframe=0
    lista_frames=[]

    indtime=0

    while True:
      ret1,frame1=cam1.read()
      ret2,frame2=cam2.read()

        
      if ret1 and ret2: #mientras haya frames que extraer

##        tiempoActual=time.time()
##        tiempo_xFrame=tiempoActual-start
        #start=tiempoActual
        
        name1="frameA"+str(currentframe)+".jpg"
        name2="frameB"+str(currentframe)+".jpg"
        
        ubicacionActual1=path.join(nombre, name1)
        ubicacionActual2=path.join(nombre, name2)
        lista_frames.append([ubicacionActual1, ubicacionActual2,l[indtime]])
        indtime+=1

        #escribir frame extraido
        cv2.imwrite(name1,frame1)
        cv2.imwrite(name2,frame2)
        
        currentframe+=1
        
      else:
        break

    cam1.release()
    cam2.release()
    cv2.destroyAllWindows()

    tabla=pd.DataFrame(data=lista_frames,columns=["DireccionA", "DireccionB","Tiempo"])
    tabla.to_csv("DatosTrakSTART.csv")


##

nombre=input("Ingrese el nombre del video: ")

absFilePath = path.abspath(__file__)
ruta, filename = path.split(absFilePath)

print(path, "y", filename)

nombre_carpeta="video_"+nombre
l=CrearVideo(nombre_carpeta, ruta)
CrearCSV(nombre_carpeta,ruta,l)

