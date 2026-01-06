import os
import urllib.request as request
from zipfile import ZipFile 
import tensorflow as tf
from pathlib import Path
from ..entities.config_entity import PrepareBaseModelConfig

class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config

    def prepare_base_model(self):
        base_model = tf.keras.applications.vgg16.VGG16(
            input_shape=tuple(self.config.params_image_size),
            include_top=self.config.params_include_top,
            weights=self.config.params_weights
        )
        base_model.save(self.config.base_model_path)
        print(f"Base model saved at: {self.config.base_model_path}")
        base_model.summary()
        return base_model

    @staticmethod
    def get_updated_base_model(base_model_path: Path, config: PrepareBaseModelConfig) -> tf.keras.Model:
        base_model = tf.keras.models.load_model(base_model_path)
        # Freeze layers
        for layer in base_model.layers:
            layer.trainable = False
        # Add custom layers on top
        x = tf.keras.layers.Flatten()(base_model.output)
        x = tf.keras.layers.Dense(1024, activation='relu')(x)
        predictions = tf.keras.layers.Dense(config.params_classes, activation='softmax')(x)
        updated_model = tf.keras.Model(inputs=base_model.input, outputs=predictions)
        updated_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=config.params_learning_rate),
                              loss='sparse_categorical_crossentropy',
                              metrics=['accuracy'])
        updated_model.save(config.updated_base_model_path)
        print(f"Updated base model saved at: {config.updated_base_model_path}")
        updated_model.summary()
        return updated_model
