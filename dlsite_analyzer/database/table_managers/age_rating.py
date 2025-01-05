from ..common import (
    SQLiteHandler,
    TableHandlerInterface
)
from ..constants import (
    AGE_RATING_TABLE,
    AGE_RATING_PRIMARY_KEY,
    AGE_RATING_NAME,
)

class AgeRatingTableHandler(TableHandlerInterface):
    '''
    A handler for managing the Age Rating table in the database.
    '''
    def __init__(self, db_connection: SQLiteHandler):
        '''
        Initialize the AgeRatingTableHandler.

        Parameters
        ----------
        db_connection : SQLiteHandler
            Database connection handler.
        '''
        table_name = AGE_RATING_TABLE
        columns_with_types = {
            AGE_RATING_PRIMARY_KEY: 'INTEGER PRIMARY KEY AUTOINCREMENT',
            AGE_RATING_NAME: 'TEXT UNIQUE NOT NULL',
        }
        super().__init__(db_connection, table_name, columns_with_types, AGE_RATING_PRIMARY_KEY)
    
    def get_age_rating_id(self, age_rating_name: str) -> int | None:
        '''
        Retrieve the age rating ID based on the given age rating name.

        Parameters
        ----------
        age_rating_name : str
            The name of the age rating.

        Returns
        -------
        int | None
            The ID of the age rating if found, otherwise None.

        Raises
        ------
        ValueError
            If the age_rating_name is None or an empty string.
        '''
        if not age_rating_name:
            raise ValueError("The age rating name cannot be empty.")

        query = f'''
        SELECT {AGE_RATING_PRIMARY_KEY}
        FROM {self.table_name}
        WHERE {AGE_RATING_NAME} = ?
        '''
        try:
            res = self.db_connection.execute_query(query, (age_rating_name,))
            record = res.fetchone()
            return record[0] if record else None
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve age rating ID: {e}")
