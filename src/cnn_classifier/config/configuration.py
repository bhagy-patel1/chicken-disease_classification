from pathlib import Path
from ..contants import *
from ..utils.common import read_yaml, create_directories
from ..entities.config_entity import DataIngestionConfig, PrepareBaseModelConfig, preparecallbacksconfig
import os

class ConfigurationManager:
    def __init__(self,
                 config_filepath=CONFIG_FILE_PATH,
                 params_filepath=PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        data_ingestion_config = self.config.data_ingestion

        data_ingestion_config = DataIngestionConfig(
            root_dir=Path(data_ingestion_config.root_dir),
            source_URL=data_ingestion_config.source_URL,
            local_data_file=Path(data_ingestion_config.local_data_file),
            unzipped_data_dir=Path(data_ingestion_config.unzipped_data_dir)
        )

        return data_ingestion_config
    


    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        config = self.config['prepare_base_model']
        params = self.params
        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(config['root_dir']),
            base_model_path=Path(config['base_model_path']),
            updated_base_model_path=Path(config['updated_base_model_path']),
            params_image_size=params.IMAGE_SIZE,
            params_learning_rate=params.LEARNING_RATE,
            params_include_top=params.INCLUDE_TOP,
            params_weights=params.WEIGHTS,
            params_classes=params.CLASSES
        )
        create_directories([prepare_base_model_config.root_dir])
        return prepare_base_model_config
    def get_prepare_callbacks_config(self) -> preparecallbacksconfig:
        prepare_callbacks_config = self.config.prepare_callbacks
        artifacts_root = self.config.artifacts_root

        root_dir = os.path.join(artifacts_root, prepare_callbacks_config.root_dir)
        tensorboard_log_dir = os.path.join(artifacts_root, prepare_callbacks_config.tensorboard_log_dir)
        checkpoint_model_filepath = os.path.join(artifacts_root, prepare_callbacks_config.checkpoint_model_filepath)

        create_directories([root_dir, tensorboard_log_dir, os.path.dirname(checkpoint_model_filepath)])

        prepare_callbacks_config = preparecallbacksconfig(
            root_dir=root_dir,
            tensorboard_log_dir=tensorboard_log_dir,
            checkpoint_model_filepath=checkpoint_model_filepath
        )

        return prepare_callbacks_config