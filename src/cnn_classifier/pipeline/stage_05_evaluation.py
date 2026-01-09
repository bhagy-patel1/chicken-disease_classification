import sys
from pathlib import Path

# Add project root to Python path for standalone execution
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from cnn_classifier.components.evaluation import Evaluation
from cnn_classifier import logger

stage_name = "Model Evaluation Stage"

class EvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        # Create evaluation config directly
        class EvaluationConfig:
            def __init__(self):
                self.path_of_model = Path("artifacts/training/trained_model.h5")
                self.path_of_test_data = Path("artifacts/data_ingestion/chicken-diseases-image-dataset/Chicken-fecal-images")
                self.params_image_size = [224, 224, 3]
                self.params_batch_size = 16
        
        evaluation_config = EvaluationConfig()
        evaluation = Evaluation(config=evaluation_config)
        evaluation.evaluation()
        evaluation.save_score()
        return evaluation.score

if __name__ == "__main__":
    try:
        logger.info(f">>>>>> Stage {stage_name} started <<<<<<")
        evaluation_pipeline = EvaluationPipeline()
        evaluation_pipeline.main()
        logger.info(f">>>>>> Stage {stage_name} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e