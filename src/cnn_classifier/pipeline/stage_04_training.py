from cnn_classifier.config.configuration import ConfigurationManager
from cnn_classifier.components.training import Training

stage_name = "Training Stage"

class TrainingPipeline:
    def __init__(self):
        pass

    def main(self, callbacks):
        config_manager = ConfigurationManager()
        train_config = config_manager.get_train_config()
        training = Training(config=train_config)
        training.get_base_model()
        training.train_valid_generator()
        training.train(callbacks=callbacks)
        return train_config.trained_model_path
    