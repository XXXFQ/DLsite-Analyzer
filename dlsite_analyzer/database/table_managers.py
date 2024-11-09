import pandas as pd

from .database_manager import DatabaseManager
from .constants import (
    VOICE_WORKS_TABLE,
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
    VOICE_WORKS_AGE_RATING,
    VOICE_WORKS_FULL_IMAGE_URL,
    MAKERS_TABLE,
    MAKER_ID,
    MAKER_NAME,
    CATEGORY_TABLE,
    CATEGORY_ID,
    CATEGORY_NAME,
    AUTHORS_TABLE,
    AUTHOR_ID,
    AUTHOR_NAME
)

class VoiceWorksTableManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        
        # テーブル情報
        self.table_info  = {
            'name': VOICE_WORKS_TABLE,
            'columns': [
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
                VOICE_WORKS_AGE_RATING,
                VOICE_WORKS_FULL_IMAGE_URL,
            ]
        }
        
        # テーブルのカラム名とデータ型
        self.columns_with_types = {
            VOICE_WORKS_PRODUCT_ID: 'TEXT PRIMARY KEY',
            VOICE_WORKS_TITLE: 'TEXT NOT NULL',
            VOICE_WORKS_URL: 'TEXT NOT NULL',
            VOICE_WORKS_CATEGORY_ID: 'INTEGER',
            VOICE_WORKS_MAKER_ID: 'INTEGER',
            VOICE_WORKS_AUTHOR_ID: 'INTEGER',
            VOICE_WORKS_PRICE: 'INTEGER',
            VOICE_WORKS_POINTS: 'INTEGER',
            VOICE_WORKS_SALES_COUNT: 'INTEGER',
            VOICE_WORKS_REVIEW_COUNT: 'INTEGER',
            VOICE_WORKS_AGE_RATING: 'TEXT',
            VOICE_WORKS_FULL_IMAGE_URL: 'TEXT',
        }
        
        # 外部キー制約
        self.foreign_keys = [
            f"FOREIGN KEY ({VOICE_WORKS_CATEGORY_ID}) REFERENCES {CATEGORY_TABLE} ({VOICE_WORKS_CATEGORY_ID})",
            f"FOREIGN KEY ({VOICE_WORKS_MAKER_ID}) REFERENCES {MAKERS_TABLE} ({VOICE_WORKS_MAKER_ID})",
            f"FOREIGN KEY ({VOICE_WORKS_AUTHOR_ID}) REFERENCES {AUTHORS_TABLE} ({VOICE_WORKS_AUTHOR_ID})",
        ]
    
    def create_table(self):
        '''
        テーブルを作成する
        '''
        columns = ', '.join([f"{col} {data_type}" for col, data_type in self.columns_with_types.items()])
        query = f"CREATE TABLE IF NOT EXISTS {self.table_info['name']} ({columns})"
        self.db_manager.execute_query(query)
        self.db_manager.commit()
    
    def insert(self, voice_works: dict):
        '''
        ボイス作品情報を挿入する
        
        Parameters
        ----------
        voice_works : dict
            ボイス作品情報
        '''
        columns = ', '.join(voice_works.keys())
        placeholders = ', '.join(['?' for _ in voice_works.values()])
        query = f"REPLACE INTO {self.table_info['name']} ({columns}) VALUES ({placeholders})"
        self.db_manager.execute_query(query, tuple(voice_works.values()))
    
    def get_all_voice_works(self) -> pd.DataFrame:
        '''
        全てのボイス作品情報を取得する
        
        Returns
        -------
        pd.DataFrame
            ボイス作品情報のデータフレーム
        '''
        query = f"SELECT * FROM {self.table_info['name']}"
        res = self.db_manager.execute_query(query)
        return pd.DataFrame(res.fetchall(), columns=self.table_info['columns'])

class MakersTableManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        
        # テーブル情報
        self.table_info  = {
            'name': MAKERS_TABLE,
            'columns': [
                MAKER_ID,
                MAKER_NAME
            ]
        }
        
        # テーブルのカラム名とデータ型
        self.columns_with_types = {
            MAKER_ID: 'TEXT PRIMARY KEY',
            MAKER_NAME: 'TEXT UNIQUE NOT NULL'
        }

    def create_table(self):
        '''
        テーブルを作成する
        '''
        columns = ', '.join([f"{col} {data_type}" for col, data_type in self.columns_with_types.items()])
        query = f"CREATE TABLE IF NOT EXISTS {self.table_info['name']} ({columns})"
        self.db_manager.execute_query(query)
        self.db_manager.commit()
        
    def insert(self, makers: dict):
        '''
        メーカー情報を挿入する
        
        Parameters
        ----------
        makers : dict
            メーカー情報
        '''
        columns = ', '.join(makers.keys())
        placeholders = ', '.join(['?' for _ in makers.values()])
        query = f"INSERT OR IGNORE INTO {self.table_info['name']} ({columns}) VALUES ({placeholders})"
        self.db_manager.execute_query(query, tuple(makers.values()))

class CategoriesTableManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        
        # テーブル情報
        self.table_info  = {
            'name': CATEGORY_TABLE,
            'columns': [
                CATEGORY_ID,
                CATEGORY_NAME
            ]
        }
        
        # テーブルのカラム名とデータ型
        self.columns_with_types = {
            CATEGORY_ID: 'INTEGER PRIMARY KEY AUTOINCREMENT',
            CATEGORY_NAME: 'TEXT UNIQUE NOT NULL'
        }
    
    def create_table(self):
        '''
        テーブルを作成する
        '''
        columns = ', '.join([f"{col} {data_type}" for col, data_type in self.columns_with_types.items()])
        query = f"CREATE TABLE IF NOT EXISTS {self.table_info['name']} ({columns})"
        self.db_manager.execute_query(query)
        self.db_manager.commit()
        
    def insert(self, categories: dict):
        '''
        カテゴリー情報を挿入する
        
        Parameters
        ----------
        categories : dict
            カテゴリー情報
        '''
        columns = ', '.join(categories.keys())
        placeholders = ', '.join(['?' for _ in categories.values()])
        query = f"INSERT OR IGNORE INTO {self.table_info['name']} ({columns}) VALUES ({placeholders})"
        self.db_manager.execute_query(query, tuple(categories.values()))
    
    def get_category_id(self, category_name: str) -> int:
        '''
        カテゴリー名からカテゴリーIDを取得する
        
        Parameters
        ----------
        category_name : str
            カテゴリー名
        
        Returns
        -------
        int
            カテゴリーID
        '''
        query = f"SELECT {CATEGORY_ID} FROM {self.table_info['name']} WHERE {CATEGORY_NAME} = ?"
        res = self.db_manager.execute_query(query, (category_name,))
        return res.fetchone()[0]

class AuthorsTableManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        
        # テーブル情報
        self.table_info  = {
            'name': AUTHORS_TABLE,
            'columns': [
                AUTHOR_ID,
                AUTHOR_NAME
            ]
        }
        
        # テーブルのカラム名とデータ型
        self.columns_with_types = {
            AUTHOR_ID: 'INTEGER PRIMARY KEY AUTOINCREMENT',
            AUTHOR_NAME: 'TEXT UNIQUE NOT NULL'
        }
    
    def create_table(self):
        '''
        テーブルを作成する
        '''
        columns = ', '.join([f"{col} {data_type}" for col, data_type in self.columns_with_types.items()])
        query = f"CREATE TABLE IF NOT EXISTS {self.table_info['name']} ({columns})"
        self.db_manager.execute_query(query)
        self.db_manager.commit()
        
    def insert(self, authors: dict):
        '''
        作者情報を挿入する
        
        Parameters
        ----------
        authors : dict
            作者情報
        '''
        columns = ', '.join(authors.keys())
        placeholders = ', '.join(['?' for _ in authors.values()])
        query = f"INSERT OR IGNORE INTO {self.table_info['name']} ({columns}) VALUES ({placeholders})"
        self.db_manager.execute_query(query, tuple(authors.values()))
    
    def get_author_id(self, author_name: str) -> int:
        '''
        作者名から作者IDを取得する
        
        Parameters
        ----------
        author_name : str
            作者名
        
        Returns
        -------
        int
            作者ID
        '''
        query = f"SELECT {AUTHOR_ID} FROM {self.table_info['name']} WHERE {AUTHOR_NAME} = ?"
        res = self.db_manager.execute_query(query, (author_name,))
        return res.fetchone()[0]