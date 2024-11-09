from ..common import (
    DatabaseManager,
    TableManagerInterface
)
from ..constants import (
    AGE_RATING_TABLE,
    AGE_RATING_ID,
    AGE_RATING_NAME,
)

class AgeRatingTableManager(TableManagerInterface):
    def __init__(self, db_manager: DatabaseManager):
        # テーブル情報
        table_info  = {
            'name': AGE_RATING_TABLE,
            'columns': [
                AGE_RATING_ID,
                AGE_RATING_NAME
            ]
        }
        
        # テーブルのカラム名とデータ型
        columns_with_types = {
            AGE_RATING_ID: 'INTEGER PRIMARY KEY AUTOINCREMENT',
            AGE_RATING_NAME: 'TEXT UNIQUE NOT NULL'
        }
        
        # 親クラスのコンストラクタを呼び出す
        super().__init__(db_manager, table_info, columns_with_types)
    
    def insert(self, age_ratings: dict):
        '''
        年齢レーティング情報を挿入する
        
        Parameters
        ----------
        age_ratings : dict
            年齢レーティング情報
        '''
        columns = ', '.join(age_ratings.keys())
        placeholders = ', '.join(['?' for _ in age_ratings.values()])
        query = f"INSERT OR IGNORE INTO {self.table_info['name']} ({columns}) VALUES ({placeholders})"
        self.db_manager.execute_query(query, tuple(age_ratings.values()))
    
    def get_age_rating_id(self, age_rating_name: str) -> int:
        '''
        年齢レーティング名から年齢レーティングIDを取得する
        
        Parameters
        ----------
        age_rating_name : str
            年齢レーティング名
        
        Returns
        -------
        int
            年齢レーティングID（見つからない場合はNoneまたは例外を発生させる）
        '''
        query = f"SELECT {AGE_RATING_ID} FROM {self.table_info['name']} WHERE {AGE_RATING_NAME} = ?"
        res = self.db_manager.execute_query(query, (age_rating_name,))
        record = res.fetchone()
        return record[0] if record else None