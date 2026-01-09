# DVC Pipeline Usage

This project uses DVC (Data Version Control) to manage the machine learning pipeline. The pipeline consists of 5 stages:

## Pipeline Stages

1. **data_ingestion** - Downloads and extracts the chicken disease dataset
2. **prepare_base_model** - Prepares the VGG16 base model and creates updated model
3. **prepare_callbacks** - Sets up TensorBoard and checkpoint callbacks
4. **training** - Trains the CNN model using the prepared data and model
5. **evaluation** - Evaluates the trained model and generates metrics

## DVC Commands

### Run the entire pipeline:
```bash
dvc repro
```

### Run a specific stage:
```bash
dvc repro data_ingestion
dvc repro prepare_base_model
dvc repro prepare_callbacks
dvc repro training
dvc repro evaluation
```

### Check pipeline status:
```bash
dvc status
```

### View pipeline DAG:
```bash
dvc dag
```

### Show metrics:
```bash
dvc metrics show
```

### Force re-run a stage (ignore cache):
```bash
dvc repro --force <stage_name>
```

## Pipeline Dependencies

- **data_ingestion**: No dependencies
- **prepare_base_model**: No dependencies  
- **prepare_callbacks**: No dependencies
- **training**: Depends on data_ingestion, prepare_base_model, prepare_callbacks
- **evaluation**: Depends on data_ingestion, training

## Outputs

- `artifacts/data_ingestion/chicken-diseases-image-dataset/` - Extracted dataset
- `artifacts/prepare_base_model/base_model.h5` - VGG16 base model
- `artifacts/prepare_base_model/updated_base_model.h5` - Modified model for training
- `artifacts/prepare_callbacks/` - Callback configurations
- `artifacts/training/trained_model.h5` - Final trained model
- `scores.json` - Evaluation metrics (loss and accuracy)

## Parameters

The pipeline uses parameters from `params.yaml`:
- `EPOCHS`: Number of training epochs
- `BATCH_SIZE`: Training batch size
- `AUGMENTATION`: Whether to use data augmentation
- `IMAGE_SIZE`: Input image dimensions

## Notes

- Each stage can be run independently as a Python script
- The pipeline automatically handles dependencies between stages
- Metrics are tracked in `scores.json` and not cached by DVC
- All artifacts are stored in the `artifacts/` directory