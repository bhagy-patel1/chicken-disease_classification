# ...existing code...
import sys
from pathlib import Path

# add project src to PYTHONPATH so "cnn_classifier" can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from cnn_classifier import logger
from cnn_classifier.pipeline.stage_01_data_ingestion import DataIngestionPipeline

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
