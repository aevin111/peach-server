from lib.sqlite_database import SQLiteDatabase


class SQLiteDataFetcher:
    def __init__(self, file_name):
        self._database = SQLiteDatabase(file_name)
        
    def _check_raw_data(self, raw_data):
        if raw_data[0] == None or raw_data[1] == None or raw_data[2] == None:
            return False
        else:
            return True

    def _close_all_resources(self, database, raw_data):
        database.close_cursor_manually(raw_data[1])
        database.close_connection_manually(raw_data[2])

    def fetch_data(self, statement, parameters):
        raw_data = self._database.fetch_all_data(statement, parameters)
        if self._check_raw_data(raw_data):
            items = [dict(zip([key[0] for key in raw_data[1].description], row)) for row in raw_data[0]]
            self._close_all_resources(self._database, raw_data)
            if items == []:
                return None
            else:
                return items
        else:
            return None

