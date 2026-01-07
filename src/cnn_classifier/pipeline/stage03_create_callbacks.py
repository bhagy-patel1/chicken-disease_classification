from cnn_classifier.config.configuration import ConfigurationManager
from cnn_classifier.components.prepare_callbacks import PrepareCallbacksConfig
from cnn_classifier import logger

stage_name = "Prepare Callbacks Stage"

class PrepareCallbacksPipeline:
    def __init__(self):
        pass

    def main(self):
        config_manager = ConfigurationManager()
        prepare_callbacks_config = config_manager.get_prepare_callbacks_config()
        prepare_callbacks = PrepareCallbacksConfig(config=prepare_callbacks_config)
        callbacks = prepare_callbacks.get_callbacks()
        return callbacks