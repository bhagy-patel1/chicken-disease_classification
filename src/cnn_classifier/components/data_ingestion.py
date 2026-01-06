import os
import urllib.request as request
import zipfile
from .. import logger
from ..utils.common import get_size, create_directories
from ..entities.config_entity import DataIngestionConfig


class DataIngestion:
    def __init__(self,config:DataIngestionConfig):
        self.config = config

    def download_data(self):
        logger.info("Starting data download...")
        # Create the root directory if it doesn't exist
        create_directories([self.config.root_dir])
        
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url=self.config.source_URL,
                filename=self.config.local_data_file
            )
            logger.info(
                f"Data downloaded successfully! File location: {filename}, size: {get_size(filename)}"
            )
        else:
            logger.info("Data file already exists. Skipping download.")
            
    def extract_zip_file(self):
        logger.info("Starting data extraction...")
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(self.config.unzipped_data_dir)
        logger.info(f"Data extracted successfully at {self.config.unzipped_data_dir}")