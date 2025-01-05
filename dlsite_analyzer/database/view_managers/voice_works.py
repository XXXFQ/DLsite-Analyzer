import pandas as pd
from ..common import SQLiteHandler, ViewHandlerInterface
from ..constants import (
    # Voice Works Table
    VOICE_WORKS_TABLE, VOICE_WORKS_PRIMARY_KEY, VOICE_WORKS_TITLE, VOICE_WORKS_URL,
    VOICE_WORKS_PRODUCT_FORMAT_ID, VOICE_WORKS_CIRCLE_ID, VOICE_WORKS_VOICE_ACTOR_ID, VOICE_WORKS_PRICE,
    VOICE_WORKS_POINTS, VOICE_WORKS_SALES_COUNT, VOICE_WORKS_REVIEW_COUNT, VOICE_WORKS_AGE_ID, VOICE_WORKS_FULL_IMAGE_URL,
    # Makers Table
    CIRCLES_TABLE, CIRCLE_PRIMARY_KEY, CIRCLE_NAME,
    # Categories Table
    PRODUCT_FORMAT_TABLE, PRODUCT_FORMAT_PRIMARY_KEY, PRODUCT_FORMAT_NAME,
    # Authors Table
    VOICE_ACTORS_TABLE, VOICE_ACTOR_PRIMARY_KEY, VOICE_ACTOR_NAME,
    # Age Ratings Table
    AGE_RATING_TABLE, AGE_RATING_PRIMARY_KEY, AGE_RATING_NAME,
    # Voice Works View
    VOICE_WORKS_VIEW, VOICE_WORKS_PRODUCT_FORMAT_VIEW, VOICE_WORKS_VIEW_CIRCLE,
    VOICE_WORKS_VIEW_VOICE_ACTOR, VOICE_WORKS_VIEW_AGE,
)

class VoiceWorksViewHandler(ViewHandlerInterface):
    '''
    A handler for managing the Voice Works view in the database.
    '''
    def __init__(self, db_connection: SQLiteHandler):
        '''
        Initialize the VoiceWorksViewHandler.

        Parameters
        ----------
        db_connection : SQLiteHandler
            A database connection handler.
        '''
        view_name = VOICE_WORKS_VIEW
        select_query = self._build_select_query()
        super().__init__(db_connection, view_name, select_query)

    @staticmethod
    def _build_select_query() -> str:
        '''
        Build the SQL query for the Voice Works view.

        Returns
        -------
        str
            The SQL query defining the Voice Works view.
        '''
        return f'''
        SELECT
            {VOICE_WORKS_TABLE}.{VOICE_WORKS_PRIMARY_KEY},
            {VOICE_WORKS_TABLE}.{VOICE_WORKS_TITLE},
            {VOICE_WORKS_TABLE}.{VOICE_WORKS_URL},
            {PRODUCT_FORMAT_TABLE}.{PRODUCT_FORMAT_NAME} AS {VOICE_WORKS_PRODUCT_FORMAT_VIEW},
            {CIRCLES_TABLE}.{CIRCLE_NAME} AS {VOICE_WORKS_VIEW_CIRCLE},
            {VOICE_ACTORS_TABLE}.{VOICE_ACTOR_NAME} AS {VOICE_WORKS_VIEW_VOICE_ACTOR},
            {VOICE_WORKS_TABLE}.{VOICE_WORKS_PRICE},
            {VOICE_WORKS_TABLE}.{VOICE_WORKS_POINTS},
            {VOICE_WORKS_TABLE}.{VOICE_WORKS_SALES_COUNT},
            {VOICE_WORKS_TABLE}.{VOICE_WORKS_REVIEW_COUNT},
            {AGE_RATING_TABLE}.{AGE_RATING_NAME} AS {VOICE_WORKS_VIEW_AGE},
            {VOICE_WORKS_TABLE}.{VOICE_WORKS_FULL_IMAGE_URL}
        FROM
            {VOICE_WORKS_TABLE}
        INNER JOIN {CIRCLES_TABLE}
            ON {VOICE_WORKS_TABLE}.{VOICE_WORKS_CIRCLE_ID} = {CIRCLES_TABLE}.{CIRCLE_PRIMARY_KEY}
        INNER JOIN {PRODUCT_FORMAT_TABLE}
            ON {VOICE_WORKS_TABLE}.{VOICE_WORKS_PRODUCT_FORMAT_ID} = {PRODUCT_FORMAT_TABLE}.{PRODUCT_FORMAT_PRIMARY_KEY}
        INNER JOIN {VOICE_ACTORS_TABLE}
            ON {VOICE_WORKS_TABLE}.{VOICE_WORKS_VOICE_ACTOR_ID} = {VOICE_ACTORS_TABLE}.{VOICE_ACTOR_PRIMARY_KEY}
        INNER JOIN {AGE_RATING_TABLE}
            ON {VOICE_WORKS_TABLE}.{VOICE_WORKS_AGE_ID} = {AGE_RATING_TABLE}.{AGE_RATING_PRIMARY_KEY}
        ORDER BY
            {VOICE_WORKS_TABLE}.{VOICE_WORKS_PRIMARY_KEY}
        '''

    def get_all_voice_works(self) -> pd.DataFrame:
        '''
        Retrieve all voice works information from the view.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing all voice works information.
        '''
        query = f"SELECT * FROM {self.view_name}"
        try:
            res = self.db_connection.execute_query(query)
            return pd.DataFrame(res.fetchall(), columns=self.get_columns())
        except Exception as e:
            raise RuntimeError(f"Failed to fetch voice works data: {e}")
