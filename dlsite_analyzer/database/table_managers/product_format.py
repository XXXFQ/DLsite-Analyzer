from ..common import SQLiteHandler, TableHandlerInterface
from ..constants import (
    PRODUCT_FORMAT_TABLE,
    PRODUCT_FORMAT_PRIMARY_KEY,
    PRODUCT_FORMAT_NAME,
)

class ProductFormatTableHandler(TableHandlerInterface):
    '''
    A handler for managing the Product Format table in the database.
    '''
    def __init__(self, db_connection: SQLiteHandler):
        '''
        Initialize the ProductFormatTableHandler.

        Parameters
        ----------
        db_connection : SQLiteHandler
            A database connection handler.
        '''
        table_name = PRODUCT_FORMAT_TABLE
        columns_with_types = {
            PRODUCT_FORMAT_PRIMARY_KEY: "INTEGER PRIMARY KEY AUTOINCREMENT",
            PRODUCT_FORMAT_NAME: "TEXT UNIQUE NOT NULL",
        }
        super().__init__(db_connection, table_name, columns_with_types, PRODUCT_FORMAT_PRIMARY_KEY)

    def get_product_format_id(self, format_name: str) -> int | None:
        '''
        Retrieve the ID of a product format based on its name.

        Parameters
        ----------
        format_name : str
            The name of the product format.

        Returns
        -------
        int | None
            The ID of the product format if found, otherwise None.

        Raises
        ------
        ValueError
            If the format_name is None or an empty string.
        '''
        query = f"""
        SELECT {PRODUCT_FORMAT_PRIMARY_KEY}
        FROM {self.table_name}
        WHERE {PRODUCT_FORMAT_NAME} = ?
        """
        try:
            res = self.db_connection.execute_query(query, (format_name,))
            record = res.fetchone()
            return record[0] if record else None
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve product format ID: {e}")
