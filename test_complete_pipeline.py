import sys
from pathlib import Path
import os
import shutil

# Add project src to PYTHONPATH
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

# Import directly from components
from cnn_classifier.components.prediction import Prediction
from cnn_classifier.entities.config_entity import PredictionConfig
from cnn_classifier import logger

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

def test_complete_pipeline():
    """Test the complete prediction pipeline"""
    print("🧪 Testing Complete Chicken Disease Classification Pipeline")
    print("=" * 60)
    
    try:
        # 1. Check if model exists
        model_path = Path("artifacts/training/trained_model.h5")
        if not model_path.exists():
            print("❌ Trained model not found!")
            print("Please run the training pipeline first: dvc repro")
            return False
        
        print("✅ Trained model found")
        
        # 2. Check if test data exists
        test_data_path = Path("artifacts/data_ingestion/chicken-diseases-image-dataset")
        if not test_data_path.exists():
            print("❌ Test data not found!")
            print("Please run the data ingestion stage first")
            return False
        
        print("✅ Test data found")
        
        # 3. Initialize prediction pipeline
        print("\n📋 Initializing prediction pipeline...")
        prediction_pipeline = PredictionPipeline()
        print("✅ Prediction pipeline initialized")
        
        # 4. Find test images
        print("\n🔍 Finding test images...")
        sample_images = []
        for root, dirs, files in os.walk(test_data_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    sample_images.append(Path(root) / file)
                    if len(sample_images) >= 5:  # Get first 5 images
                        break
            if len(sample_images) >= 5:
                break
        
        if not sample_images:
            print("❌ No test images found")
            return False
        
        print(f"✅ Found {len(sample_images)} test images")
        
        # 5. Test single prediction
        print("\n🔮 Testing single image prediction...")
        test_image = sample_images[0]
        print(f"Testing with: {test_image.name}")
        
        result = prediction_pipeline.predict(test_image)
        
        print(f"📊 Results:")
        print(f"   Predicted Class: {result['predicted_class']}")
        print(f"   Confidence: {result['confidence']:.4f}")
        print(f"   All Predictions:")
        for class_name, confidence in result['all_predictions'].items():
            print(f"     {class_name}: {confidence:.4f}")
        
        # 6. Test batch prediction
        print(f"\n📦 Testing batch prediction with {min(3, len(sample_images))} images...")
        batch_results = []
        for i, image_path in enumerate(sample_images[:3]):
            result = prediction_pipeline.predict(image_path)
            batch_results.append(result)
            print(f"   Image {i+1}: {Path(result['image_path']).name}")
            print(f"     Predicted: {result['predicted_class']} (Confidence: {result['confidence']:.4f})")
        
        # 7. Create a sample for web app testing
        print(f"\n📁 Creating sample images for web app testing...")
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(exist_ok=True)
        
        # Copy a few sample images to uploads directory for easy testing
        for i, image_path in enumerate(sample_images[:3]):
            dest_path = uploads_dir / f"sample_{i+1}_{image_path.name}"
            shutil.copy2(image_path, dest_path)
            print(f"   Copied: {dest_path}")
        
        print("\n🎉 Complete Pipeline Test Results:")
        print("=" * 40)
        print("✅ Model loading: SUCCESS")
        print("✅ Image preprocessing: SUCCESS")
        print("✅ Single prediction: SUCCESS")
        print("✅ Batch prediction: SUCCESS")
        print("✅ Sample images prepared: SUCCESS")
        
        print(f"\n📝 Summary:")
        print(f"   - Model: {model_path}")
        print(f"   - Test images: {len(sample_images)} found")
        print(f"   - Classes: {prediction_pipeline.prediction_config.class_names}")
        print(f"   - Image size: {prediction_pipeline.prediction_config.params_image_size}")
        
        print(f"\n🌐 Web App Testing:")
        print(f"   - Sample images copied to: {uploads_dir}")
        print(f"   - Run: python app.py")
        print(f"   - Open: http://localhost:8080")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_complete_pipeline()
    
    if success:
        print("\n🚀 Ready to deploy! All tests passed.")
        print("\nNext steps:")
        print("1. Run the web app: python app.py")
        print("2. Open browser: http://localhost:8080")
        print("3. Upload sample images from the 'uploads' folder")
    else:
        print("\n❌ Pipeline test failed. Please check the errors above.")