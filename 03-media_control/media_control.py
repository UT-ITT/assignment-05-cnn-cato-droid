import keras.models
import cv2 
import numpy as np
import sys
import pyglet
import pynput
import time
from time import sleep
from pyglet import window
from PIL import Image
from pynput.keyboard import Key, Controller

#variables for smoother gesture recognition
last_gesture = None
last_trigger_time = 0
cooldown = 1

#control keyboard
keyboard = Controller()

#video source
video_id = 0

if len(sys.argv) > 1:
    video_id = int(sys.argv[1])

# Create a video capture object for the webcam
cap = cv2.VideoCapture(video_id)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

win = window.Window(width, height, caption="Camera Test")

# image size (needs to match the one in train_model.py)
IMG_SIZE = 32
SIZE = (IMG_SIZE, IMG_SIZE)

label_names = ['like', 'no_gesture', 'dislike', 'stop']


# converts OpenCV image to PIL image and then to pyglet texture
# https://gist.github.com/nkymut/1cb40ea6ae4de0cf9ded7332f1ca0d55
def cv2glet(img,fmt):
    '''Assumes image is in BGR color space. Returns a pyimg object'''
    if fmt == 'GRAY':
      rows, cols = img.shape
      channels = 1
    else:
      rows, cols, channels = img.shape

    raw_img = Image.fromarray(img).tobytes()

    top_to_bottom_flag = -1
    bytes_per_row = channels*cols
    pyimg = pyglet.image.ImageData(width=cols, 
                                   height=rows, 
                                   fmt=fmt, 
                                   data=raw_img, 
                                   pitch=top_to_bottom_flag*bytes_per_row)
    return pyimg


model = keras.models.load_model("gesture_recognition_like_dislike_stop.keras")
print("show hand gestures to the camera to control your media:")
print("thumb up for volume up\nthumb down for volume down\nflat hand to start/stop")
print("you can check your camera input in the window. Make sure the gesture is visible clearly in the middle of the camera. The video also gives you Feedback on the recognized gesture. If you have trouble with gesture recognition, try adding a background in a single color to your hand")
print("to stop this programm, jsut close the camera window")

@win.event
def on_draw():
    global label_names, SIZE, IMG_SIZE, cap, width, height, keyboard, last_gesture, last_trigger_time, cooldown

    # Capture a frame from the webcam
    ret, frame = cap.read()
    if ret:
        resized = cv2.resize(frame, SIZE)
        reshaped = resized.reshape(-1, IMG_SIZE, IMG_SIZE, 3)

        prediction = model.predict(reshaped)
        gesture = label_names[np.argmax(prediction)]
        
        #reset last_gesture when no gesture is shown
        if gesture == "no_gesture":
            last_gesture = "no_gesture"

        current_time = time.time()

        #wait after triggering the next gesture and have at least one gesture (including no gesture) in between recognizing the same one again
        if (gesture != "no_gesture" and
            gesture != last_gesture and
            current_time - last_trigger_time >= cooldown):
            last_gesture = gesture
            last_trigger_time = current_time
            if gesture == "like":
                print("vol up")
                keyboard.press(Key.media_volume_up)
                keyboard.release(Key.media_volume_up)
            elif gesture == "dislike":
                print("vol down")
                keyboard.press(Key.media_volume_up)
                keyboard.release(Key.media_volume_up)
            elif gesture == "stop":
                print("start/stop")
                keyboard.press(Key.media_play_pause)
                keyboard.release(Key.media_play_pause)

        #print(label_names[np.argmax(prediction)], np.max(prediction))

        #draw test window with recognized gesture
        win.clear()
        img = cv2glet(frame, 'BGR')
        img.blit(0, 0, 0)
        label = pyglet.text.Label(f"gesture: {label_names[np.argmax(prediction)]}",
                                font_size=36,
                                x=width/2,
                                y=height/2 + 50,
                                anchor_x = "center",
                                anchor_y = "center")
        label.draw()

pyglet.app.run()