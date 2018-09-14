# AutoNOMOSmini
Create a virtual environment, all instructions in "Conda Env" folder.

Record some data with rosbag record command http://wiki.ros.org/rosbag/Commandline

Clear your data using the scripts in "extractor de bolsas" folder

### Training
Use the code TrainRos.py to train the model whit the data set created before.


### Test
Use the code CNN_LAB.py you must be connected to the car by wireless way in order to send the commands to the car.
Before start receiving images from ROS topic, the model must load a picture test, otherwise can't be published the steering prediction.
