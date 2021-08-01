import os

import numpy as np

from models.inceptionv3 import ModifiedInception
from settings import _HEIGHT, _WIDTH


CLASSES = 9
EPOCHS = 5


def main():
    model = ModifiedInception(_HEIGHT, _WIDTH, channels=3, n_classes=9)
    iteration = 1
    X, Y = [], []
    for subdir, _, files in os.walk("./data"):
        for file in files:
            full_path = os.path.join(subdir, file)
            print("loading: ", full_path)
            train_data = np.load(full_path, allow_pickle=True)

            np.random.shuffle(train_data)
            for x, y in train_data:
                X.append(x)
                Y.append(y)
            assert len(X) == len(Y)
            if len(X) >= 20000:
                X = np.array(X)
                Y = np.array(Y)
                model.train(X, Y, batch_size=16, epochs=EPOCHS, validation_split=0.08)
                #model.save("inceptionv3-iter{}.h5".format(iteration))
                X, Y = [], []
                iteration += 1

if __name__ == "__main__":
    main()
