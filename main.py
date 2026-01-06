# ...existing code...
import sys
from pathlib import Path


# add project src to PYTHONPATH so "cnn_classifier" can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from cnn_classifier import logger
from cnn_classifier.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from cnn_classifier.config.configuration import ConfigurationManager
from cnn_classifier.pipeline.stage02_prepare_base_model import PrepareBaseModelPipeline

# ...existing code...

stage_name = "Data Ingestion Stage"
try:
    logger.info(f">>>>>> Stage {stage_name} started <<<<<<")
    data_ingestion_pipeline = DataIngestionPipeline()
    data_ingestion_pipeline.main()
    logger.info(f">>>>>> Stage {stage_name} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

stage_name = "Prepare Base Model Stage"
try:
    logger.info(f">>>>>> Stage {stage_name} started <<<<<<")
    prepare_base_model_pipeline = PrepareBaseModelPipeline()
    prepare_base_model_pipeline.main()
    logger.info(f">>>>>> Stage {stage_name} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e
