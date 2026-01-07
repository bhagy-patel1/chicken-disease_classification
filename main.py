# ...existing code...
import sys
from pathlib import Path

# add project src to PYTHONPATH so "cnn_classifier" can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from cnn_classifier import logger
from cnn_classifier.config.configuration import ConfigurationManager
# ...existing code...

stage_name = "Data Ingestion Stage"
try:
    logger.info(f">>>>>> Stage {stage_name} started <<<<<<")
    from cnn_classifier.pipeline.stage_01_data_ingestion import DataIngestionPipeline
    data_ingestion_pipeline = DataIngestionPipeline()
    data_ingestion_pipeline.main()
    logger.info(f">>>>>> Stage {stage_name} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

stage_name = "Prepare Base Model Stage"
try:
    logger.info(f">>>>>> Stage {stage_name} started <<<<<<")
    from cnn_classifier.pipeline.stage02_prepare_base_model import PrepareBaseModelPipeline
    prepare_base_model_pipeline = PrepareBaseModelPipeline()
    prepare_base_model_pipeline.main()
    logger.info(f">>>>>> Stage {stage_name} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

stage_name = "Prepare Callbacks Stage"
try:
    logger.info(f">>>>>> Stage {stage_name} started <<<<<<")
    from cnn_classifier.pipeline.stage03_create_callbacks import PrepareCallbacksPipeline
    prepare_callbacks_pipeline = PrepareCallbacksPipeline()
    callbacks = prepare_callbacks_pipeline.main()
    logger.info(f">>>>>> Stage {stage_name} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

stage_name = "Training Stage"
try:
    logger.info(f">>>>>> Stage {stage_name} started <<<<<<")
    from cnn_classifier.pipeline.stage_04_training import TrainingPipeline
    training_pipeline = TrainingPipeline()
    trained_model_path = training_pipeline.main(callbacks=callbacks)
    logger.info(f">>>>>> Stage {stage_name} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

stage_name = "Model Evaluation Stage"
try:
    logger.info(f">>>>>> Stage {stage_name} started <<<<<<")
    from cnn_classifier.pipeline.stage_05_evaluation import EvaluationPipeline
    evaluation_pipeline = EvaluationPipeline()
    evaluation_scores = evaluation_pipeline.main()
    logger.info(f"Model Evaluation - Loss: {evaluation_scores[0]:.4f}, Accuracy: {evaluation_scores[1]:.4f}")
    logger.info(f">>>>>> Stage {stage_name} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e
# ...existing code...

