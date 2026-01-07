import tensorflow as tf
from pathlib import Path
import json

class Evaluation:
    def __init__(self, config):
        self.config = config
        
    def _valid_generator(self):
        datagenerator_kwargs = dict(
            rescale=1./255,
            validation_split=0.30
        )

        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear",
            class_mode="categorical"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.path_of_test_data,
            subset="validation",
            shuffle=False,
            **dataflow_kwargs
        )
        
    @staticmethod
    def load_model(path):
        return tf.keras.models.load_model(path)

    def evaluation(self):
        self.model = self.load_model(self.config.path_of_model)
        self._valid_generator()
        self.score = self.model.evaluate(self.valid_generator)
        return self.score
        
    def save_score(self):
        scores = {"loss": float(self.score[0]), "accuracy": float(self.score[1])}
        with open("scores.json", "w") as f:
            json.dump(scores, f, indent=4)
        print(f"Scores saved: {scores}")
