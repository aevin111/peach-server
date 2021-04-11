import sqlite3


class SQLiteDatabase:
    def __init__(self, file_name):
        self._file_name = file_name
        
    def _create_connection(self):
        try:
            return sqlite3.connect(self._file_name)
        except sqlite3.Error as exception:
            pass
        return None

    def _close_cursor(self, cursor):
        try:
            cursor.close()
        except sqlite3.Error as exception:
            pass

    def _close_connection(self, connection):
        try:
            connection.close()
        except sqlite3.Error as exception:
            pass

    def execute_update(self, statement, parameters):
        try:
            connection = self._create_connection()
            cursor = connection.cursor()
            cursor.execute(statement, parameters)
            connection.commit()
            success = True
        except sqlite3.Error as exception:
            print(exception)
            success = False
        finally:
            self._close_cursor(cursor)
            self._close_connection(connection)
        return success

    def execute_query(self, statement, parameters):
        try:
            connection = self._create_connection()
            cursor = connection.cursor()
            cursor.execute(statement, parameters)
            result = cursor.fetchall()
        except sqlite3.Error as exception:
            print(exception)
            result = None
        finally:
            self._close_cursor(cursor)
            self._close_connection(connection)
        return result
    
    def close_cursor_manually(self, cursor):
        self._close_cursor(cursor)
        
    def close_connection_manually(self, connection):
        self._close_connection(connection)
    
    def fetch_all_data(self, statement, parameters):
        try:
            connection = self._create_connection()
            cursor = connection.cursor()
            cursor.execute(statement, parameters)
            result = cursor.fetchall()
        except sqlite3.Error as exception:
            self._close_cursor(cursor)
            self._close_connection(connection)
            result = None
            cursor = None
            connection = None
        return [result, cursor, connection]
