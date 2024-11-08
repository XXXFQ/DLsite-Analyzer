import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        '''
        データベースを開く
        
        Parameters
        ----------
        db_path : str
            データベースファイルのパス
        
        Attributes
        ----------
        connection : sqlite3.Connection
            データベース接続
        cursor : sqlite3.Cursor
            カーソル
        '''
        self._connection = sqlite3.connect(db_path)
        self._cursor = self._connection.cursor()

    def __enter__(self) -> 'DatabaseManager':
        '''
        トランザクションを開始する
        '''
        self.execute_query('BEGIN')
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        '''
        トランザクションを終了する
        '''
        if exc_type is None:
            self.commit()
        else:
            self._connection.rollback()
        self._connection.close()
    
    def __del__(self):
        '''
        データベースを閉じる
        '''
        self._connection.close()

    def execute_query(self, query, params=None) -> sqlite3.Cursor:
        '''
        クエリを実行する
        
        Parameters
        ----------
        query : str
            クエリ
        params : tuple
            クエリのパラメータ
        
        Returns
        -------
        sqlite3.Cursor
            カーソル
        '''
        if params:
            res = self._cursor.execute(query, params)
        else:
            res = self._cursor.execute(query)
        return res

    def commit(self):
        '''
        変更を保存する
        '''
        self._connection.commit()