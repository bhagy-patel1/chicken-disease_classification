
import os
import urllib.request as request
from zipfile import ZipFile 
import tensorflow as tf
import time
from ..entities.config_entity import TrainConfig

class Training:
    def __init__(self, config: TrainConfig):
        self.config = config

    def get_base_model(self):
        self.model = tf.keras.models.load_model(self.config.updated_base_model_path)
        # Recreate and compile a fresh optimizer so optimizer variables match the model's trainable variables
        self.model.compile(optimizer=tf.keras.optimizers.Adam(),
                           loss='categorical_crossentropy',  # Changed from sparse_categorical_crossentropy
                           metrics=['accuracy'])
        print(self.model.summary())

    def train_valid_generator(self):
        datagen_kwargs = dict(rescale=1./255,
                              validation_split=0.20)
        dataflow_kwargs = dict(target_size=self.config.param_image_size[:2],
                               batch_size=self.config.param_batch_size,
                               class_mode='categorical')
        valid_datagen = tf.keras.preprocessing.image.ImageDataGenerator(**datagen_kwargs)
        self.valid_generator = valid_datagen.flow_from_directory(
            directory=self.config.trainng_data_path,
            subset="validation",
            shuffle=False,
            **dataflow_kwargs
        )
        if self.config.param_is_augmentation:
            train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                rotation_range=20,
                horizontal_flip=True,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.2,
                **datagen_kwargs,
            )
        else:
            train_datagen = valid_datagen

        self.train_generator = train_datagen.flow_from_directory(
            directory=self.config.trainng_data_path,
            subset="training",
            shuffle=True,
            **dataflow_kwargs,
        )

    def train(self, callbacks:list):
        self.model.fit(
            self.train_generator,
            epochs=self.config.param_epochs,
            validation_data=self.valid_generator,
            callbacks=callbacks
        )
        self.model.save(self.config.trained_model_path)
        print(f"Trained model saved at : {self.config.trained_model_path}")
