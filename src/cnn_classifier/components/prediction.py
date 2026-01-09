import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from pathlib import Path
import os
from cnn_classifier import logger


class Prediction:
    def __init__(self, config):
        self.config = config
        self.model = None
    
    def load_model(self):
        """Load the trained model"""
        try:
            self.model = load_model(self.config.model_path)
            logger.info(f"Model loaded successfully from {self.config.model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise e
    
    def preprocess_image(self, image_path):
        """Preprocess the input image for prediction"""
        try:
            # Load and resize image
            img = image.load_img(image_path, target_size=self.config.params_image_size[:2])
            
            # Convert to array and normalize
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0  # Normalize to [0,1]
            
            logger.info(f"Image preprocessed successfully: {image_path}")
            return img_array
            
        except Exception as e:
            logger.error(f"Error preprocessing image {image_path}: {e}")
            raise e
    
    def predict(self, image_path):
        """Make prediction on a single image"""
        try:
            # Load model if not already loaded
            if self.model is None:
                self.load_model()
            
            # Preprocess image
            processed_image = self.preprocess_image(image_path)
            
            # Make prediction
            prediction = self.model.predict(processed_image)
            predicted_class_idx = np.argmax(prediction, axis=1)[0]
            confidence = float(np.max(prediction))
            
            # Get class name
            predicted_class = self.config.class_names[predicted_class_idx]
            
            result = {
                "image_path": str(image_path),
                "predicted_class": predicted_class,
                "confidence": confidence,
                "all_predictions": {
                    self.config.class_names[i]: float(prediction[0][i]) 
                    for i in range(len(self.config.class_names))
                }
            }
            
            logger.info(f"Prediction completed: {predicted_class} with confidence {confidence:.4f}")
            return result
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise e
    
    def predict_batch(self, image_paths):
        """Make predictions on multiple images"""
        try:
            results = []
            for image_path in image_paths:
                result = self.predict(image_path)
                results.append(result)
            
            logger.info(f"Batch prediction completed for {len(image_paths)} images")
            return results
            
        except Exception as e:
            logger.error(f"Error during batch prediction: {e}")
            raise e