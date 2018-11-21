## ENGLISH
# Requirements:
python 2.7, ros indigo or newer, ros bag file

<Rosbag_name>.bag with topics:

	/app/camera/rgb/image_raw/compressed
	
	/manual_control/speed
	
	/manual_control/steering


Optional: file to select frames "util_data"

### Extract training data
The command below extracts all images from a bag file in to a folder
"imagenesBolsa" and its related file "datosBolsa.csv"

An example were the script is in the same folder as the ros bag file:
```
python2 bag2DataTrainTCompresed.py <nombre_de_la_Bolsa>.bag
```

### Clear data using auxiliary file
The script searches from "imagenesBolsa" and "datosBolsa.csv" in the actual folder
```
python2 clearDataBag.py util_data
```
This requiere a file whit the frames wanna conserve in it,
frames are from 1 to the last message in the bag file.
All frames NOT indicated in the file will be removed.
 

### A valid example from util_data content:
----
1-15

18

25-29

40-100

102

----

The file will keep all frames indicated in the file.

10-25: take all frames from 10 to 25

30: Adds only the frame 30

# NOTE
Last line in the auxiliar file must be a number NOT a blank line, Do not left empty lines or spaces.

32-40: <- Here ends the file

<- Do not must be empty lines after any numbers

_______________________________
_______________________________
## ESPAÑOL
# Requisitos:
python 2.7, ros indigo o superior, bolsa de ros

<nombre_de_la_Bolsa>.bag con los topicos:

	/app/camera/rgb/image_raw/compressed
	
	/manual_control/speed
	
	/manual_control/steering


Opcional: archivo para selecionar frames "util_data"

### Extraer datos de entrenamiento
El siguiente comando extrae las imágenes en una carpeta llamada 
"imagenesBolsa" y crea el archivo "datosBolsa.csv"

Suponiendo que el script se encuentra en la misma carpeta que la bolsa de ros:
```
python2 bag2DataTrainTCompresed.py <nombre_de_la_Bolsa>.bag
```

### Limpiar datos utilizando un archivo auxiliar
El script busca "imagenesBolsa" y "datosBolsa.csv" en la carpeta actual
```
python2 clearDataBag.py util_data
```
Requiere un archivo con los frames que desee conservar,
el primer frame empieza con 1 hasta el numero de mensajes en la bolsa.
Removera todo frame que NO este indicado en este archivo 

### Ejemplo válido del contenido de util_data:
----
1-15

18

25-29

40-100

102

----

El archivo conservará los frames indicados en el archivo.

10-25: toma los frames del 10 al 25

30: Agrega solo el frame 30

# NOTA
La última línea del archivo debe ser un numero o un rango, no dejar líneas en blanco ni espacios.

32-40: <- Aquí termina el archivo

<- No debe haver líneas en blanco despues de los números

