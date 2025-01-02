import pandas as pd

from ..common import (
    DatabaseManager,
    TableManagerInterface
)
from ..constants import (
    VOICE_WORKS_TABLE,
    VOICE_WORKS_PRIMARY_KEY,
    VOICE_WORKS_TITLE,
    VOICE_WORKS_URL,
    PRODUCT_FORMAT_FOREIGN_KEY,
    CIRCLES_FOREIGN_KEY,
    VOICE_ACTORS_FOREIGN_KEY,
    VOICE_WORKS_PRICE,
    VOICE_WORKS_POINTS,
    VOICE_WORKS_SALES_COUNT,
    VOICE_WORKS_REVIEW_COUNT,
    AGE_FOREIGN_KEY,
    VOICE_WORKS_FULL_IMAGE_URL,
    CIRCLES_TABLE,
    PRODUCT_FORMAT_TABLE,
    VOICE_ACTORS_TABLE,
    AGE_TABLE,
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
                VOICE_WORKS_PRIMARY_KEY,
                VOICE_WORKS_TITLE,
                VOICE_WORKS_URL,
                PRODUCT_FORMAT_FOREIGN_KEY,
                CIRCLES_FOREIGN_KEY,
                VOICE_ACTORS_FOREIGN_KEY,
                VOICE_WORKS_PRICE,
                VOICE_WORKS_POINTS,
                VOICE_WORKS_SALES_COUNT,
                VOICE_WORKS_REVIEW_COUNT,
                AGE_FOREIGN_KEY,
                VOICE_WORKS_FULL_IMAGE_URL,
            ]
        }
        
        # テーブルのカラム名とデータ型
        columns_with_types = {
            VOICE_WORKS_PRIMARY_KEY: 'TEXT PRIMARY KEY',
            VOICE_WORKS_TITLE: 'TEXT NOT NULL',
            VOICE_WORKS_URL: 'TEXT NOT NULL',
            PRODUCT_FORMAT_FOREIGN_KEY: 'INTEGER',
            CIRCLES_FOREIGN_KEY: 'INTEGER',
            VOICE_ACTORS_FOREIGN_KEY: 'INTEGER',
            VOICE_WORKS_PRICE: 'INTEGER',
            VOICE_WORKS_POINTS: 'INTEGER',
            VOICE_WORKS_SALES_COUNT: 'INTEGER',
            VOICE_WORKS_REVIEW_COUNT: 'INTEGER',
            AGE_FOREIGN_KEY: 'INTEGER',
            VOICE_WORKS_FULL_IMAGE_URL: 'TEXT',
        }
        
        # 外部キー制約
        foreign_keys = [
            f"FOREIGN KEY ({PRODUCT_FORMAT_FOREIGN_KEY}) REFERENCES {PRODUCT_FORMAT_TABLE} ({PRODUCT_FORMAT_FOREIGN_KEY})",
            f"FOREIGN KEY ({CIRCLES_FOREIGN_KEY}) REFERENCES {CIRCLES_TABLE} ({CIRCLES_FOREIGN_KEY})",
            f"FOREIGN KEY ({VOICE_ACTORS_FOREIGN_KEY}) REFERENCES {VOICE_ACTORS_TABLE} ({VOICE_ACTORS_FOREIGN_KEY})",
            f"FOREIGN KEY ({AGE_FOREIGN_KEY}) REFERENCES {AGE_TABLE} ({AGE_FOREIGN_KEY})"
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