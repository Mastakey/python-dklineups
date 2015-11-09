#SQLite wrapper in python
import sqlite3

class SQ3Reader(object):
    def __init__(self, dbstr, config):
        self.dbcon = sqlite3.connect(dbstr)
        tableCursor = self.dbcon.cursor()
        self.tables = tableCursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        self.config = config
        self.debugLog("\n")

    def debugLog(self, string):
        if self.config['logging'] == "on":
            f = open("SQ3Reader.log", "a")
            f.write(string.encode('utf8'))
            f.write("\n")

    def getTables(self):
        return self.tables

    def printDB(self):
        for table in self.tables:
            infoCursor = self.dbcon.cursor()
            print (table)
            columns = infoCursor.execute("PRAGMA table_info("+table[0]+")")
            for column in columns:
                print (column)

    def executeQuery(self, query):
        cursor = self.dbcon.cursor()
        query = unicode(query)
        self.debugLog(query)
        values = cursor.execute(query)
        self.dbcon.commit()
        return values

    def executeQueryDict(self, query):
        cursor = self.dbcon.cursor()
        self.debugLog(query)
        results = cursor.execute(query)
        column_dict = {}
        result_list = []
        count = 0
        for columns in cursor.description:
            for column in columns:
                if column is not None:
                    column_dict[column] = count
                    count = count + 1
        for result in results:
            result_dict = {}
            for key in column_dict.keys():
                    result_dict[key] = result[column_dict[key]]
            result_list.append(result_dict)
        return result_list

    def close(self):
        self.dbcon.close()
