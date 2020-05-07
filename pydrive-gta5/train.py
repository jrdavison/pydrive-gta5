from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D, Input
from keras import backend as K
from keras.optimizers import SGD
import numpy as np

from settings import _EPOCHS, _HEIGHT, _WIDTH, _NP_DATA_NORM, _MODEL_NAME


train_data = list(np.load(_NP_DATA_NORM, allow_pickle=True))
for i in range(5, 6):
    train_data += list(np.load("data/training_data_v{}_normal.npy".format(i), allow_pickle=True))

X = np.array([i[0] for i in train_data])
Y = [i[1] for i in train_data]

# create the base pre-trained model
base_model = InceptionV3(weights='imagenet', include_top=False)

# global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
# fully-connected layer
x = Dense(1024, activation='relu')(x)
# logistic layer
predictions = Dense(3, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)
model.compile(optimizer=SGD(lr=0.0001, momentum=0.9),loss='categorical_crossentropy', metrics=['accuracy'])

model.fit([X], [Y], epochs=_EPOCHS, validation_split=0.1)
model.save(_MODEL_NAME)
