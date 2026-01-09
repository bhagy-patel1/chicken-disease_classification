import sys
from pathlib import Path

# Add project root to Python path for standalone execution
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

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

if __name__ == "__main__":
    try:
        logger.info(f">>>>>> Stage {stage_name} started <<<<<<")
        prepare_callbacks_pipeline = PrepareCallbacksPipeline()
        prepare_callbacks_pipeline.main()
        logger.info(f">>>>>> Stage {stage_name} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e