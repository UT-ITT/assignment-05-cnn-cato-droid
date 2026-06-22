[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/OcE5Fe4c)
# assignment-05-CNN

Sorry for this submission. Due to personal reasons I had less time than I liked for this assignment and ran out of time to go over things I wanted to revisit in the end. All tasks work somewhat, but I had no time to go over them again and they are all a bit wonky/some things don't quite work because I had no time to go over them again.

## Exploring Hyperparameters
- 4 models have been trained with different image resolutions. If you want to rerun the files to create them, you need to either copy the gesture_dataset_sample folder we used in the exercise in the 01-hyperparameters folder or change the PATH variable at the end of the first code block in each file to the path where it is located on your file system
- explanations/plots are in hyperparameters.ipynb

## Gathering a Dataset
- images and annotations can be found in folder cato_images
- confusion matrix and code to generate it (gather_data.ipynb) directly in 02-dataset
- Note: I know something is wrong with the confusion matrix, but I did not find out in time what it was

## Gesture-based Media Controls
- first, the model was trained to recognize like, dislike and stop with `train_model.py` (to run this again, PATH needs to be adjusted or the gesture_dataset_sample folder added to this task's folder)
- `media_control.py` uses the trained model to recognize gestures shown to the camera and triggers the matching keyboard events
- use:

like: volume up

dislike: volume down

stop: start/stop media playback

- you can see your camera and feedback on the recognized gestures in the window.
- if you keep holding a gesture, it will only be recognized once. Remove your hand and then show the gesture again if you want to e.g. up your volume twice
- There also is a cooldown between gestures that can be adjusted at the top of the code, if you want to switch between gestures faster than once a second
- close the window to stop the program

