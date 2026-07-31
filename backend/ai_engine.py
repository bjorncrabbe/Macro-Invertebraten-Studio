import os

os.environ["TF_USE_LEGACY_KERAS"] = "1"

import cv2
import numpy as np
import tensorflow as tf

from config import *
from collections import deque
tf.config.set_visible_devices([], "GPU")


class AIEngine:

    def __init__(self):

        self.model = None
        self.labels = []
        self.loaded = False
        self.history = deque(maxlen=5)
        self.load()

    def load(self):

        try:

            self.model = tf.keras.models.load_model(
                MODEL_PATH,
                compile=False,
                safe_mode=False
            )


        except Exception as err:

            print(f"TensorFlow load mislukt: {err}")

            try:

                import tf_keras

                self.model = tf_keras.models.load_model(
                    MODEL_PATH,
                    compile=False
                )

            except Exception as e:

                print(e)
                return

        # Controleer of labels.txt bestaat
        if not os.path.exists(LABELS_PATH):
            raise FileNotFoundError(
                f"Labelsbestand niet gevonden: {LABELS_PATH}"
            )

        self.labels = []

        with open(LABELS_PATH, "r", encoding="utf8") as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                if " " in line:
                    line = line.split(" ", 1)[1]

                self.labels.append(line)

        self.loaded = True

        print("AI Engine gestart.")

    def preprocess(self, frame):

        img = cv2.resize(
            frame,
            (AI_INPUT_SIZE, AI_INPUT_SIZE)
        )

        img = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2RGB
        )

        img = img.astype(np.float32)

        img = (img / 127.5) - 1

        img = np.expand_dims(img, axis=0)

        return img

    def predict(self, frame):

        if not self.loaded:
            return None, 0

        image = self.preprocess(frame)

        prediction = self.model.predict(
            image,
            verbose=0
        )[0]

        index = np.argmax(prediction)

        confidence = round(float(prediction[index]) * 100, 1)

        if index >= len(self.labels):
            return "Onbekend", confidence

        label = self.labels[index]

        return label, confidence

    def predict_stable(self, frame):

        label, confidence = self.predict(frame)

        if label is None:
            return None, 0.0

        self.history.append((label, confidence))

        labels = [item[0] for item in self.history]

        winner = max(
            set(labels),
            key=labels.count
        )

        values = [
            c
            for l, c in self.history
            if l == winner
        ]

        average = sum(values) / len(values)

        return winner, average

    def get_labels(self):
        """Geeft alle AI-labels terug."""
        return set(self.labels)