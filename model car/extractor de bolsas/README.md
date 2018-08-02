# Requisitos:
python 2, ros, bolsa de ros

nombreBolsa.bag con los topicos:
	/app/camera/rgb/image_raw/compressed
	/manual_control/speed
	/manual_control/steering

Opcional: archivo para selecionar frames "util_data"

### Extraer datos de entrenamiento
python bag2DataTrainTCompresed.py nombreBolsa.bag

### Limpiar datos utilizando un archivo auxiliar
python clearDataBag.py util_data

Requiere un archivo con los frames que desee conservar,
el primer frame empieza con 1 hasta el numero de mensajes en la bolsa.
Removera todo dato que NO este indexado en este archivo 

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
La última línea del archivo debe ser un numero o un rango, no dejar líneas en blanco
32-40: <- Aquí termina el archivo
<- No debe haver líneas despues de los números

