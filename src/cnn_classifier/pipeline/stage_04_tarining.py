from cnn_classifier.config.configuration import ConfigurationManager
from cnn_classifier.components.training import TrainConfig

stage_name = "training data"

class trainingPipeline:
    def __init__(self):
        pass

    def main(self,callbacks):
        config_manager = ConfigurationManager()
        train_config = config_manager.get_train_config()
        trainning = TrainConfig(config=train_config,callbacks=callbacks)
        trained_model_path = trainning.train()
        return trained_model_path
    