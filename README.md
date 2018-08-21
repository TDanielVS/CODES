# CODES

This repository has all source codes of the autonomous navigation from a scale vehicle using deep neural networks. There are three phases in this work, learn how to do it using Udacity Software, next applying the techniques learned to control a scale 1:10 vehicle, finally whit or own tool we speeding up the process trough transfer learning technique.

#### UDACITY software
Replicate the Behavioral Cloning Project, all description is on https://github.com/udacity/CarND-Behavioral-Cloning-P3.

First configure a virtual environment using Conda https://github.com/udacity/CarND-Term1-Starter-Kit/blob/master/doc/configure_via_anaconda.md

Download the simulator. I recommend record the training data set in windows version, it runs faster and have better response using controls or steering wheel. Use linux version to test trained networks. https://www.dropbox.com/sh/64lxq4heqnvsasm/AAC3Oz9mM35y8dXKMIa7ncFea?dl=0.

All source codes in "cloning vehaviour" folder

### ROS Indigo AutoNOMOSmini platform
We have tested in the model car v1, all documentation is on the official web page https://github.com/AutoModelCar/AutoModelCarWiki/wiki

Install ROS indigo or newer version on your computer http://wiki.ros.org/indigo/Installation/Ubuntu

All source codes in "model car" folder

### Transfer learning 

It is a tool based on the Behavioral Cloning Project. Helps you to improve your trainings and saves a lot of time whenever you collect a data set. 

You can choose between two different tracks on a realistic environment, based on IPN Robotics lab. An interactive dynamic light interface and more.

Compatibility with X-box 360 controllers.

Total compatibility with AutoNOMOSmini platform, especially after applying transfer learning technique.

All source codes in "transfear_learning" folder
