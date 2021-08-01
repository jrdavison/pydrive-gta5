import os
import time

import numpy as np

from models.inceptionv3 import ModifiedInception
from keys import Keys, execute_input
from screen import record_screen
from settings import _HEIGHT, _WIDTH


debug = True

def predict():
    keys = Keys()
    model = ModifiedInception(load=True, model_path="pydrive-model-v1.h5")
    paused = False
    for frame in record_screen(resize=(_WIDTH, _HEIGHT)):
        if not paused:
            np_frame = np.array([frame])
            prediction = model.predict(np_frame)[0]
            if debug:
                print(prediction)

            confident = False
            for p in prediction:
                if p >= 0.1:
                    confident = True
                    break

            if confident:
                move_index = np.argmax(prediction)
                execute_input(move_index)
            else:
                execute_input()

        if "T" in keys.check():
            if paused:
                paused = False
                print("Resuming...")
                time.sleep(1)
            else:
                paused = True
                execute_input() # release all keys
                print("Paused")
                time.sleep(1)
        elif "Q" in keys.check():
            execute_input() # release all keys
            print("Exiting...")
            break



if __name__ == "__main__":
    predict()
