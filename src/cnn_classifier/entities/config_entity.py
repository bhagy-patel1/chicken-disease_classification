from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzipped_data_dir: Path

@dataclass
class PrepareBaseModelConfig:
    root_dir: Path
    base_model_path: Path
    updated_base_model_path: Path
    params_image_size: list
    params_learning_rate: float
    params_include_top: bool
    params_weights: str
    params_classes: int

@dataclass
class preparecallbacksconfig:
    root_dir: Path
    tensorboard_log_dir: Path
    checkpoint_model_filepath: Path
@dataclass
class TrainConfig:
    root_dir: Path
    trained_model_path: Path
    updated_base_model_path: Path
    trainng_data_path: Path
    param_epochs: int
    param_batch_size: int
    param_image_size: list
    param_is_augmentation: bool

@dataclass
class EvaluationConfig:
    path_of_model: Path
    path_of_test_data: Path
    all_params: dict
    params_image_size: list
    params_batch_size: int

@dataclass
class PredictionConfig:
    model_path: Path
    params_image_size: list
    class_names: list


