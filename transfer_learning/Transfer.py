import csv
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from keras.models import Model
from keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
import sklearn
import time
import random
from keras import callbacks
import cv2
from keras.models import load_model

path = '/home/user/Documents/SataSet/'
path_image = path + 'imagenesBolsa/'
# CSV: imágen, velocidad, dirección

plotear = True
BINS = 200
ANGULO = 2
VELOCIDAD = 1
IMAGEN = 0

samples = []
angulos = []
with open(path + 'datosBolsa.csv') as csvfile:  # reading of file csv
    reader = csv.reader(csvfile)
    lineas = list(reader)[1:]  # Remove header
    random.shuffle(lineas)  # Random data
    for line in lineas:
        angle = float(line[ANGULO])  # Steering angle
        angle = (angle - 90) / 90
        samples.append(line)
        angulos.append(-angle)

if plotear:
    plt.hist(angulos, normed=False, bins=BINS)
    plt.show()

## Balance data #####
val_max = max(set(angulos), key=angulos.count)
print(val_max)
times = angulos.count(val_max)
maxtimes = angulos.count(val_max)
print(times)
seconds = angulos.copy()

for i in range(times):  # remove most repeated value
    seconds.remove(val_max)

val = max(set(seconds), key=seconds.count)  # Get most repeated
print(val)
times = seconds.count(val)  # Get concurrences
print(times)
if plotear:
    plt.hist(seconds, normed=False, bins=BINS)
    plt.show()
seconds.clear()

cleared_samples = []
angulos2 = []
angulosFlip = []
count = 0

samples2 = samples.copy()
random.shuffle(samples2)
limite = int(times * 2)
print("limit:", limite)
angulos.clear()
for i, data in enumerate(samples2):
    angulos2.append(data[2])
    val_max = angulos2.count(data[2])
    if val_max <= limite:
        cleared_samples.append(data)
        angulo = (float(data[2]) - 90) / 90
        angulos.append(angulo)
        angulosFlip.append(angulo)
        angulosFlip.append(- angulo)

print("samples: ", len(samples))
random.shuffle(cleared_samples)
samples = cleared_samples
num = len(samples)
print("Taken: ", num)
print("Taken + Flip:", num*2)

if plotear:
    plt.hist(angulos, normed=False, bins=BINS)
    plt.show()

    plt.hist(angulosFlip, normed=False, bins=BINS)
    plt.show()


def generator(samples, batch_size=32):
    num_samples = len(samples)
    while 1:  # Loop forever so the generator never terminates
        samples = sklearn.utils.shuffle(samples)
        for offset in range(0, num_samples, batch_size):
            batch_samples = samples[offset:offset + batch_size]
            images, steering = [], []
            for batch_sample in batch_samples:
                angle = float(batch_sample[ANGULO])  # Steering angle
                angle = (angle - 90) / 90
                image_name = batch_sample[IMAGEN]  # name of image
                image = mpimg.imread(path_image + image_name)
                image = cv2.resize(image, (320, 240), interpolation=cv2.INTER_CUBIC)
                images.append(image)  # append image to array
                steering.append(-angle)  # append steering angle to array  #+
                image_flipped = np.fliplr(image)
                images.append(image_flipped)  # flipped
                steering.append(angle)  # flipped   #-
            x_train = np.array(images)
            y_train = np.array(steering)
            yield sklearn.utils.shuffle(x_train, y_train)


train_samples, validation_samples = train_test_split(samples, test_size=0.2)  # 0.25

print("val samples: ", len(validation_samples))
print("train_samples: ", len(train_samples))

# compile and train the model using the generator function
train_generator = generator(train_samples, batch_size=16)
validation_generator = generator(validation_samples, batch_size=16)

ACTIV = 'softplus'

modelo_path = path + "preTrainModel.h5"
start_time = 0

modelA = load_model(modelo_path);
modelA.summary()
model2 = Model(input= modelA.input, output=modelA.layers[-5].output)
for layer in model2.layers:
    layer.trainable = True
model2.summary()
D1 = Dense(100, activation=ACTIV)(model2.layers[-1].output)
D2 = Dense(50, activation=ACTIV)(D1)
dr2 = Dropout(0.1, name="dropout_3")(D2)
D3 = Dense(10, activation=ACTIV)(dr2)
S = Dense(1, activation='linear')(D3)

model = Model(input=model2.input, output=S)

start_time = time.time()
model.compile(loss='mse', optimizer='adam')
model.summary()
earlyStopping=callbacks.EarlyStopping(monitor='val_loss', patience=3, verbose=1, mode='auto')
saveBestModel = callbacks.ModelCheckpoint(filepath=path+'model.h5', monitor='val_loss', verbose=1, save_best_only=True, mode='auto')
history_object = model.fit_generator(train_generator, samples_per_epoch=len(train_samples)*2,
                    validation_data=validation_generator, nb_val_samples=len(validation_samples)
                    , nb_epoch=7, callbacks=[earlyStopping, saveBestModel])#

elapsed_time = time.time() - start_time
print('Tiempo: %.3f[s]' % (elapsed_time))

# list all data in history
print(history_object.history.keys())
plt.plot(history_object.history['loss'], label='train')
plt.plot(history_object.history['val_loss'], label='test')
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()

exit()
