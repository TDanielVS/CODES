import csv
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Cropping2D, Dropout
from keras.layers.convolutional import Convolution2D
from sklearn.model_selection import train_test_split
import sklearn
import time
import random
from keras import callbacks
import cv2

path = '/home/user/Documents/DataSet/'  # TODO: change dataset path 
path_image = path + 'imagenesBolsa/'

samples = []
angulos = []

# Contenido del archivo datosBolsa.csv
# [Image name, Speed value, Steering value]
ANGULO = 2
VELOCIDAD = 1
IMAGEN = 0

plotear = True
BINS = 200

with open(path + 'datosBolsa.csv') as csvfile:
    reader = csv.reader(csvfile)
    lineas = list(reader)[1:]  # Remover primer fila
    random.shuffle(lineas)  # Random
    for line in lineas:
        angle = float(line[ANGULO])
        samples.append(line)
        angulos.append(angle)

# Plot de la distribución del conjunto de datos
if plotear:
    plt.hist(angulos, normed=False, bins=BINS)
    plt.show()


# Balancear los datos
val_max = max(set(angulos), key=angulos.count)
times = angulos.count(val_max)
print("Valor que más se repite:", val_max, "encontrado", times, "veces")

seconds = angulos.copy()
for i in range(times):  # elimina el valor que más se repite
    seconds.remove(val_max)

val = max(set(seconds), key=seconds.count)  # El más repetido ahora
times = seconds.count(val)
print("Segundo que más se repite:", val, "encontrado", times, "veces")

# Plot de la distribución sin el más repetido
if plotear:
    plt.hist(seconds, normed=False, bins=BINS)
    plt.show()

# Limpiar arreglos
seconds.clear()
cleared_samples = []
angulos2 = []
angulosFlip = []
count = 0

samples2 = samples.copy()
random.shuffle(samples2)
# Se elige una proporción entre los datos más repetidos y los segundos más repetidos
# Para permitir aleatoriamente quedarnos con esa cantidad de datos
limite = int(times * 0.5)
print("Permitir:", limite, "de", val_max)
angulos.clear()
for i, data in enumerate(samples2):
    angulos2.append(data[2])
    val_max = angulos2.count(data[2])
    if val_max <= limite:
        cleared_samples.append(data)
        angulos.append(float(data[2]))
        angulosFlip.append(float(data[2]))
        angulosFlip.append(180 - float(data[2]))

print("Cantidad de datos: ", len(samples))
random.shuffle(cleared_samples)
samples = cleared_samples
num = len(samples)
print("Cantidad quitando exedente: ", num)
print("Cantidad del data set con espejo:", num * 2)

if plotear:
    # Plot de los datos con la proporcion que se permite usar
    plt.hist(angulos, normed=False, bins=BINS)
    plt.show()
    # Plot del conjuto de datos balanceado
    plt.hist(angulosFlip, normed=False, bins=BINS)
    plt.show()

## Valores velocidad, dirección
# izq=180, centro = 90, der=0
# -adelante +reversa  :MAXIMOS ! [-2500, 2500]

# Generador batch para entrenar la red
def generator(samples, batch_size=32):
    num_samples = len(samples)
    while 1:
        samples = sklearn.utils.shuffle(samples)
        for offset in range(0, num_samples, batch_size):
            batch_samples = samples[offset:offset + batch_size]
            images, steering = [], []
            for batch_sample in batch_samples:
                angle = float(batch_sample[ANGULO])  # Ángulo
                image_name = batch_sample[IMAGEN]  # Imagen
                image = mpimg.imread(path_image + image_name)
                image = cv2.resize(image, (320, 240), interpolation=cv2.INTER_CUBIC)
                images.append(image)
                steering.append(angle)
                image_flipped = np.fliplr(image)
                images.append(image_flipped)
                steering.append(180 - angle)  # Espejo del ángulo
            x_train = np.array(images)
            y_train = np.array(steering)
            yield sklearn.utils.shuffle(x_train, y_train)


# Separa el conjunto de datos en entrenamiento y validación
train_samples, validation_samples = train_test_split(samples, test_size=0.2)
train_generator = generator(train_samples, batch_size=16)
validation_generator = generator(validation_samples, batch_size=16)

# Arquitectura de la red
model = Sequential()
model.add(Lambda(lambda x: x / 255.0 - 0.5, input_shape=(240, 320, 3)))
model.add(Cropping2D(cropping=((48, 0), (0, 0))))
model.add(Convolution2D(3, 5, 5, subsample=(2,2), activation="relu"))
model.add(Convolution2D(24, 5, 5, subsample=(2, 2), activation="relu"))
model.add(Convolution2D(36, 5, 5, subsample=(2, 2), activation="relu"))
model.add(Convolution2D(48, 5, 5, subsample=(2, 2), activation="relu"))
model.add(Convolution2D(64, 3, 3, activation="relu"))
model.add(Convolution2D(64, 3, 3, activation="relu"))
model.add(Dropout(0.1))
model.add(Flatten())
model.add(Dense(100, activation="relu"))
model.add(Dense(50, activation="relu"))
model.add(Dense(10, activation="relu"))
model.add(Dense(1))

# Tiempo inicial
start_time = time.time()
model.compile(loss='mse', optimizer='adam')
model.summary()
earlyStopping=callbacks.EarlyStopping(monitor='val_loss', patience=10, verbose=1, mode='auto')
saveBestModel = callbacks.ModelCheckpoint(filepath=path+'model.h5', monitor='val_loss', verbose=1, save_best_only=True, mode='auto')
history_object = model.fit_generator(train_generator, samples_per_epoch=len(train_samples)*2,
                    validation_data=validation_generator, nb_val_samples=len(validation_samples)
                    , nb_epoch=50, callbacks=[earlyStopping, saveBestModel])

# Imprimir el tiempo que tardó el entrenamiento en segundos
elapsed_time = time.time() - start_time
print('Tiempo: %.3f[s]' % (elapsed_time))

print(history_object.history.keys())
plt.plot(history_object.history['loss'], label='train')
plt.plot(history_object.history['val_loss'], label='test')
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()


exit()
