from ..common import (
    DatabaseManager,
    TableManagerInterface
)
from ..constants import (
    PRODUCT_FORMAT_TABLE,
    PRODUCT_FORMAT_PRIMARY_KEY,
    PRODUCT_FORMAT_NAME,
)

class CategoriesTableManager(TableManagerInterface):
    def __init__(self, db_manager: DatabaseManager):
        # テーブル情報
        table_info  = {
            'name': PRODUCT_FORMAT_TABLE,
            'columns': [
                PRODUCT_FORMAT_PRIMARY_KEY,
                PRODUCT_FORMAT_NAME
            ]
        }
        
        # テーブルのカラム名とデータ型
        columns_with_types = {
            PRODUCT_FORMAT_PRIMARY_KEY: 'INTEGER PRIMARY KEY AUTOINCREMENT',
            PRODUCT_FORMAT_NAME: 'TEXT UNIQUE NOT NULL'
        }
        
        # 親クラスのコンストラクタを呼び出す
        super().__init__(db_manager, table_info, columns_with_types)
    
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
        query = f"SELECT {PRODUCT_FORMAT_PRIMARY_KEY} FROM {self.table_info['name']} WHERE {PRODUCT_FORMAT_NAME} = ?"
        res = self.db_manager.execute_query(query, (category_name,))
        record = res.fetchone()
        return record[0] if record else None