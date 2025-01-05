from ..common import SQLiteHandler, TableHandlerInterface
from ..constants import CIRCLES_TABLE, CIRCLE_PRIMARY_KEY, CIRCLE_NAME

class CirclesTableHandler(TableHandlerInterface):
    '''
    A handler for managing the Circles table in the database.
    '''
    def __init__(self, db_connection: SQLiteHandler):
        '''
        Initialize the CirclesTableHandler.

        This sets up the table schema and inherits the basic operations
        from TableHandlerInterface.

        Parameters
        ----------
        db_connection : SQLiteHandler
            A database connection handler.
        '''
        table_name = CIRCLES_TABLE
        columns_with_types = {
            CIRCLE_PRIMARY_KEY: "TEXT PRIMARY KEY",
            CIRCLE_NAME: "TEXT NOT NULL",
        }
        super().__init__(db_connection, table_name, columns_with_types, CIRCLE_PRIMARY_KEY)
