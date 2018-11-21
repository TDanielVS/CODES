# SIMULATOR
Implement a simulator tool to train a convolutional neural network, then apply transfer learning in order to control AutoNOMOSmini platform. Download Windows or Linux executable version from the simulator in “Executables” folder, then collect your own dataset preferably in Windows version.

Go to “model car” folder and follow the instructions to create a virtual environment with Conda. After activate the virtual environment proceed to train or run.

## Training
You can train your neural network simply by using “TrainSim.py”. Modify the code to add your collected dataset path or the model itself.

Run the python code in your virtual environment:
```
Python3 TrainSim.py
```

## Running
model.h5 is the model saved from the training step

Run the python code in your virtual environment:
```
Python3 driveCIC.py model.h5
```
Socket will wait for exe version of the simulator runs, then you can use autonomous mode to test your model.


The model trained with “TrainSim.py” or “Transfer.py” can be used in the “model car” section from this repository to control AutoNOMOSmini platform.
