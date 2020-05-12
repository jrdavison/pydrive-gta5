import os
import time
from random import shuffle

import numpy as np

from keys import Keys
from screen import record_screen
from settings import _HEIGHT, _WIDTH


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

        # save new array every 10,000 iterations
        if (len(training_data) % 10000) == 0:
            print("Saving array...")
            save_path = f"{full_path}/training_data{file_num}.npy"
            np.save(save_path, training_data)
            training_data = []
            file_num += 1
            countdown("Continuing in...", 5)

        # pressing Q will save array and normalize data
        if "Q" in pressed_keys:
            print("Saving array...")
            save_path = f"{full_path}/training_data{file_num}.npy"
            np.save(save_path, training_data)
            normalize(full_path)
            break


def countdown(msg, seconds):
    print(msg)
    for i in range(seconds - 1)[::-1]:
        print(i + 1)
        time.sleep(1)


def normalize(directory):
    all_data = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".npy"):
            temp_data = np.load(f"{directory}/{filename}", allow_pickle=True)
            lefts, rights, forwards = [], [], []
            shuffle(temp_data)
            for data in temp_data:
                img = data[0]
                move = data[1]
                if move == [1, 0, 0]:
                    lefts.append([img, move])
                elif move == [0, 1, 0]:
                    forwards.append([img, move])
                elif move == [0, 0, 1]:
                    rights.append([img, move])
                else:
                    print("No matches")

            forwards = forwards[:len(lefts)][:len(rights)]
            lefts = lefts[:len(forwards)]
            rights = rights[:len(forwards)]

            final_data = forwards + lefts + rights
            shuffle(final_data)
            print(len(final_data))

            all_data += final_data

    if not os.path.exists("data/normalized"):
        os.makedirs("data/normalized")

    ver = len(os.listdir("data/normalized")) + 1
    np.save(f"data/normalized/training_data_normalized_v{ver}.npy", all_data)


if __name__ == "__main__":
    main()
