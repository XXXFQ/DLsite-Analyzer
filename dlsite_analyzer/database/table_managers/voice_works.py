import pandas as pd
from ..common import SQLiteHandler, TableHandlerInterface
from ..constants import (
    VOICE_WORKS_TABLE,
    VOICE_WORKS_PRIMARY_KEY,
    VOICE_WORKS_TITLE,
    VOICE_WORKS_URL,
    VOICE_WORKS_PRODUCT_FORMAT_ID,
    VOICE_WORKS_CIRCLE_ID,
    VOICE_WORKS_VOICE_ACTOR_ID,
    VOICE_WORKS_PRICE,
    VOICE_WORKS_POINTS,
    VOICE_WORKS_SALES_COUNT,
    VOICE_WORKS_REVIEW_COUNT,
    VOICE_WORKS_AGE_ID,
    VOICE_WORKS_FULL_IMAGE_URL,
    CIRCLES_TABLE,
    PRODUCT_FORMAT_TABLE,
    VOICE_ACTORS_TABLE,
    AGE_RATING_TABLE,
)

class VoiceWorksTableHandler(TableHandlerInterface):
    '''
    A handler for managing the Voice Works table in the database.
    '''
    def __init__(self, db_connection: SQLiteHandler):
        '''
        Initialize the VoiceWorksTableHandler.

        Parameters
        ----------
        db_connection : SQLiteHandler
            A database connection handler.
        '''
        table_name = VOICE_WORKS_TABLE
        columns_with_types = {
            VOICE_WORKS_PRIMARY_KEY: "TEXT PRIMARY KEY",
            VOICE_WORKS_TITLE: "TEXT NOT NULL",
            VOICE_WORKS_URL: "TEXT NOT NULL",
            VOICE_WORKS_PRODUCT_FORMAT_ID: "INTEGER",
            VOICE_WORKS_CIRCLE_ID: "INTEGER",
            VOICE_WORKS_VOICE_ACTOR_ID: "INTEGER",
            VOICE_WORKS_PRICE: "INTEGER",
            VOICE_WORKS_POINTS: "INTEGER",
            VOICE_WORKS_SALES_COUNT: "INTEGER",
            VOICE_WORKS_REVIEW_COUNT: "INTEGER",
            VOICE_WORKS_AGE_ID: "INTEGER",
            VOICE_WORKS_FULL_IMAGE_URL: "TEXT",
        }
        foreign_keys = [
            f"FOREIGN KEY ({VOICE_WORKS_PRODUCT_FORMAT_ID}) REFERENCES {PRODUCT_FORMAT_TABLE} ({VOICE_WORKS_PRODUCT_FORMAT_ID})",
            f"FOREIGN KEY ({VOICE_WORKS_CIRCLE_ID}) REFERENCES {CIRCLES_TABLE} ({VOICE_WORKS_CIRCLE_ID})",
            f"FOREIGN KEY ({VOICE_WORKS_VOICE_ACTOR_ID}) REFERENCES {VOICE_ACTORS_TABLE} ({VOICE_WORKS_VOICE_ACTOR_ID})",
            f"FOREIGN KEY ({VOICE_WORKS_AGE_ID}) REFERENCES {AGE_RATING_TABLE} ({VOICE_WORKS_AGE_ID})"
        ]
        super().__init__(db_connection, table_name, columns_with_types, VOICE_WORKS_PRIMARY_KEY, foreign_keys)

    def get_all_voice_works(self) -> pd.DataFrame:
        '''
        Retrieve all voice works information from the table.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing all voice works information.
        '''
        query = f"SELECT * FROM {self.table_name}"
        try:
            res = self.db_connection.execute_query(query)
            return pd.DataFrame(res.fetchall(), columns=self.columns_with_types.keys())
        except Exception as e:
            raise RuntimeError(f"Failed to fetch voice works data: {e}")
