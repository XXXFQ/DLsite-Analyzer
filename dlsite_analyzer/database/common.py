import sqlite3

class DatabaseManager:
    def __init__(self, db_path: str):
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

class TableManagerInterface:
    def __init__(self, db_manager: DatabaseManager, table_info: dict, columns_with_types: dict, foreign_keys: list=None):
        '''
        データベースを開く
        
        Parameters
        ----------
        db_manager : DatabaseManager
            データベースマネージャ
        table_info : dict
            テーブル情報
        columns_with_types : dict
            カラム名とデータ型
        foreign_keys : list
            外部キー制約
        
        Attributes
        ----------
        connection : sqlite3.Connection
            データベース接続
        cursor : sqlite3.Cursor
            カーソル
        '''
        self.db_manager = db_manager # データベースマネージャ
        self.table_info = table_info # テーブル情報
        self.columns_with_types = columns_with_types # カラム名とデータ型
        self.foreign_keys = foreign_keys # 外部キー制約
    
    def create_table(self):
        '''
        テーブルを作成する
        '''
        # カラム名とデータ型を取得する
        columns = ', '.join([f"{col} {data_type}" for col, data_type in self.columns_with_types.items()])
        
        if self.foreign_keys:
            # 外部キー制約がある場合
            foreign_keys = ', '.join(self.foreign_keys)
            query = f"CREATE TABLE IF NOT EXISTS {self.table_info['name']} ({columns}, {foreign_keys})"
        else:
            query = f"CREATE TABLE IF NOT EXISTS {self.table_info['name']} ({columns})"
        
        # テーブルを作成する
        self.db_manager.execute_query(query)
        self.db_manager.commit()
    
    def get_columns(self) -> list:
        '''
        カラム名のリストを取得する
        
        Returns
        -------
        list
            カラム名のリスト
        '''
        query = f"PRAGMA table_info({self.table_info['name']})"
        res = self.db_manager.execute_query(query)
        return [column[1] for column in res.fetchall()]

class ViewManagerInterface:
    def __init__(self, db_manager: DatabaseManager, view_info: dict, tables: list, joins: list, order_by: str):
        '''
        データベースを開く
        
        Parameters
        ----------
        db_manager : DatabaseManager
            データベースマネージャ
        view_info : dict
            ビューの情報
        tables : list
            テーブルの情報
        joins : list
            ビューの結合条件
        order_by : str
            ビューの並び順
        
        Attributes
        ----------
        connection : sqlite3.Connection
            データベース接続
        cursor : sqlite3.Cursor
            カーソル
        '''
        self.db_manager = db_manager # データベースマネージャ
        self.view_info = view_info # ビューの情報
        self.tables = tables # テーブルの情報
        self.joins = joins # ビューの結合条件
        self.order_by = order_by # ビューの並び順
    
    def create_view(self) -> None:
        '''
        ビューを作成する
        '''
        columns = ', '.join(self.view_info['columns'])
        from_clause = ', '.join(self.tables)
        join_clause = ' AND '.join(self.joins)
        query = f'''
        CREATE VIEW IF NOT EXISTS {self.view_info['name']} AS
        SELECT
            {columns}
        FROM
            {from_clause}
        WHERE
            {join_clause}
        ORDER BY
            {self.order_by}
        '''
        self.db_manager.execute_query(query)
        self.db_manager.commit()
    
    def get_columns(self) -> list:
        '''
        カラム名のリストを取得する
        
        Returns
        -------
        list
            カラム名のリスト
        '''
        query = f"PRAGMA table_info({self.view_info['name']})"
        res = self.db_manager.execute_query(query)
        return [column[1] for column in res.fetchall()]