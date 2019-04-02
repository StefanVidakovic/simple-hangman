import sqlite3


class WordGenerator:

    def __init__(self, database, table):
        self.database = database
        self.table = table
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

    def getRandomWord(self):
        self.cursor.execute("SELECT * FROM '%s' ORDER BY RANDOM() LIMIT 1" %self.table)
        return self.cursor.fetchone()[0]
