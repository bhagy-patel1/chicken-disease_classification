import sys
from pathlib import Path

# Add project src to PYTHONPATH so "cnn_classifier" can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

# Import directly from components instead of pipeline
from cnn_classifier.components.prediction import Prediction
from cnn_classifier.entities.config_entity import PredictionConfig
from cnn_classifier import logger
import os

class PredictionPipeline:
    def __init__(self):
        # Create prediction config directly
        self.prediction_config = PredictionConfig(
            model_path=Path("artifacts/training/trained_model.h5"),
            params_image_size=[224, 224, 3],
            class_names=["Coccidiosis", "Healthy"]
        )
        self.prediction = None

    def _get_prediction_component(self):
        """Get or create prediction component"""
        if self.prediction is None:
            self.prediction = Prediction(config=self.prediction_config)
        return self.prediction

    def predict(self, image_path):
        """Make prediction on a single image"""
        try:
            prediction = self._get_prediction_component()
            result = prediction.predict(image_path)
            return result
        except Exception as e:
            logger.exception(e)
            raise e
    
    def predict_batch(self, image_paths):
        """Make predictions on multiple images"""
        try:
            prediction = self._get_prediction_component()
            results = prediction.predict_batch(image_paths)
            return results
        except Exception as e:
            logger.exception(e)
            raise e

def main():
    """Demo script for prediction pipeline"""
    try:
        # Initialize prediction pipeline
        prediction_pipeline = PredictionPipeline()
        
        # Example: Find some test images from the dataset
        test_data_path = Path("artifacts/data_ingestion/chicken-diseases-image-dataset")
        
        if test_data_path.exists():
            # Look for sample images in the dataset
            sample_images = []
            for root, dirs, files in os.walk(test_data_path):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        sample_images.append(Path(root) / file)
                        if len(sample_images) >= 3:  # Get first 3 images
                            break
                if len(sample_images) >= 3:
                    break
            
            if sample_images:
                print("=== Chicken Disease Classification Prediction Demo ===\n")
                
                # Single image prediction
                print("1. Single Image Prediction:")
                result = prediction_pipeline.predict(sample_images[0])
                print(f"Image: {result['image_path']}")
                print(f"Predicted Class: {result['predicted_class']}")
                print(f"Confidence: {result['confidence']:.4f}")
                print(f"All Predictions: {result['all_predictions']}")
                print()
                
                # Batch prediction
                if len(sample_images) > 1:
                    print("2. Batch Prediction:")
                    batch_results = prediction_pipeline.predict_batch(sample_images[:3])
                    for i, result in enumerate(batch_results, 1):
                        print(f"Image {i}: {Path(result['image_path']).name}")
                        print(f"  Predicted: {result['predicted_class']} (Confidence: {result['confidence']:.4f})")
                    print()
                
                print("=== Prediction Demo Completed Successfully ===")
            else:
                print("No sample images found in the dataset. Please ensure the data ingestion stage has been completed.")
        else:
            print("Dataset not found. Please run the DVC pipeline first:")
            print("dvc repro")
            
    except Exception as e:
        logger.exception(f"Error in prediction demo: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()