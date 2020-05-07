import os
import time
from random import shuffle

import numpy as np

from keys import Keys
from screen import record_screen
from settings import _HEIGHT, _WIDTH, _NP_DATA, _NP_DATA_NORM, _DATA_DIR


def main():
    # create directory
    if not os.path.exists(_DATA_DIR):
        os.makedirs(_DATA_DIR)

    print('Starting in...')
    for i in range(9)[::-1]:
        print(i + 1)
        time.sleep(1)

    keys = Keys()
    training_data = []
    for frame in record_screen(resize=(_HEIGHT, _WIDTH)):
        pressed_keys = keys.check()
        onehot = keys.keys_to_onehot(pressed_keys)
        training_data.append([frame, onehot])

        # save array every 1000 iterations
        if (len(training_data) % 1000) == 0:
            print('Saving array...')
            np.save(_NP_DATA, training_data)

        # pressing P will save array and normalize data
        if 'P' in pressed_keys:
            print('Saving array...')
            np.save(_NP_DATA, training_data)
            normalize()
            break


def normalize():
    train_data = np.load(_NP_DATA, allow_pickle=True)

    lefts = []
    rights = []
    forwards = []

    shuffle(train_data)

    for data in train_data:
        img = data[0]
        choice = data[1]

        if choice == [1, 0, 0]:
            lefts.append([img, choice])
        elif choice == [0, 1, 0]:
            forwards.append([img, choice])
        elif choice == [0, 0, 1]:
            rights.append([img, choice])
        else:
            print('no matches')

    forwards = forwards[:len(lefts)][:len(rights)]
    lefts = lefts[:len(forwards)]
    rights = rights[:len(forwards)]

    final_data = forwards + lefts + rights
    shuffle(final_data)
    print(len(final_data))
    np.save(_NP_DATA_NORM, final_data)


if __name__ == '__main__':
    main()
