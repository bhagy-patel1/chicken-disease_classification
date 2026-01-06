import os 
from box.exceptions import BoxValueError
from box import config_box
import yaml
from cnn_classifier import logger
import json
import joblib
from ensure import ensure_annotations
from pathlib import Path
from typing import Any
import base64

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> config_box.ConfigBox:
    """Reads a YAML file and returns its contents as a ConfigBox object.

    Args:
        path_to_yaml (Path): The path to the YAML file.
    Returns:
        ConfigBox: The contents of the YAML file as a ConfigBox object.
    """ 
    try:
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file: {path_to_yaml} loaded successfully")
            return config_box.ConfigBox(content)
    except BoxValueError as e:
        logger.error(f"Error converting YAML to ConfigBox: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error reading YAML file: {e}")
        raise e
@ensure_annotations
def write_yaml(path_to_yaml: Path, data: config_box.ConfigBox) -> None:
    """Writes a ConfigBox object to a YAML file.

    Args:
        path_to_yaml (Path): The path to the YAML file.
        data (ConfigBox): The ConfigBox object to write to the file.
    """
    try:
        with open(path_to_yaml, "w") as yaml_file:
            yaml.dump(data.to_dict(), yaml_file)
            logger.info(f"YAML file: {path_to_yaml} written successfully")
    except Exception as e:
        logger.error(f"Error writing YAML file: {e}")
        raise e
@ensure_annotations
def save_json(path: Path, data: Any) -> None:
    """Saves data to a JSON file.

    Args:
        path (Path): The path to the JSON file.
        data (Any): The data to save to the file.
    """
    try:
        with open(path, "w") as json_file:
            json.dump(data, json_file, indent=4)
            logger.info(f"JSON file: {path} saved successfully")
    except Exception as e:
        logger.error(f"Error saving JSON file: {e}")
        raise e
@ensure_annotations
def load_json(path: Path) -> Any:
    """Loads data from a JSON file.

    Args:
        path (Path): The path to the JSON file.
    Returns:
        Any: The data loaded from the file.
    """
    try:
        with open(path, "r") as json_file:
            data = json.load(json_file)
            logger.info(f"JSON file: {path} loaded successfully")
            return data
    except Exception as e:
        logger.error(f"Error loading JSON file: {e}")
        raise e
@ensure_annotations
def save_binary(path: Path, data: Any) -> None:
    """Saves data to a binary file using joblib.

    Args:
        path (Path): The path to the binary file.
        data (Any): The data to save to the file.
    """
    try:
        joblib.dump(data, path)
        logger.info(f"Binary file: {path} saved successfully")
    except Exception as e:
        logger.error(f"Error saving binary file: {e}")
        raise e
@ensure_annotations
def decode_base64_to_image(base64_string: str, output_path: Path) -> None:
    """Decodes a base64 string and saves it as an image file.

    Args:
        base64_string (str): The base64 encoded string.
        output_path (Path): The path to save the decoded image.
    """
    try:
        image_data = base64.b64decode(base64_string)
        with open(output_path, "wb") as image_file:
            image_file.write(image_data)
        logger.info(f"Image saved successfully at: {output_path}")
    except Exception as e:
        logger.error(f"Error decoding base64 string to image: {e}")
        raise e
@ensure_annotations
def incode_image_to_base64(image_path: Path) -> str:
    """Encodes an image file to a base64 string.

    Args:
        image_path (Path): The path to the image file.
    Returns:
        str: The base64 encoded string of the image.
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        logger.info(f"Image at {image_path} encoded to base64 successfully")
        return encoded_string
    except Exception as e:
        logger.error(f"Error encoding image to base64 string: {e}")
        raise e
@ensure_annotations
def load_binary(path: Path) -> Any:
    """Loads data from a binary file using joblib.

    Args:
        path (Path): The path to the binary file.
    Returns:

        Any: The data loaded from the file.
    """ 
    try:
        data = joblib.load(path)
        logger.info(f"Binary file: {path} loaded successfully")
        return data
    except Exception as e:
        logger.error(f"Error loading binary file: {e}")
        raise e
    

from typing import List, Union
def create_directories(path_to_directories: List[Union[str, Path]]) -> None:
    """Creates directories if they do not exist.

    Args:
        path_to_directories (List[Union[str, Path]]): A list of directory paths to create.
    """
    for path in path_to_directories:
        path = Path(path)  # Convert to Path object if it's a string
        try:
            os.makedirs(path, exist_ok=True)
            logger.info(f"Directory created successfully: {path}")
        except Exception as e:
            logger.error(f"Error creating directory {path}: {e}")
            raise e
        
@ensure_annotations
def get_size(path: Path) -> str:
    """Gets the size of a file in KB.

    Args:
        path (Path): The path to the file.
    Returns:
        str: The size of the file in KB.
    """
    size_in_kb = round(os.path.getsize(path) / 1024, 2)
    logger.info(f"Size of file {path} is {size_in_kb} KB")
    return f"{size_in_kb} KB"
    

