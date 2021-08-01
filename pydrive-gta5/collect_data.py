import os
import time
from random import shuffle

import numpy as np

from keys import Keys
from screen import record_screen
from settings import _HEIGHT, _WIDTH


def countdown(msg, seconds):
    print(msg)
    for i in range(seconds - 1)[::-1]:
        print(i + 1)
        time.sleep(1)


def main():
    # create training data specific dir
    milliseconds = int(round(time.time() * 1000))
    full_path = f"data/{milliseconds}"
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    countdown("Starting in...", 5)

    keys = Keys()
    training_data = []
    file_num = 1
    for frame in record_screen(resize=(_WIDTH, _HEIGHT)):
        pressed_keys = keys.check()
        onehot = keys.keys_to_onehot(pressed_keys)
        training_data.append([frame, onehot])

        # save new array every 500 iterations
        if (len(training_data) == 500):
            save_path = f"{full_path}/training_data{file_num}.npy"
            print("Saving {}...".format(save_path))
            np.save(save_path, training_data)
            training_data = []
            file_num += 1

        # pressing Q will end the capture
        if "Q" in pressed_keys:
            break


if __name__ == "__main__":
    main()
