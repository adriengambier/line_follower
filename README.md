## Getting Started

The goal for this part of the project is to detect the line in the middle of the road and use it to move the car (Here, we use the 4Tronix Initio with a raspberry on top). I implemented the neural network used in the ENSTA [Project](https://becominghuman.ai/autonomous-racing-robot-with-an-arduino-a-raspberry-pi-and-a-pi-camera-3e72819e1e63) in Keras for the line detection. I then used the angle and the position of this line to decide whether or not the car should turn.

### Prerequisites


All the libraries of this project can be pip installed, Keras can be installed easily on Raspberry [here](https://medium.com/@abhizcc/installing-latest-tensor-flow-and-keras-on-raspberry-pi-aac7dbf95f2)

## Create and use a dataset

### Record dataset

To record the dataset, use this script and drive the car along the tracks

```
python record_dataset.py -f folderForRecordedVideo/
```

Then, convert the video to .mp4

```
MP4Box -add raw_video mp4_video
```

Convert video to images

```
python create_dataset.py -v mp4_video -o output_folder/
```

### Data augmentation

The dataset can be reversed or concatenate with another one 

```
python reverse_dataset.py -i input_folder/ -o output_folder/
```

```
python concatenate_dataset.py  -i input_folder/ -a additionnal_folder/ -o output_folder/
```

### Label images

Images are labeled manually by placing 2 points on the white line

```
python label.py  -f input_folder/
```

### Train the neural network

To train the neural network, use the following command

```
python NN.py -f path_to_dataset/
```

### Test the neural network

The model can then be tested on a specified dataset

```
python test_nn.py -f path_to_dataset/
```

## Drive the car

The prediction of the neural network is used to compute the orientation of the car from the detected line and turns accordingly.

```
python drive.py
```

## Acknowledgments

* Thanks to Antonin RAFFIN for his work on line [detection](https://becominghuman.ai/autonomous-racing-robot-with-an-arduino-a-raspberry-pi-and-a-pi-camera-3e72819e1e63), the idea of the architecture for the neural network comes from this project.



