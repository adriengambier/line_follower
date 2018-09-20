from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Activation
from keras.optimizers import SGD
from keras.optimizers import Adam
from keras.layers import Dense
from keras.layers import Conv2D
from keras.layers import Input
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.utils import np_utils
from imutils import paths
import numpy as np
import argparse
import cv2
import os
import json
from pathlib import Path
import util
from keras.callbacks import History 

def training(model_name, dataset, learning_rate, num_epochs):
	features = [] #Images
	data = [] #Coordinates
	history = History() 

	#Deleting already existing model
	if Path(model_name).is_file():
		print("[INFO] Deleting previous model...")
		os.remove(model_name)

	# Loading labels
	print("[INFO] Loading labels...")
	samples = json.load(open(dataset+'labels.json'))
	labels = list(samples.keys())

	# Storing dataset in variables
	print("[INFO] Storing data...")
	for (i, label) in enumerate(labels):
		image = cv2.imread(dataset + label)
		features.append(util.image_to_feature_vector(image))
		data.append(np.asarray(samples[label]).flatten()[0:4])
		if i > 0 and i % 1000 == 0:
			print("[INFO] processed {}/{}".format(i, len(labels)))

	(trainData, testData, trainLabels, testLabels) = train_test_split(features, data, test_size=0.25, random_state=42)

	# MODEL
	model = main_model()

	# TRAINING
	print("[INFO] compiling model...")
	#sgd = SGD(lr=learning_rate, momentum=0.9, nesterov=True)
	#adam = Adam(lr = learning_rate)
	model.compile(loss='mean_squared_error', optimizer='adam',metrics=["accuracy"])
	model.summary()
	model.fit(np.array(trainData), np.array(trainLabels), epochs=num_epochs, batch_size=4,verbose=1, callbacks=[history])

	# TESTING
	print("[INFO] evaluating on testing set...")
	(loss, accuracy) = model.evaluate(np.array(testData), np.array(testLabels),batch_size=128, verbose=1)
	print("[INFO] loss={:.4f}, accuracy: {:.4f}%".format(loss,accuracy * 100))

	# SAVING
	print("[INFO] dumping architecture and weights to file...")
	model.save(model_name)

	save_history(history)


def main_model():
	model = Sequential()
	model.add(Conv2D(20, (7,7), strides=(2,2), activation='relu', input_shape=(32,32,3)))
	model.add(MaxPooling2D(pool_size=(3,3), strides=2))
	model.add(Conv2D(20,(3,3),strides=(1,1),activation='relu'))
	model.add(MaxPooling2D(pool_size=(3,3),strides=2))
	model.add(Dense(32,activation='relu'))
	model.add(Dense(32,activation='relu'))
	model.add(Dense(4,activation='relu'))
	model.add(Flatten())
	return model

def save_history(history):
        f = open('results.txt', 'w')
        for i in range(len(history.history['acc'])):
                f.write(str(np.round(history.history['acc'][i],5)*100) + '\n')
        f.close()


if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-d", "--dataset", required=True,help="path to input dataset")
	ap.add_argument("-m", "--model", default = 'model.h5',help="path to output model file")
	args = ap.parse_args()

	training(model_name=args.model, dataset=args.dataset, learning_rate=0.0001, num_epochs = 100)





















