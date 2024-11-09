import pandas as pd

from ..common import (
    DatabaseManager,
    TableManagerInterface
)
from ..constants import (
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
    VOICE_WORKS_AGE_RATING_ID,
    VOICE_WORKS_FULL_IMAGE_URL,
    MAKERS_TABLE,
    CATEGORY_TABLE,
    AUTHORS_TABLE,
    AGE_RATING_TABLE,
)

class VoiceWorksTableManager(TableManagerInterface):
    def __init__(self, db_manager: DatabaseManager):
        '''
        ボイス作品テーブルマネージャ
        
        Parameters
        ----------
        db_manager : DatabaseManager
            データベースマネージャ  
        '''
        # テーブル情報
        table_info  = {
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
                VOICE_WORKS_AGE_RATING_ID,
                VOICE_WORKS_FULL_IMAGE_URL,
            ]
        }
        
        # テーブルのカラム名とデータ型
        columns_with_types = {
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
            VOICE_WORKS_AGE_RATING_ID: 'INTEGER',
            VOICE_WORKS_FULL_IMAGE_URL: 'TEXT',
        }
        
        # 外部キー制約
        foreign_keys = [
            f"FOREIGN KEY ({VOICE_WORKS_CATEGORY_ID}) REFERENCES {CATEGORY_TABLE} ({VOICE_WORKS_CATEGORY_ID})",
            f"FOREIGN KEY ({VOICE_WORKS_MAKER_ID}) REFERENCES {MAKERS_TABLE} ({VOICE_WORKS_MAKER_ID})",
            f"FOREIGN KEY ({VOICE_WORKS_AUTHOR_ID}) REFERENCES {AUTHORS_TABLE} ({VOICE_WORKS_AUTHOR_ID})",
            f"FOREIGN KEY ({VOICE_WORKS_AGE_RATING_ID}) REFERENCES {AGE_RATING_TABLE} ({VOICE_WORKS_AGE_RATING_ID})"
        ]
        
        # 親クラスのコンストラクタを呼び出す
        super().__init__(db_manager, table_info, columns_with_types, foreign_keys)
    
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