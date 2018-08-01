import csv  # files csv: tables
import numpy as np
import matplotlib.image as mpimg
from keras.models import Sequential, Model
from keras.layers import Flatten, Dense, Lambda, Cropping2D, AveragePooling2D, Dropout, MaxPooling2D
from keras.layers.convolutional import Convolution2D
from sklearn.model_selection import train_test_split
import sklearn
import time
import matplotlib.pyplot as plt
import random

