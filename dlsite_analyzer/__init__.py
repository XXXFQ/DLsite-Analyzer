import os
import glob

from tqdm import tqdm

from .scraper import VoiceWorkScraper
from .config import DATABASE_PATH
from .text_analyzer import (
    extract_words,
    generate_wordcloud,
    plot_wordcloud
)
from .database import (
    DatabaseManager,
    VoiceWorksViewManager,
    VoiceWorksTableManager,
    MakersTableManager,
    CategoriesTableManager,
    AuthorsTableManager,
    AgeRatingTableManager
)
from .database.constants import (
    VOICE_WORKS_PRODUCT_ID,
    VOICE_WORKS_TITLE,
    VOICE_WORKS_URL,
    VOICE_WORKS_CATEGORY_ID,
    VOICE_WORKS_MAKER_ID,
    VOICE_WORKS_AUTHOR_ID,
    VOICE_WORKS_PRICE,
    VOICE_WORKS_POINTS,
    VOICE_WORKS_SALES_COUNT,
    VOICE_WORKS_REVIEW_COUNT,
    VOICE_WORKS_AGE_RATING_ID,
    VOICE_WORKS_FULL_IMAGE_URL,
    MAKER_ID,
    MAKER_NAME,
    CATEGORY_NAME,
    AUTHOR_NAME,
    AGE_RATING_NAME
)
from .utils import (
    Logger,
    load_json,
    save_json,
    sleep_random
)

logger = Logger.getLogger(__name__)

def initialize_database():
    '''
    データベースを初期化し、必要なテーブルを作成する
    '''
    with DatabaseManager(DATABASE_PATH) as db_manager:
        voice_works_manager = VoiceWorksTableManager(db_manager)
        makers_manager = MakersTableManager(db_manager)
        categories_manager = CategoriesTableManager(db_manager)
        authors_manager = AuthorsTableManager(db_manager)
        age_rating_manager = AgeRatingTableManager(db_manager)
        voice_works_view = VoiceWorksViewManager(db_manager)
        voice_works_manager.create_table()
        makers_manager.create_table()
        categories_manager.create_table()
        authors_manager.create_table()
        age_rating_manager.create_table()
        voice_works_view.create_view()
    
    logger.info("Database initialized successfully.")

def fetch_and_save_voice_works(save_dir: str):
    '''
    ボイス作品を取得し、各ページのデータをJSONファイルに保存する
    
    Parameters
    ----------
    save_dir : str
        JSONファイルを保存するディレクトリのパス
    '''
    scraper = VoiceWorkScraper()
    
    first_page_response = scraper.get_voice_works_page()
    if first_page_response.status_code != 200:
        logger.error("Failed to fetch the first page.")
        return None

    total_pages = scraper.get_total_pages(first_page_response.text)
    logger.info(f"Total pages to process: {total_pages}")
    
    for page in tqdm(range(1, total_pages + 1), desc="Fetching pages"):
        response = scraper.get_voice_works_page(page)

        if response.status_code == 200:
            voice_works = scraper.extract_voice_work_data(response.text)
            save_file_path = save_dir / f"voice_works_page_{page}.json"
            save_json(voice_works, save_file_path)
            logger.info(f"Page {page} data saved successfully.")
        else:
            logger.error(f"Failed to fetch page {page}: Status code {response.status_code}")
            break
        
        sleep_random(2, 4)
    
    logger.info("All pages processed and saved as JSON files.")

def import_voice_works_to_db(input_dir: str):
    '''
    保存されたJSONファイルからボイス作品のデータを読み込み、データベースに保存する
    
    Parameters
    ----------
    input_dir : str
        JSONファイルが保存されているディレクトリのパス
    '''
    json_paths = sorted(glob.iglob(os.path.join(input_dir, "*.json")))
    
    with DatabaseManager(DATABASE_PATH) as db_manager:
        voice_works_manager = VoiceWorksTableManager(db_manager)
        makers_manager = MakersTableManager(db_manager)
        categories_manager = CategoriesTableManager(db_manager)
        authors_manager = AuthorsTableManager(db_manager)
        age_rating_manager = AgeRatingTableManager(db_manager)
        
        # 作者なしのデータを挿入
        authors_manager.insert({AUTHOR_NAME: ''})
        
        for json_path in tqdm(json_paths, desc="Importing JSON to DB"):
            voice_works = load_json(json_path)
            
            for work in voice_works:
                # メーカーデータを挿入 
                maker_data = {
                    MAKER_ID: work['maker_id'],
                    MAKER_NAME: work['maker']
                }
                makers_manager.insert(maker_data)
                
                # カテゴリーデータを挿入
                category_data = {CATEGORY_NAME: work['category']}
                categories_manager.insert(category_data)
                category_id = categories_manager.get_category_id(category_data[CATEGORY_NAME])
                
                # 作者データを挿入
                author_data = {AUTHOR_NAME: work['author']}
                author_id = authors_manager.get_author_id(author_data[AUTHOR_NAME])
                if author_id is None and author_data[AUTHOR_NAME]:
                    authors_manager.insert(author_data)
                    author_id = authors_manager.get_author_id(author_data[AUTHOR_NAME])
                
                # 年齢レーティングデータを挿入
                age_rating_data = {AGE_RATING_NAME: work['age_rating']}
                age_rating_id = age_rating_manager.get_age_rating_id(age_rating_data[AGE_RATING_NAME])
                if age_rating_id is None:
                    age_rating_manager.insert(age_rating_data)
                    age_rating_id = age_rating_manager.get_age_rating_id(age_rating_data[AGE_RATING_NAME])
                
                # ボイス作品データを挿入
                voice_work_entry = {
                    VOICE_WORKS_PRODUCT_ID: work['product_id'],
                    VOICE_WORKS_TITLE: work['title'],
                    VOICE_WORKS_URL: work['url'],
                    VOICE_WORKS_CATEGORY_ID: category_id,
                    VOICE_WORKS_MAKER_ID: maker_data[MAKER_ID],
                    VOICE_WORKS_AUTHOR_ID: author_id,
                    VOICE_WORKS_PRICE: work['price'],
                    VOICE_WORKS_POINTS: work['points'],
                    VOICE_WORKS_SALES_COUNT: work['sales_count'],
                    VOICE_WORKS_REVIEW_COUNT: work['review_count'],
                    VOICE_WORKS_AGE_RATING_ID: age_rating_id,
                    VOICE_WORKS_FULL_IMAGE_URL: work['full_image_url']
                }
                voice_works_manager.insert(voice_work_entry)
              
        logger.info("All JSON data imported to the database.")

__all__ = [
    'initialize_database',
    'fetch_and_save_voice_works',
    'import_voice_works_to_db',
    'generate_wordcloud',
    'plot_wordcloud',
    'extract_words',
]