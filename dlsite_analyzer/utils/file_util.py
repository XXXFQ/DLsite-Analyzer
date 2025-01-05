import json
import random
import shutil
from datetime import datetime
from pathlib import Path
from time import sleep

from .logger import Logger

logger = Logger.get_logger(__name__)

def sleep_random(min_seconds: int, max_seconds: int) -> None:
    '''
    Pause execution for a random duration between min_seconds and max_seconds.

    Parameters
    ----------
    min_seconds : int
        Minimum duration in seconds.
    max_seconds : int
        Maximum duration in seconds.
    '''
    delay = random.uniform(min_seconds, max_seconds)
    sleep(delay)

def load_json(file_path: str, encoding: str='UTF-8') -> dict:
    '''
    Load JSON data from the specified file path.

    Parameters
    ----------
    file_path : str
        Path to the JSON file.
    encoding : str
        File encoding, default is 'UTF-8'.

    Returns
    -------
    dict
        The loaded JSON data.
    '''
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return json.load(file)
    except FileNotFoundError:
        logger.warning(f"File not found: {file_path}")
        return {}

def save_json(data: dict, file_path: str, indent: int=4, encoding: str='UTF-8', ensure_ascii: bool=True) -> None:
    '''
    Save data as a JSON file at the specified file path.

    Parameters
    ----------
    data : dict
        Data to be saved.
    file_path : str
        Path to save the JSON file.
    indent : int
        Indentation for the JSON file, default is 4.
    encoding : str
        File encoding, default is 'UTF-8'.
    ensure_ascii : bool
        If True, ensures ASCII characters only, default is True.
    '''
    with open(file_path, 'w', encoding=encoding) as file:
        json.dump(data, file, indent=indent, ensure_ascii=ensure_ascii)

def create_output_directory(output_dir_path: str) -> Path:
    '''
    Create an output directory if it does not exist.

    Parameters
    ----------
    output_dir_path : str
        Path to the output directory.

    Returns
    -------
    Path
        Path object of the created directory.
    '''
    output_dir = Path(output_dir_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def cleanup(directory_path: str) -> None:
    '''
    Delete the specified directory and recreate it.

    Parameters
    ----------
    directory_path : str
        Path to the directory to be cleaned up.
    '''
    directory = Path(directory_path)
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir(exist_ok=True)
    logger.info(f"Cleaned up and recreated directory: {directory_path}")

def archive_and_zip_files(files: list, output_dir: str) -> bool:
    '''
    Archive files into a ZIP file.

    Parameters
    ----------
    files : list
        List of file paths to be archived.
    output_dir : str
        Path to the directory to save the ZIP file.

    Returns
    -------
    bool
        True if archiving is successful, False otherwise.
    '''
    if not files:
        logger.warning("No files provided for archiving.")
        return False

    archive_path = Path(output_dir) / datetime.now().strftime("%Y-%m-%d-%H%M%S")
    archive_path.mkdir(parents=True, exist_ok=True)

    for file in files:
        shutil.move(file, archive_path)

    zip_path = shutil.make_archive(str(archive_path), 'zip', root_dir=archive_path)
    shutil.rmtree(archive_path)
    logger.info(f"Files archived and saved as ZIP: {zip_path}")
    return True
