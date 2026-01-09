import sys
from pathlib import Path
import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import uuid

# Add project src to PYTHONPATH so "cnn_classifier" can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

# Import directly from components instead of pipeline
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

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize prediction pipeline
prediction_pipeline = PredictionPipeline()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Please upload PNG, JPG, JPEG, or GIF files.'}), 400
        
        if file:
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Save file
            file.save(filepath)
            
            try:
                # Make prediction
                result = prediction_pipeline.predict(filepath)
                
                # Clean up uploaded file
                os.remove(filepath)
                
                return jsonify({
                    'success': True,
                    'predicted_class': result['predicted_class'],
                    'confidence': result['confidence'],
                    'all_predictions': result['all_predictions']
                })
                
            except Exception as e:
                # Clean up uploaded file in case of error
                if os.path.exists(filepath):
                    os.remove(filepath)
                logger.error(f"Prediction error: {e}")
                return jsonify({'error': f'Prediction failed: {str(e)}'}), 500
                
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Chicken Disease Classification API is running'})

if __name__ == '__main__':
    print("Starting Chicken Disease Classification Web App...")
    print("Upload an image to get predictions!")
    print("Access the app at: http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)