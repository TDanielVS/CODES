import csv
import numpy as np
import matplotlib.image as mpimg
from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Cropping2D, AveragePooling2D, Dropout
from keras.layers.convolutional import Convolution2D
from sklearn.model_selection import train_test_split
import sklearn
import time
import matplotlib.pyplot as plt
import random

path = '/home/user/Documents/DataSet/'
path_image = path + 'IMG/'

model_name = "entrenamiento"
samples = []
angulos = []

# Contenido del archivo driving_log.csv:
#  CenterImage| LeftImage| RightImage| Steering Angle| Throttle| Break| Speed
# [0            , 1         , 2         , 3             , 4     , 5     , 6]
Angulo = 3
plotear = True  # Opción para plotear
BINS = 200  # Resolución del plot

with open(path + 'driving_log.csv') as csvfile:  # lectura del archivo csv
    reader = csv.reader(csvfile)
    for line in reader:
        angle = float(line[Angulo])  # Steering Angle
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
times = seconds.count(val)  # Get concurrences
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
limite = int(times * 0.5)  # proporción
print("Permitir:", limite, "de", val_max)
angulos.clear()
for i, data in enumerate(samples2):
    angulos2.append(data[Angulo])
    val_max = angulos2.count(data[Angulo])
    if val_max <= limite:
        cleared_samples.append(data)
        angulos.append(float(data[Angulo]))
        angulosFlip.append(float(data[Angulo]))
        angulosFlip.append(-float(data[Angulo]))

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

# Generador batch para entrenar la red
def generator(samples, batch_size=32):
    num_samples = len(samples)
    while 1:
        samples = sklearn.utils.shuffle(samples)
        for offset in range(0, num_samples, batch_size):
            batch_samples = samples[offset:offset + batch_size]
            images, steering = [], []
            for batch_sample in batch_samples:
                angle = float(batch_sample[Angulo])  # Ángulo
                image_name = batch_sample[0].split('\\')[-1]  # imagen de CenterImage
                image = mpimg.imread(path_image + image_name)
                image_flipped = np.fliplr(image)  # Espejo de la imagen
                images.append(image)
                steering.append(angle)
                images.append(image_flipped)
                steering.append(-angle)  # Espejo del ángulo
            x_train = np.array(images)
            y_train = np.array(steering)
            yield sklearn.utils.shuffle(x_train, y_train)


# Separa el conjunto de datos en entrenamiento y validación
train_samples, validation_samples = train_test_split(samples, test_size=0.2)
train_generator = generator(train_samples, batch_size=16)
validation_generator = generator(validation_samples, batch_size=16)

# Arquitectura de la red
model = Sequential()
model.add(Cropping2D(cropping=((80, 20), (0, 0)), input_shape=(160, 320, 3)))
model.add(AveragePooling2D(pool_size=(1, 4), name="Resize", trainable=False))
model.add(Lambda(lambda x: x / 127.5 - 1., name="Normalize"))  # lambda x: x/127.5 - 1.
model.add(Convolution2D(3, 5, 5, subsample=(2, 2), activation="relu"))
model.add(Convolution2D(24, 3, 3, subsample=(2, 2), activation="relu"))
model.add(Convolution2D(36, 3, 3, subsample=(1, 1), activation="relu"))
model.add(Convolution2D(48, 3, 3, subsample=(1, 1), activation="relu"))
model.add(Convolution2D(64, 3, 3, activation="relu"))
model.add(Convolution2D(64, 3, 3, activation="relu"))
model.add(Dropout(0.1))
model.add(Flatten())
model.add(Dense(100, activation="relu"))
model.add(Dense(50, activation="relu"))
model.add(Dense(10, activation="relu"))
model.add(Dense(1, trainable=False))

# Tiempo inicial
start_time = time.time()
model.compile(loss='mse', optimizer='adam')
model.summary()
history_object = model.fit_generator(train_generator, samples_per_epoch=len(train_samples) * 2,
                                     validation_data=validation_generator, nb_val_samples=len(validation_samples),
                                     nb_epoch=2)

model.save(model_name + '.h5')
# Imprimir el tiempo que tardó el entrenamiento en segundos
elapsed_time = time.time() - start_time
print('Tiempo: %.3f[s]' % (elapsed_time))

plt.plot(history_object.history['loss'], label='train')
plt.plot(history_object.history['val_loss'], label='val')
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.savefig(model_name + ".jpg")
plt.clf()

exit()
