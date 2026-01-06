import os
import urllib.request as request
from zipfile import ZipFile 
import tensorflow as tf
import time
from cnn_classifier.contants import CONFIG_FILE_PATH
from cnn_classifier.utils.common import read_yaml
from cnn_classifier.utils.common import create_directories

class PrepareCallbacksConfig:
    def __init__(self, config:dict = read_yaml(CONFIG_FILE_PATH)):
        self.config = config
        self.prepare_callbacks_config = self.config['prepare_callbacks_config']
        create_directories([self.prepare_callbacks_config['callbacks_dir']])
        
    def create_time_stamped_dir(self):
        time_stamp = time.strftime("%Y%m%d-%H%M%S")
        tensorboard_log_dir = os.path.join(
            self.prepare_callbacks_config['tensorboard_log_dir'], time_stamp
        )
        return tensorboard_log_dir
    def create_checkpoint_filepath(self):
        checkpoint_model_filepath = os.path.join(
            self.prepare_callbacks_config['checkpoint_model_filepath'], 'cp-{epoch:04d}.ckpt'
        )
        return checkpoint_model_filepath
    def get_callbacks(self):
        tensorboard_log_dir = self.create_time_stamped_dir()
        checkpoint_model_filepath = self.create_checkpoint_filepath()

        tensorboard_callback = tf.keras.callbacks.TensorBoard(
            log_dir=tensorboard_log_dir
        )
        checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_model_filepath,
            save_weights_only=True,
            save_best_only=True,
            monitor='val_loss',
            verbose=1
        )
        return [tensorboard_callback, checkpoint_callback]