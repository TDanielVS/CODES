import os, shutil, argparse
from cv_bridge import CvBridge, CvBridgeError
import cv2, rosbag, csv

def save_topics(bag=None, num_msgs=None, topics=None, bag_name=''):
    num_ceros = len(str(num_msgs))
    bridge = CvBridge()

    # Create images folder
    path_save = 'imagenesBolsa'
    if os.path.exists(path_save):
        shutil.rmtree(path_save)  # remove old path
    os.makedirs(path_save)

    # Write header csv
    file_csv = open('datosBolsa.csv', 'wt')
    writer = csv.writer(file_csv)
    writer.writerow(('Image name', 'Speed value', 'Steering value'))
    print "Creando datos ..."
    image_list = []
    speed_list = []
    steering_list = []
    count = 1
    for topic, msg, t in bag.read_messages():
        if topic == topics[0]:  # image_raw_compresed
            try:
                cv_image = bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
            except CvBridgeError, e:
                print e

            image_name = "image_raw_" + str(count).rjust(num_ceros, '0') + "_" + bag_name + ".jpg"
            tiempo = str(t)
            image_list.append({tiempo: image_name})
            cv2.imwrite(os.path.join(path_save, image_name), cv_image)
            count += 1

        if topic == topics[1]:  # speed
            tiempo = str(t)
            val = str(msg).split()[-1]
            speed_list.append({tiempo: val})

        if topic == topics[2]:
            tiempo = str(t)
            val = str(msg).split()[-1]
            steering_list.append({tiempo: val})

    image_list.sort()
    speed_list.sort()
    steering_list.sort()

    for i, (im_dic, sp_dic, st_dic) in enumerate(zip(image_list, speed_list, steering_list)):
        llave = im_dic.keys()[0]
        dato1 = dict(im_dic).get(llave)
        llave = sp_dic.keys()[0]
        dato2 = dict(sp_dic).get(llave)
        llave = st_dic.keys()[0]
        dato3 = dict(st_dic).get(llave)

        comp = str(dato1).split('_')[2]
        if int(comp) != i+1:
            print "No se ordeno" + comp
            return 1

        writer.writerow((dato1, dato2, dato3))

    file_csv.close()
    print "Se han creado los datos"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bagfile')  # Args = bagName.bag
    args = parser.parse_args()

    bag = rosbag.Bag(args.bagfile, 'r')
    name_bag = str(args.bagfile).split(".")[0]
    print "Se ha cargado la bolsa %s" % (args.bagfile)
    image_topic = '/app/camera/rgb/image_raw/compressed'
    speed_topic = '/manual_control/speed'
    steering_topic = '/manual_control/steering'
    topic_list = [image_topic, speed_topic, steering_topic]
    num_msgs = bag.get_message_count(image_topic)

    print 'numero de mensages: %s' % (num_msgs)
    print 'Topicos:'
    print image_topic
    print speed_topic
    print steering_topic

    save_topics(bag=bag, num_msgs=num_msgs, topics=topic_list, bag_name=name_bag)
    bag.close()
