from pathlib import Path
from ..contants import *
from ..utils.common import read_yaml, create_directories
from ..entities.config_entity import DataIngestionConfig

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