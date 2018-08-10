# !/usr/bin/env python
import numpy as np
from keras.models import load_model
import rospy
from sensor_msgs.msg import CompressedImage
import cv2
from std_msgs.msg import Int16
import time
import matplotlib.image as mpimg

global pub_1
global min
global max
global lastTime, hlat
global maxLat, count, index

# Opción para reducir la dimensión de las imágenes
reduce = True

# Valores iniciales
pub_1 = 10
min = 1
max = 0
maxLat = 0
count = 0
index = 0
hlat = 0


def mi_callback(ros_data, args):
    start_time = time.time()
    global pub_1, min, max, hlat
    global lastTime, maxLat, count
    global index
    modelo = args[0]
    pub_speed = args[1]
    pub_steering = args[2]
    r = rospy.Rate(30)

    if  pub_1 < 10:
        pub_speed.publish(-400)
        print("speed -400")
        pub_1 += 1

    np_arr = np.fromstring(ros_data.data, np.uint8)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    if reduce:
        image_np = cv2.resize(image_np, (320, 240), interpolation=cv2.INTER_CUBIC) # NEW
        #image_np = cv2.resize(image_np, (132, 145), interpolation=cv2.INTER_CUBIC) # last used
    angulo = (modelo.predict(image_np[None, :, :, :], batch_size=1, verbose=0))

    print("angulo", angulo)
    elapsed_time = time.time() - start_time
    # tiempo que tarda en predecir
    print('Tiempo: %.3f[s]' % (elapsed_time))
    pub_steering.publish(int(angulo))  # Publica el valor obtenido
    if elapsed_time < min:
        min = elapsed_time;
    if elapsed_time > max:
        max = elapsed_time;
    # Imprime el minimo y máximo tiempo que tarda la red en publicar
    print("min:", min, "max:", max)
    sometime = time.time() - lastTime
    if sometime > maxLat and count > 1:
        maxLat = sometime
        index = count
    if sometime > 0.5:
        hlat = sometime
    print("Latencia: %.6f[s], Último valor pico %.6f[s]" %(sometime, hlat))
    print("máxima Latencia%.6f[s] en frame %d" % (maxLat, index))
    lastTime = time.time()
    print("---------------------------\n")
    count +=1
    r.sleep()


def rosListener(modelo):  # Subscribe los tópicos
    rospy.init_node('nnpy', anonymous=True)
    pub_speed = rospy.Publisher('/manual_control/speed', Int16, queue_size=1)
    pub_steering = rospy.Publisher('/manual_control/steering', Int16, queue_size=1)

    # para subscribir el tópico de la imagen comprimida
    rospy.Subscriber("/app/camera/rgb/image_raw/compressed", CompressedImage, mi_callback, (modelo, pub_speed, pub_steering), queue_size=5)
    rospy.spin()


if __name__ == '__main__':
    path = '/home/dv_user/Documents/VirtualCIC/Transfer_flatten/'

    global lastTime
    lastTime = time.time()

    modeloEntrenado = load_model(path + 'model.h5') #20_2_18E3.h5, 16_4_18_E1.h5(best)
    # Se carga una imágen de prueba, sin este paso la red no manda datos al subscribirse al tópico
    image_np = mpimg.imread("/home/dv_user/Documents/imag_cap/" + 'outfile.jpg')  # No borrar los siguientes códigos
    if reduce:
        image_np = cv2.resize(image_np, (320, 240), interpolation=cv2.INTER_CUBIC)
        #image_np = cv2.resize(image_np, (132, 145), interpolation=cv2.INTER_CUBIC)
    angulo = (modeloEntrenado.predict(image_np[None, :, :, :], batch_size=1, verbose=0))
    angulo = np.asarray(angulo)[0][0]
    print(angulo)  # Imprime un valor de prueba

    rosListener(modeloEntrenado)