from ..common import (
    DatabaseManager,
    TableManagerInterface
)
from ..constants import (
    CIRCLES_TABLE,
    CIRCLE_PRIMARY_KEY,
    CIRCLE_NAME,
)

class MakersTableManager(TableManagerInterface):
    def __init__(self, db_manager: DatabaseManager):
        # テーブル情報
        table_info  = {
            'name': CIRCLES_TABLE,
            'columns': [
                CIRCLE_PRIMARY_KEY,
                CIRCLE_NAME
            ]
        }
        
        # テーブルのカラム名とデータ型
        columns_with_types = {
            CIRCLE_PRIMARY_KEY: 'TEXT PRIMARY KEY',
            CIRCLE_NAME: 'TEXT NOT NULL'
        }
        
        # 親クラスのコンストラクタを呼び出す
        super().__init__(db_manager, table_info, columns_with_types)
    
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