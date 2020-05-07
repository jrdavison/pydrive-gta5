_HEIGHT = 299
_WIDTH = 299

_V = 7
_DATA_DIR = 'data/'
_NP_DATA = '{}training_data_v{}.npy'.format(_DATA_DIR, _V)
_NP_DATA_NORM = '{}training_data_v{}_normal.npy'.format(_DATA_DIR, _V)

_EPOCHS = 10
_MODEL_NAME = 'pygta5-car-{}-{}-epochs.model'.format('inceptionV3', _EPOCHS)
