from ..common import (
    SQLiteHandler,
    TableHandlerInterface
)
from ..constants import (
    VOICE_ACTORS_TABLE,
    VOICE_ACTOR_PRIMARY_KEY,
    VOICE_ACTOR_NAME,
)

class VoiceActorsTableHandler(TableHandlerInterface):
    '''
    A handler for managing the Voice Actors table in the database.
    '''
    def __init__(self, db_connection: SQLiteHandler):
        '''
        Initialize the VoiceActorsTableHandler.

        Parameters
        ----------
        db_connection : SQLiteHandler
            Database connection handler.
        '''
        table_name = VOICE_ACTORS_TABLE
        columns_with_types = {
            VOICE_ACTOR_PRIMARY_KEY: "INTEGER PRIMARY KEY AUTOINCREMENT",
            VOICE_ACTOR_NAME: "TEXT UNIQUE NOT NULL",
        }
        super().__init__(db_connection, table_name, columns_with_types, VOICE_ACTOR_PRIMARY_KEY)

    def get_voice_actor_id(self, voice_actor_name: str) -> int | None:
        '''
        Retrieve the ID of a voice actor based on their name.

        Parameters
        ----------
        voice_actor_name : str
            The name of the voice actor.

        Returns
        -------
        int | None
            The ID of the voice actor if found, otherwise None.

        Raises
        ------
        ValueError
            If the voice_actor_name is None or an empty string.
        '''
        query = f'''
        SELECT {VOICE_ACTOR_PRIMARY_KEY}
        FROM {self.table_name}
        WHERE {VOICE_ACTOR_NAME} = ?
        '''
        try:
            res = self.db_connection.execute_query(query, (voice_actor_name,))
            record = res.fetchone()
            return record[0] if record else None
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve voice actor ID: {e}")
