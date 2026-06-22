[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/OcE5Fe4c)
# assignment-05-CNN

## Exploring Hyperparameters
- 4 models have been trained with different image resolutions. If you want to rerun the files to create them, you need to either copy the gesture_dataset_sample folder we used in the exercise in the 01-hyperparameters folder or change the PATH variable at the end of the first code block in each file to the path where it is located on your file system
- explanations/plots are in hyperparameters.ipynb

## Gathering a Dataset
- images and annotations can be found in folder cato_images
- confusion matrix and code to generate it (gather_data.ipynb) directly in 02-dataset

## Gesture-based Media Controls
- first, the model was trained to recognize like, dislike and stop with `train_model.py` (to run this again, PATH needs to be adjusted or the gesture_dataset_sample folder added to this task's folder)
- `media_control.py` uses the trained model to recognize gestures shown to the camera and triggers the matching keyboard events
- use:

like: volume up

dislike: volume down

stop: start/stop media playback

