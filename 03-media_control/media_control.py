import keras.models
import cv2 
import numpy as np
import sys
import pyglet
import pynput
from time import sleep
from pyglet import window
from PIL import Image
from pynput.keyboard import Key, Controller

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
    global label_names, SIZE, IMG_SIZE, cap, width, height, keyboard

    # Capture a frame from the webcam
    ret, frame = cap.read()
    if ret:
        resized = cv2.resize(frame, SIZE)
        reshaped = resized.reshape(-1, IMG_SIZE, IMG_SIZE, 3)

        prediction = model.predict(reshaped)
        if label_names[np.argmax(prediction)] == "like":
            print("vol up")
            # keyboard.press(Key.media_volume_up)
            sleep(1)
            # keyboard.release(Key.media_volume_up)

        elif label_names[np.argmax(prediction)] == "dislike":
            print("vol down")
            # keyboard.press(Key.media_volume_up)
            sleep(1)
            # keyboard.release(Key.media_volume_up)
        elif label_names[np.argmax(prediction)] == "stop":
            print("start/stop")
            #keyboard.press(Key.media_play_pause)
            sleep(1)
            #keyboard.release(Key.media_play_pause)

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