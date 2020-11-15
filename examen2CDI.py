# -*- coding: utf-8 -*-
"""
Created on Tue May 26 17:53:30 2020

@author: Marc
"""

import numpy as np
from scipy import misc
from math import sqrt,log2,log
import matplotlib.pyplot as plt
from PIL import Image
import pywt


"-----------------EXERCICI PREFIJO-----------------"

def prefix_code(lst):
    output = []
    sumatorio = 0
    for i in lst:
        sumatorio += 2**(-i)
    if(sumatorio > 1):
        return output
    else:
        for index, i in enumerate(lst):
            if(index is 0):
                output.append(bin(0)[2:].zfill(i))
            else:
                for j in range(0, 2**i):
                    prefix = False
                    aux = bin(j)[2:].zfill(i)
                    for binword in output:
                        prefix = ((aux.startswith(binword)) or (binword.startswith(aux)))
                        if prefix :
                            break
                    if not prefix:
                        output.append(aux)
                        break
    return output

prova = [3,3,3,5,5,6,6,7,8,8,9,9,9]
binarywords = prefix_code(prova)
if not binarywords:
    print ("no")
else:
    print("yes")
    [print(binword)for binword in binarywords]


"-----------------EXERCICI code LZ77-----------------"

def LZ77Code(mensaje,S=12,W=18):
	code=[[0,0,mensaje[0]]]
	mydict=[[0,0,mensaje[0]]]
	i=1#donde estamos leyendo carácteres
	ahead=W-S
	lookahead=mensaje[1:1+ahead]
	old=str(mensaje[max(0,i-S-1):max(0,i)])
	while i < len(mensaje):
		offset=0
		length=0
		char=lookahead[0]
		window = old+lookahead
		#miramos matches 
		for j in range(len(old)-1,-1,-1):
			if old[j] == lookahead[0]:
				#tenemos algun match
				match=True
				izq=j+1
				der=len(old)+1
				maxlen=1
				#longest prefix match
				while match and der <len(window):
					if window[izq] == window[der]:
						izq+=1
						der+=1
						maxlen+=1
					else: 
						match=False
				#extendemos carácteres extra
				if maxlen> length :
					offset= len(old) -j
					length= maxlen
					try :
						char= window[der]
					except:
						try:
							char= window[i+length]
						except:
							char=window[der-1]
							length -=1
							if length == 0:
								offset=0
							
		code=code+[[offset,length,char]]
		i += length+1
		old=str(mensaje[max(0,i-S):i])
		lookahead= str(mensaje[i:ahead+i])
	code[-1]=[code[-1][0],code[-1][1]+1,'EOF']
	return code

mensaje = 'abcdeabaebbadab'
code = LZ77Code(mensaje, 12, 18)
print(code)

 , 0.0128,  0.016, , 0.0051, 0.0102, ]
"-----------------EXERCICI decode LZ77-----------------"

def LZ77Decode(codigo):
	mensaje=''
	for i in codigo:
		if i[0] != 0:
			pos=len(mensaje)-i[0]
			word=mensaje[pos:pos+ i[1]] 
			extension= ""
			mensaje += word 
			if i[0] <= i[1]:#debemos extender el último simbolo
				mensaje += mensaje[i[0]+1:i[1]+1] 
		mensaje+= i[2]
	return mensaje[:-3]


def LZ77Decode(codigo):
	mensaje=''
	for i in codigo:
		if i[0] != 0:
			pos=len(mensaje) - i[0]
			word=mensaje[pos:pos+ i[1]] 
			extension= ""
			mensaje += word 
			if i[0] <= i[1]:#debemos extender el último simbolo
				mensaje += mensaje[i[0]+1:i[1]+1] 
		mensaje+= i[2]
	return mensaje[:-3]

def LZ78Decode(codigo):
    mensaje=''
    diccionario=[]
    n=len(codigo)
    for i in range(n-1):
        indice=codigo[i][0]
        letra=codigo[i][1]    
        if indice==0:
            mensaje+=letra
            diccionario+=[letra]
        else:
            palabra=diccionario[indice-1]+letra
            mensaje+=palabra
            diccionario+=[palabra]

            
    indice=codigo[n-1][0]
    letra=codigo[n-1][1]

    if indice>0:
        palabra=diccionario[indice-1]
        mensaje+=palabra
      
    return mensaje, diccionario















"-----------------EXERCICI quins son codis-----------------"

def prefix_code(code):
    for binword in code:
        for aux in code:
            if(binword !=aux):
                prefix = ((aux.startswith(binword)) or (binword.startswith(aux)))
                if(prefix):
                    return ("no")
    return ("yes")

code = ['00','11','001','111','0111', '01111','10000']
print(prefix_code(code))
"-----------------EXERCICI MATRIU ORTOGONAL-----------------"
"S'ha de mirar quina matriu multiplicada per la transposada dona algo rollo [1,0,0][0,1,0][0,0,1]
 
matrix1=[[2/3,2/3,1/3],
         [-(sqrt(2))/2,(sqrt(2))/2,0],
         [-(sqrt(2))/6,-(sqrt(2))/6,2*(sqrt(2))/3]]

matrix2=[[2/3,2/3,1/3],
         [(sqrt(2))/2,(sqrt(2))/2,(sqrt(2))/4],
         [-(sqrt(2))/6,-(sqrt(2))/6,2*(sqrt(2))/3]]

matrix3= [[2,2,1],
          [4,4,2],
          [-2,-2,8]]

matrix4 = [[2,2,1],
           [-2,2,0],
           [-2,-2,8]]

"fer aixo x cada 1"

mat = np.asarray(matrix1)
"print(mat.transpose())"
mat1T=(np.dot(mat,mat.transpose()))

mat = np.asarray(matrix2)
"print(mat.transpose())"
mat2T=(np.dot(mat,mat.transpose()))

mat = np.asarray(matrix3)
"print(mat.transpose())"
mat3T=(np.dot(mat,mat.transpose()))

mat = np.asarray(matrix4)
"print(mat.transpose())"
mat4T=(np.dot(mat,mat.transpose()))

"*---------------------------------------------------------------------------*"

"-----------------EXERCICI RATIO D COMPRESSIÖ-----------------"

def ratio_de_compression(pixeles,escala,entradas,pixelesB):
    num = pixeles*pixeles*log2(escala)
    den = (pixeles/pixelesB)*(pixeles/pixelesB)*log2(entradas) + entradas*pixelesB*pixelesB*log2(escala)
    return num/den

ratio_de_compression(512,128,128,4)



"-----------------EXERCICI WAVELET-----------------"
l2 = [0.28,0.8481,0.4271,-0.141]
l3= [-0.32,0.2481,-0.1729,-0.741]
l = [0.28,0.8481,0.4271,-0.141]
suman = 0
suma2 = 0
for i in l:
    suman += i
    suma2 += (i**2)
print(suman,"=", sqrt(2))
print("1 =",suma2)
print((l[2]*l[0])+(l[3]*l[1]))

"-----------------EXERCICI BLOC DE COLORS-----------------"


def idc_bloque(p):
    "Substituir x valor de l'exercici"
    c = [[0.0, -0.5773502691896257, 0.8164965809277261, 0.0],
[0.0, -0.5773502691896257, -0.40824829046386313, -0.7071067811865475],
[0.0, -0.5773502691896257, -0.408248290463863, 0.7071067811865477],
[1.0, 0.0, 0.0, 0.0]]
    ct = np.transpose(c)
    return (np.tensordot(np.tensordot(ct,p,axes=([1],[0])), c, axes = ([1],[0]))).reshape(-1)

fig = plt.figure()
array = np.zeros((4,4))
array = array.astype(int)
for i in range(4):
    for j in range(4):
        array[i][j] = 1
        m = idc_bloque(array)
        fig.add_subplot(4,4,i*4+j+1).axis('off')
        plt.imshow(m.reshape((4,4)))
        array[i][j] = 0


def LZ78Decode(codigo):
    mensaje=''
    diccionario=[]
    n=len(codigo)
    for i in range(n-1):
        indice=codigo[i][0]
        letra=codigo[i][1]    
        if indice==0:
            mensaje+=letra
            diccionario+=[letra]
        else:
            palabra=diccionario[indice-1]+letra
            mensaje+=palabra
            diccionario+=[palabra]

            
    indice=codigo[n-1][0]
    letra=codigo[n-1][1]

    if indice>0:
        palabra=diccionario[indice-1]
        mensaje+=palabra
      
    return mensaje, diccionario