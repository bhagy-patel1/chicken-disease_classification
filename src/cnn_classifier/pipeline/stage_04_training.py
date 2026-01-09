import sys
from pathlib import Path

# Add project root to Python path for standalone execution
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from cnn_classifier.config.configuration import ConfigurationManager
from cnn_classifier.components.training import Training
from cnn_classifier.components.prepare_callbacks import PrepareCallbacksConfig
from cnn_classifier import logger

stage_name = "Training Stage"

class TrainingPipeline:
    def __init__(self):
        pass

    def main(self, callbacks=None):
        if callbacks is None:
            # Get callbacks if not provided
            config_manager = ConfigurationManager()
            prepare_callbacks_config = config_manager.get_prepare_callbacks_config()
            prepare_callbacks = PrepareCallbacksConfig(config=prepare_callbacks_config)
            callbacks = prepare_callbacks.get_callbacks()
        
        config_manager = ConfigurationManager()
        train_config = config_manager.get_train_config()
        training = Training(config=train_config)
        training.get_base_model()
        training.train_valid_generator()
        training.train(callbacks=callbacks)
        return train_config.trained_model_path

if __name__ == "__main__":
    try:
        logger.info(f">>>>>> Stage {stage_name} started <<<<<<")
        training_pipeline = TrainingPipeline()
        training_pipeline.main()
        logger.info(f">>>>>> Stage {stage_name} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e