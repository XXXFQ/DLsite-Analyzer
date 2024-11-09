from ..common import (
    DatabaseManager,
    TableManagerInterface
)
from ..constants import (
    AUTHORS_TABLE,
    AUTHOR_ID,
    AUTHOR_NAME,
)

class AuthorsTableManager(TableManagerInterface):
    def __init__(self, db_manager: DatabaseManager):
        # テーブル情報
        table_info  = {
            'name': AUTHORS_TABLE,
            'columns': [
                AUTHOR_ID,
                AUTHOR_NAME
            ]
        }
        
        # テーブルのカラム名とデータ型
        columns_with_types = {
            AUTHOR_ID: 'INTEGER PRIMARY KEY AUTOINCREMENT',
            AUTHOR_NAME: 'TEXT UNIQUE NOT NULL'
        }
        
        # 親クラスのコンストラクタを呼び出す
        super().__init__(db_manager, table_info, columns_with_types)
     
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
        record = res.fetchone()
        return record[0] if record else None