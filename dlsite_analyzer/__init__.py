import os
import glob
from time import sleep
from pathlib import Path
from typing import Optional

from tqdm import tqdm

from .scraper import VoiceWorkScraper
from .config import DATABASE_PATH, RAW_JSON_DATA_DIR, ARCHIVE_DIR
from .database_initializer import DatabaseInitializer
from .database import (
    SQLiteHandler,
    VoiceWorksTableHandler,
    CirclesTableHandler,
    ProductFormatTableHandler,
    VoiceActorsTableHandler,
    AgeRatingTableHandler,
)
from .database.constants import (
    VOICE_WORKS_PRIMARY_KEY,
    VOICE_WORKS_TITLE,
    VOICE_WORKS_URL,
    VOICE_WORKS_PRODUCT_FORMAT_ID,
    VOICE_WORKS_CIRCLE_ID,
    VOICE_WORKS_VOICE_ACTOR_ID,
    VOICE_WORKS_PRICE,
    VOICE_WORKS_POINTS,
    VOICE_WORKS_SALES_COUNT,
    VOICE_WORKS_REVIEW_COUNT,
    VOICE_WORKS_AGE_ID,
    VOICE_WORKS_FULL_IMAGE_URL,
    CIRCLE_PRIMARY_KEY,
    CIRCLE_NAME,
    PRODUCT_FORMAT_NAME,
    VOICE_ACTOR_NAME,
    AGE_RATING_NAME,
)
from .utils import (
    Logger,
    load_json,
    save_json,
    archive_and_zip_files,
    cleanup
)

logger = Logger.get_logger(__name__)

def archive_and_cleanup():
    '''
    Archives the previously collected tweet JSON files and cleans up the directory.
    '''
    if RAW_JSON_DATA_DIR.exists():
        tweet_file_paths = sorted(glob.iglob(os.path.join(RAW_JSON_DATA_DIR, "*.json")))
        archive_and_zip_files(tweet_file_paths, output_dir=ARCHIVE_DIR)
        cleanup(RAW_JSON_DATA_DIR)

def fetch_and_save_voice_works(save_dir: Path, max_retries: int=3, retry_delay: float=2.0) -> Optional[None]:
    '''
    Fetch voice works data from a website and save each page as a JSON file.

    Parameters
    ----------
    save_dir : Path
        Directory where JSON files will be saved.
    max_retries : int
        Maximum number of retries for failed requests.
    retry_delay : float
        Time in seconds to wait before retrying a failed request.

    Returns
    -------
    Optional[None]
        Returns None if the process completes successfully.
    '''
    scraper = VoiceWorkScraper()
    
    # Fetch the first page and determine the total number of pages
    for attempt in range(max_retries):
        first_page_response = scraper.get_voice_works_response()
        if first_page_response.status_code == 200:
            break
        logger.error(f"Failed to fetch the first page. Retrying ({attempt + 1}/{max_retries})...")
        sleep(retry_delay)
    else:
        logger.error("Exceeded maximum retries for the first page.")
        return None

    total_pages = scraper.get_total_pages(first_page_response.text)
    logger.info(f"Total pages to process: {total_pages}")

    save_dir.mkdir(parents=True, exist_ok=True)

    # Process each page
    for page in tqdm(range(1, total_pages + 1), desc="Fetching pages"):
        for attempt in range(max_retries):
            response = scraper.get_voice_works_response(page)
            if response.status_code == 200:
                break
            logger.error(f"Failed to fetch page {page}. Retrying ({attempt + 1}/{max_retries})...")
            sleep(retry_delay)
        else:
            logger.error(f"Exceeded maximum retries for page {page}. Skipping this page.")
            continue

        voice_works = scraper.extract_voice_work_data(response.text)
        save_file_path = save_dir / f"voice_works_page_{page}.json"
        save_json(voice_works, save_file_path)
        # logger.info(f"Page {page} data saved successfully.")

    logger.info("All pages processed and saved as JSON files.")

def _insert_voice_work_data(db_connection: SQLiteHandler, work: dict) -> None:
    '''
    Insert a single voice work entry and its associated data into the database.

    Parameters
    ----------
    db_connection : SQLiteHandler
        Database connection handler.
    work : dict
        Voice work data to be inserted.
    '''
    try:
        age_rating_manager = AgeRatingTableHandler(db_connection)
        circles_manager = CirclesTableHandler(db_connection)
        product_format_manager = ProductFormatTableHandler(db_connection)
        voice_actors_manager = VoiceActorsTableHandler(db_connection)
        voice_works_manager = VoiceWorksTableHandler(db_connection)

        # Insert or retrieve maker
        circles_data = {CIRCLE_PRIMARY_KEY: work['maker_id'], CIRCLE_NAME: work['maker']}
        circles_manager.insert(circles_data)

        # Insert or retrieve product format
        category_data = {PRODUCT_FORMAT_NAME: work['category']}
        product_format_manager.insert(category_data)
        category_id = product_format_manager.get_product_format_id(category_data[PRODUCT_FORMAT_NAME])

        # Insert or retrieve author
        author_data = {VOICE_ACTOR_NAME: work['author']}
        author_id = voice_actors_manager.get_voice_actor_id(author_data[VOICE_ACTOR_NAME])
        if author_id is None and author_data[VOICE_ACTOR_NAME]:
            voice_actors_manager.insert(author_data)
            author_id = voice_actors_manager.get_voice_actor_id(author_data[VOICE_ACTOR_NAME])

        # Insert or retrieve age rating
        age_rating_data = {AGE_RATING_NAME: work['age_rating']}
        age_rating_id = age_rating_manager.get_age_rating_id(age_rating_data[AGE_RATING_NAME])
        if age_rating_id is None:
            age_rating_manager.insert(age_rating_data)
            age_rating_id = age_rating_manager.get_age_rating_id(age_rating_data[AGE_RATING_NAME])

        # Insert voice work
        voice_work_entry = {
            VOICE_WORKS_PRIMARY_KEY: work['product_id'],
            VOICE_WORKS_TITLE: work['title'],
            VOICE_WORKS_URL: work['url'],
            VOICE_WORKS_PRODUCT_FORMAT_ID: category_id,
            VOICE_WORKS_CIRCLE_ID: circles_data[CIRCLE_PRIMARY_KEY],
            VOICE_WORKS_VOICE_ACTOR_ID: author_id,
            VOICE_WORKS_PRICE: work['price'],
            VOICE_WORKS_POINTS: work['points'],
            VOICE_WORKS_SALES_COUNT: work['sales_count'],
            VOICE_WORKS_REVIEW_COUNT: work['review_count'],
            VOICE_WORKS_AGE_ID: age_rating_id,
            VOICE_WORKS_FULL_IMAGE_URL: work['full_image_url'],
        }
        voice_works_manager.insert(voice_work_entry)
    except Exception as e:
        logger.error(f"Failed to insert voice work data: {e}")

def import_voice_works_to_db(input_dir: Path) -> None:
    '''
    Import voice works data from saved JSON files into the database.

    Parameters
    ----------
    input_dir : Path
        Directory where JSON files are stored.
    '''
    json_paths = sorted(glob.glob(str(input_dir / "*.json")))
    try:
        with SQLiteHandler(DATABASE_PATH) as db_connection:
            for json_path in tqdm(json_paths, desc="Importing JSON to DB"):
                voice_works = load_json(json_path)
                for work in voice_works:
                    _insert_voice_work_data(db_connection, work)
    except Exception as e:
        logger.error(f"Failed to process {json_path}: {e}")

    logger.info("All JSON data imported to the database.")

__all__ = [
    'archive_and_cleanup',
    'DatabaseInitializer',
    'fetch_and_save_voice_works',
    'import_voice_works_to_db',
]