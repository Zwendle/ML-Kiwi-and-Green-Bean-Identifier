#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 03:34:50 2024

@author: zacharywen
"""

# import necessary libraries

import gc

from keras.src.legacy.preprocessing.image import ImageDataGenerator

from keras.models import Sequential
from keras.layers import Conv2D, Activation, MaxPooling2D, Flatten, Dense, Dropout
import tensorflow as tf
from keras import backend as K

IMG_WIDTH, IMG_HEIGHT = 150, 150
TRAIN_DATA_DIR = 'train'
VALIDATION_DATA_DIR = 'validation'
NB_TRAIN_SAMPLES = 20
NB_VALIDATION_SAMPLE = 20
EPOCHS = 50
BATCH_SIZE = 5

def build_model():
    if K.image_data_format() == 'channels_first':
        input_shape = (3, IMG_WIDTH, IMG_HEIGHT)
    else:
        input_shape = (IMG_WIDTH, IMG_HEIGHT, 3)
        
    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    
    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    
    return model


def train_model(model):
    # this is the augmentation configuration we will use for training
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)
    
    # this is the augmentation configuration we will use for testing:
    # only rescaling
    test_datagen = ImageDataGenerator(rescale=1.0/255)
    
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DATA_DIR,
        target_size=(IMG_WIDTH, IMG_HEIGHT),
        batch_size=BATCH_SIZE,
        class_mode='binary')
    
    validation_generator = test_datagen.flow_from_directory(
        VALIDATION_DATA_DIR,
        target_size=(IMG_WIDTH, IMG_HEIGHT),
        batch_size=BATCH_SIZE,
        class_mode='binary')
    
    model.fit(
        train_generator,
        steps_per_epoch=NB_VALIDATION_SAMPLE // BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=validation_generator)
    
    return model

def save_model(model):
    model.save('saved_model.h5')




def main():
    myModel = None
    tf.keras.backend.clear_session() # for ensuring everything is loaded and saved cleanly
    gc.collect() # garbage collection
    myModel = build_model()
    myModel = train_model(myModel)
    save_model(myModel)

main()