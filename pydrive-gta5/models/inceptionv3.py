import keras
from tensorflow.keras import Model
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.losses import categorical_crossentropy
from tensorflow.keras.layers import GlobalAveragePooling2D, Dropout, Dense


class ModifiedInception:

    def __init__(self, height=227, width=227, channels=3, n_classes=10, keep_prob=0.5, load=False, model_path=""):
        if load:
            self.model = load_model(model_path)
        else:
            base_model = InceptionV3(weights="imagenet", include_top=False, input_shape=(height, width, channels))
            x = base_model.output
            x = GlobalAveragePooling2D(name="avg_pool")(x)
            x = Dropout(keep_prob)(x)
            predictions = Dense(n_classes, activation="softmax")(x)
            self.model = Model(inputs=base_model.input, outputs=predictions)
            self.model.compile(loss=categorical_crossentropy, optimizer="adam", metrics=["accuracy"])

    def train(self, X, Y, batch_size=16, epochs=10, validation_split=0.1, log_dir="logs"):
        tensorboard = TensorBoard(log_dir=log_dir)
        print("================")
        print("tensorboard cmd:")
        print("tensorboard --logdir={}".format(log_dir))
        print("================")

        filepath="model-checkpoint-{epoch:02d}-{loss:.4f}.h5"
        checkpoint = ModelCheckpoint(filepath, monitor="loss", verbose=1, save_best_only=True, mode="min")
        cb_list = [tensorboard, checkpoint]

        self.model.fit(X, Y, batch_size=batch_size, epochs=epochs, validation_split=validation_split, callbacks=cb_list)

    def predict(self, frame):
        return self.model.predict(frame)

    def save(self, model_path):
        self.model.save(model_path)

if __name__ == "__main__":
    model = ModifiedInception(270, 480, 3)
    model.summary()
    model.save("test_save_model.model")
