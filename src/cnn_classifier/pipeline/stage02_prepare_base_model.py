from cnn_classifier.config.configuration import ConfigurationManager
from cnn_classifier.components.prepare_base_model import PrepareBaseModel
from cnn_classifier import logger

stage_name = "Prepare Base Model Stage"

class PrepareBaseModelPipeline:
    def __init__(self):
        pass

    def main(self):
        config_manager = ConfigurationManager()
        prepare_base_model_config = config_manager.get_prepare_base_model_config()
        prepare_base_model = PrepareBaseModel(config=prepare_base_model_config)
        base_model = prepare_base_model.prepare_base_model()
        updated_base_model = PrepareBaseModel.get_updated_base_model(
            base_model_path=prepare_base_model_config.base_model_path,
            config=prepare_base_model_config
        )

if __name__ == "__main__":
    try:
        logger.info(f">>>>>> Stage {stage_name} started <<<<<<")
        prepare_base_model_pipeline = PrepareBaseModelPipeline()
        prepare_base_model_pipeline.main()
        logger.info(f">>>>>> Stage {stage_name} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
