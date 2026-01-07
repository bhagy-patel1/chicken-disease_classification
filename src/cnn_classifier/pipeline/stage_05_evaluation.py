from cnn_classifier.components.evaluation import Evaluation
from cnn_classifier import logger
from pathlib import Path

stage_name = "Model Evaluation Stage"

class EvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        # Create evaluation config directly
        class EvaluationConfig:
            def __init__(self):
                self.path_of_model = Path("artifacts/training/trained_model.h5")
                self.path_of_test_data = Path("artifacts/data_ingestion/chicken-diseases-image-dataset")
                self.params_image_size = [224, 224, 3]
                self.params_batch_size = 16
        
        evaluation_config = EvaluationConfig()
        evaluation = Evaluation(config=evaluation_config)
        evaluation.evaluation()
        evaluation.save_score()
        return evaluation.score