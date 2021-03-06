import os
import time

import numpy as np
from keras.models import load_model

from keys import Keys, execute_input
from screen import record_screen
from settings import _MODEL_NAME, _HEIGHT, _WIDTH


turn_thresh = 0.80
fwd_thresh = 0.70
debug = True

def predict():
    keys = Keys()
    model = load_model(_MODEL_NAME)
    paused = False
    for frame in record_screen(resize=(_HEIGHT, _WIDTH)):
        if not paused:
            np_frame = np.array([frame])
            prediction = model.predict(np_frame)[0]

            if debug:
                print(prediction)

            move = [0, 1, 0]
            if prediction[1] > fwd_thresh:
                move = [0, 1, 0]
            elif prediction[0] > turn_thresh:
                move = [1, 0, 0]
            elif prediction[2] > turn_thresh:
                move = [0, 0, 1]

            execute_input(move)

        if "T" in keys.check():
            if paused:
                paused = False
                print("Resuming...")
                time.sleep(1)
            else:
                paused = True
                execute_input([0, 0, 0])
                print("Paused")
                time.sleep(1)
        elif "Q" in keys.check():
            execute_input([0, 0, 0])
            print("Exiting...")
            break



if __name__ == "__main__":
    predict()
