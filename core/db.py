import sqlite3
from core.config import SETTINGS

_conn = None

def get_connection():
    """
    Returns a single sqlite3.Connection for SETTINGS['database_path'].
    If that Connection has been closed, it will re-open it.
    """
    global _conn

    # If we already had a connection but it's closed, reset it.
    if _conn is not None:
        try:
            _conn.cursor()
        except sqlite3.ProgrammingError:
            _conn = None

    if _conn is None:
        _conn = sqlite3.connect(
            SETTINGS['database_path'],
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            check_same_thread=False,
            uri=True  # allows file:... URIs if you ever switch
        )
        _conn.row_factory = sqlite3.Row

    return _conn
