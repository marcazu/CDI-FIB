# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 08:14:40 2020

@author: fernando
"""

########################################################
import scipy
import numpy as np
import time
import matplotlib.pyplot as plt
import imageio
import PIL
import pickle



#%%


imagen=imageio.imread('../standard_test_images/jetplane.png')
# imagen=imageio.imread('../standard_test_images/mandril_gray.png')
# imagen=imageio.imread('../standard_test_images/crosses.png')
# imagen=imageio.imread('../standard_test_images/circles.png')
# imagen=imageio.imread('../standard_test_images/cameraman.png')
# imagen=imageio.imread('../standard_test_images/walkbridge.png')


(n,m)=imagen.shape # filas y columnas de la imagen

plt.figure()
plt.xticks([])
plt.yticks([])
plt.imshow(imagen, cmap=plt.cm.gray,vmin=0, vmax=255)
plt.show()

       

#%%
"""
Definir una funcion que dada una imagen
cuantize uniformemente los valores en cada bloque 
"""

def pasarABloques(image, rows, cols):
    blockImage = np.zeros((int(rows * cols / 64), 8, 8))
    block = 0
    for i in range(int(cols / 8)):
        for j in range(int(rows / 8)):
            blockImage[block] = np.reshape(image[j*8:j*8+8, i*8:i*8+8], [8,8])
            block += 1
    return blockImage


def quantitzarBloc(imagenCodigo, bloc, nivells):
    maxim = np.max(bloc)
    minim = np.min(bloc)
    quantitzacio = [maxim,minim]
    gap = (maxim - minim)/nivells
    i = 0
    while i < len(bloc):
        j = 0
        while j < len(bloc[i]):
            k = 0
            while k < nivells:
                aux = minim + gap*(k+1)
                if(bloc[i][j] <= aux):
                    bloc[i][j] = k
                    break
                k += 1
            j += 1
        i += 1
    
    "return bloc.reshape(-1)"
    return np.concatenate((quantitzacio,bloc.reshape(-1)))

def Cuantizacion_uniforme_adaptativa(imagen, bits=3, n_bloque=8):
    print("Cuantizando, tada un par de segundos")
    imagenCopy = imagen.copy()
    nivells = 2**3
    m = len(imagenCopy) #files
    n = len(imagenCopy[0]) #columnes
    imagenCodigo = np.asanyarray([n,m,n_bloque,bits])
    imagenCopy = pasarABloques(imagenCopy, len(imagen), len(imagen[0]))
    n_bloques = n_bloques = len(imagenCodigo)
    for i in range(len(imagenCopy)):
        quantitzarBloc(imagenCodigo, bloc, nivells)
        
        
    return imagenCodigo

imagenCodigo = Cuantizacion_uniforme_adaptativa(imagen, bits=3, n_bloque=8)
    
    
"""
imagen: imagen a cuantizar
bits: número de bits necesarios para cuantizar cada bloque, 
      o sea que en cada bloque habrá 2**bits valores diferentes como máximo
n_bloque: se consideran bloques de tamaño n_bloque*n_bloque 

imagenCodigo: es una lista de la forma
[[n,m,n_bloque,bits],[[minimo,maximo],bloqueCodificado],...,[[minimo,maximo],bloqueCodificado]]

siendo:
[n,m,n_bloque,bits] información de la imagen
  n: número de filas de la imagen
  m: número de columnas de la imagen
  n_bloque: tamaño de los bloques usados (múltiplo de n y m)
Ejemplo: [1024, 1024, 8, 3]

[[minimo,maximo],bloqueCodificado] información de cada bloque codificado
minimo: valor mínimo del bloque
maximo: valor máximo del bloque
bloqueCodificado: array de tamaño n_bloque*n_bloque que contiene en cada 
  posición a que intervalo de cuantización correspondía el valor del píxel
  correspondiente en la imagen

Ejemplo: sabemos que trabajamos con bloques 8x8 y que hemos cuantizado en 2**3=8 niveles
    [[85, 150], 
    Array([[4, 0, 0, 4, 7, 7, 6, 7], 
           [4, 3, 1, 1, 4, 7, 7, 6],
           [6, 6, 3, 0, 0, 4, 6, 6], 
           [6, 6, 5, 3, 1, 0, 3, 6],
           [6, 5, 6, 6, 4, 0, 0, 3],
           [5, 6, 6, 6, 6, 4, 2, 0],
           [6, 6, 5, 5, 6, 7, 4, 1],
           [6, 6, 5, 5, 5, 6, 6, 5]]  
   El valor mínimo de los píxeles del bloque era 85 y el máximo 150, por lo 
   tanto los límites de decisión son:
       [85.0, 93.25, 101.5, 109.75, 118.0, 126.25, 134.5, 142.75, 151.0]
   el valor del primer pixel (4) estaría entre 109.75<=p<118
   el valor del segundo pixel pixel (0) estaría entre 85<=p<93.25...
   
      
Importante: Trabajar con Arrays de Numpy

"""


#%%
"""
Definir una funcion que dada una imagen codificada por la función 
Cuantizacion_uniforme_adaptativa() muestre la imagen

"""
def Dibuja_imagen_cuantizada(imagenCodigo):
    plt.figure()
    plt.xticks([])
    plt.yticks([])
    plt.imshow(Imagen_cuantizada(imagenCodigo), cmap=plt.cm.gray,vmin=0, vmax=255)
    plt.show()
    
def Imagen_cuantizada(imagenCodigo):
    imagen = imagenCodigo.copy()
    n = imagen[0]
    m = imagen[1]
    n_bloque = imagen[2]
    bits = imagen[3]
    sizeBloque = n_bloque*n_bloque
    result = np.array([])
    i = 4
    while (i < len(imagen)):
        maximo = imagen[i]
        minimo = imagen[i+1]
        bloque = imagen[i+2:i+2+sizeBloque]
        bloque = DescuantizarBloque(maximo,minimo, bloque, sizeBloque)
        result = np.concatenate((result,bloque))
        i+=sizeBloque+2
    return pasarAImagen(n,m,result,n_bloque).astype(int)
    """imagenPIL=PIL.Image.fromarray(result)
    return imagenPIL"""

def DescuantizarBloque(maximo,minimo, bloque, sizebloque):
    dif = maximo - minimo
    i = 0
    while i < sizebloque:
        minimoLocal = bloque[i]*dif + minimo
        bloque[i] = int((minimoLocal+dif)/2)
        i+=1
    return bloque

def pasarAImagen(n,m,array,n_bloque):
    img = np.zeros((n, m))
    z = 0
    for i in range(int(n / 8)):
        for j in range(int(m / 8)):
            aux = array[z:z+(n_bloque*n_bloque)]
            aux = np.reshape(aux,(n_bloque,n_bloque))
            img[i*n_bloque:i*n_bloque+n_bloque,j*n_bloque:j*n_bloque+n_bloque] = aux
            z += 1
    return img
            
Dibuja_imagen_cuantizada(imagenCodigo)
 #%%   
 
"""
Aplicar vuestras funciones a las imágenes que encontraréis en la carpeta 
standard_test_images hacer una estimación de la ratio de compresión
"""

       

#%%
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
#%%
"""
Algunas sugerencias que os pueden ser útiles
"""

# Divido todos los píxeles de la imagen por q
# a continuación redondeo todos los píxeles
# a continuación sumo 1/2 a todos los píxeles de la imagen
# a continuación convierto los valores de todos los píxeles en enteros de 8 bits sin signo
# por último múltiplico todos los píxeles de la imagen por q

bits=3
q=2**(bits) 
imagen2=((np.floor(imagen/q)+1/2).astype(np.uint8))*q

# dibujo la imagen cuanzizada resultante

fig=plt.figure()
fig.suptitle('Bloques: '+str(bits)+' bits/píxel')
plt.xticks([])
plt.yticks([])
plt.imshow(imagen2, cmap=plt.cm.gray,vmin=0, vmax=255) 
plt.show()


# Lectura y escritura de objetos

import pickle

fichero='QScalar'

with  open(fichero+'_dump.pickle', 'wb') as file:
    pickle.dump(imagenCodigo, file)


with open(fichero, 'rb') as file:
    imagenLeidaCodificada=pickle.load(file)


# Convertir un array en imagen, mostrarla y guardarla en formato png.
# La calidad por defecto con que el ecosistema python (ipython, jupyter,...)
# muestra las imágenes no hace justicia ni a las imágenes originales ni a 
# las obtenidas tras la cuantización.     

import PIL

imagenPIL=PIL.Image.fromarray(imagenRecuperada)
imagenPIL.show()
imagenPIL.save(fichero +'_imagen.png', 'PNG')
