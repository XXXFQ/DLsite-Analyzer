import sqlite3
from typing import Dict, Optional

class SQLiteHandler:
    '''
    Handles SQLite database operations with context management.
    '''
    def __init__(self, db_path: str):
        '''
        Initialize the database connection.

        Parameters
        ----------
        db_path : str
            Path to the SQLite database file.
        '''
        self._connection = sqlite3.connect(db_path) # データベース接続
        self._cursor = self._connection.cursor() # カーソル

    def __enter__(self) -> 'SQLiteHandler':
        '''
        Begin a transaction on entering the context.
        '''
        self.execute_query('BEGIN')
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        '''
        Commit or rollback transaction and close the connection on exiting the context.
        '''
        if exc_type is None:
            self.commit()
        else:
            self._connection.rollback()
        self._connection.close()

    def execute_query(self, query: str, params: tuple=None) -> sqlite3.Cursor:
        '''
        Execute a single query.

        Parameters
        ----------
        query : str
            The SQL query to execute.
        params : tuple, optional
            Parameters for the query.

        Returns
        -------
        sqlite3.Cursor
            Cursor object containing query results.
        '''
        return self._cursor.execute(query, params or ())
    
    def executemany_query(self, query: str, params: list) -> sqlite3.Cursor:
        '''
        Execute a query with multiple parameter sets.

        Parameters
        ----------
        query : str
            The SQL query to execute.
        params : list
            List of parameter tuples.

        Returns
        -------
        sqlite3.Cursor
            Cursor object containing query results.
        '''
        return self._cursor.executemany(query, params)
    
    def commit(self) -> None:
        '''
        Commit the current transaction.
        '''
        self._connection.commit()
    
    def close(self) -> None:
        '''
        Close the database connection.
        '''
        self._connection.close()

class TableHandlerInterface:
    '''
    Generic handler for managing database tables.
    '''
    def __init__(self, db_connection: SQLiteHandler, table_name: str, columns_with_types: dict, primary_key: str, foreign_keys: list=None):
        '''
        Initialize a handler for a specific database table.

        Parameters
        ----------
        db_connection : SQLiteHandler
            Database connection handler.
        table_name : str
            Name of the table to manage.
        columns_with_types : dict
            Dictionary mapping column names to their types.
        primary_key : str
            Name of the primary key column.
        foreign_keys : list, optional
            List of foreign key constraints (default is None).
        '''
        self.db_connection = db_connection
        self.table_name = table_name
        self.columns_with_types = columns_with_types
        self.primary_key = primary_key
        self.foreign_keys = foreign_keys or []
    
    def create_table(self) -> None:
        '''
        Create the table with specified schema.
        '''
        columns = ', '.join([f"{col} {dtype}" for col, dtype in self.columns_with_types.items()])
        foreign_keys = ', '.join(self.foreign_keys)
        constraints = f", {foreign_keys}" if foreign_keys else ""

        query = f'''
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            {columns}{constraints}
        )
        '''
        self.db_connection.execute_query(query)
        self.db_connection.commit()
    
    def create_index(self) -> None:
        '''
        Create an index on the primary key.
        '''
        query = f"""
        CREATE INDEX IF NOT EXISTS idx_{self.table_name}_{self.primary_key}
        ON {self.table_name} ({self.primary_key})
        """
        self.db_connection.execute_query(query)
        self.db_connection.commit()
    
    def insert(self, record: dict) -> None:
        '''
        Insert data into the table.
        
        Parameters
        ----------
        record : dict
            Dictionary of column data.
        '''
        columns = ', '.join(record.keys())
        placeholders = ', '.join(['?' for _ in record.values()])
        query = f"INSERT OR IGNORE INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        self.db_connection.execute_query(query, tuple(record.values()))
    
    def fetch_all(self) -> dict:
        '''
        Fetch all rows from the table.

        Returns
        -------
        dict
            Dictionary of rows with the primary key as the key and other data as the value.
        '''
        query = f"SELECT * FROM {self.table_name}"
        results = self.db_connection.execute_query(query).fetchall()
        return {row[0]: row[1:] for row in results}
    
    def fetch_results_as_dict(self, query: str, params: Optional[tuple]=None) -> Dict[int, Dict]:
        '''
        Execute a query and fetch results as a dictionary.

        Parameters
        ----------
        query : str
            SQL query to execute.
        params : tuple, optional
            Parameters for the query.

        Returns
        -------
        dict
            Dictionary of results keyed by the primary key.
        '''
        result = self.db_connection.execute_query(query, params).fetchall()
        columns = self._get_columns()
        return {
            row[0]: {column: row[i] for i, column in enumerate(columns)}
            for row in result
        }
    
    def _get_columns(self) -> list:
        '''
        Retrieve column names from the view.

        Returns
        -------
        list
            List of column names.
        '''
        query = f"PRAGMA table_info({self.table_name})"
        result = self.db_connection.execute_query(query)
        return [row[1] for row in result.fetchall()]

class ViewHandlerInterface:
    '''
    Generic handler for managing database views.
    '''
    def __init__(self, db_connection: SQLiteHandler, view_name: str, select_query: str):
        '''
        Initialize a handler for a specific database view.

        Parameters
        ----------
        db_connection : SQLiteHandler
            Database connection handler.
        view_name : str
            Name of the view to manage.
        select_query : str
            SQL query defining the view.
        '''
        self.db_connection = db_connection
        self.view_name = view_name
        self.select_query = select_query
        
    def create_view(self) -> None:
        '''
        Create the view with specified SQL.
        '''
        query = f"""
        CREATE VIEW IF NOT EXISTS {self.view_name} AS
        {self.select_query}
        """
        self.db_connection.execute_query(query)
        self.db_connection.commit()
    
    def get_columns(self) -> list:
        '''
        Retrieve column names from the view.

        Returns
        -------
        list
            List of column names.
        '''
        query = f"PRAGMA table_info({self.view_name})"
        result = self.db_connection.execute_query(query)
        return [row[1] for row in result.fetchall()]
