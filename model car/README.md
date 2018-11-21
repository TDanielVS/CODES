# AutoNOMOSmini
Create a virtual environment, all instructions in "Conda Env" folder.

Record some data with rosbag record command http://wiki.ros.org/rosbag/Commandline

Clear your data using the scripts in the folder: "extractor de bolsas"

### Training
Use the code TrainRos.py to train the model whit the data set created before.

```
Python3 TrainRos.py
```


### Test
Use the code CNN_LAB.py.

```
Python3 CNN_LAB.py model.h5
```

You must be connected to the car by wireless in order to send commands to the car.
Before start receiving images from ROS topic, the model must load a test picture (like "outfile.jpg"), otherwise the steering prediction can't be published.
