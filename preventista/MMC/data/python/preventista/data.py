import e32db


"""
Dbms:
    begin() Begins a transaction on the database. 
    rollback() Rolls back the current transaction. 
    commit() Commits the current transaction. 

    compact() Compacts the database, reclaiming unused space in the database
        file. 
    create(dbname) Creates a database with path dbname. 
"""

class Data_manager(object):
    def __init__(self, dbfile):
        """
        Open a the database on dbfile. If dbfile does not exists try to create
        a new database and open that.
        """
        self.db_object = e32db.Dbms()
        self.db_view = e32db.Db_view()

        try:
            self.db_object.open(unicode(debfile))
        except:
            self.db_object.create(unicode(debfile))
            self.db_object.open(debfile)

        self._changes = 0


    def _get_row(self):
        """
        Returns the current row.
        """
        # TODO: Try to return a dict?
        self.db_view.get_line()
        row = []
        for i in xrange(self.db_view.col_count()):
            try:
                row.append(self.db_view.col(i + 1))
            except:
                row.append(None)
        return row


    def query_first(self, statement):
        """
        Executes a query and retrieve the first resulting row.
        """
        self.db_view.prepare(self.db_object, unicode(statement))
        self.db_view.first_line()
        return self._get_row()


    def query_all(self, statement):
        """
        Executes a query and returns a rows generator that will iterate all
        the result rows.
        """
        self.db_view.prepare(self.db_object, unicode(statement))
        self.db_view.first_line()

        for i in xrange(self.db_view.count_line()):
            yield self._get_row()
            self.db_view.next_line()


    def close(self):
        """
        Close the database. Will compact the file in any change were made.
        """
        if self_changes:
            self.db_object.compact()
        return self.db_object.close()


    def execute(self, statement):
        """
        Executes a SQL Query.
        Returns:
            On SQL Schema Update:
                0 if success
            On SQL Data Update:
                The number of rows inserted, updated or deleted
        """

        self._changes += 1
        return self.db_object.execute(statement)



def main():
    from random import randrange

    dbfile = r"e:\prueba.db"
    data = Data_manager(dbfile)
    sql_create = (u"CREATE TABLE bookmarks (id COUNTER, url VARCHAR,"
        u"score UNSIGNED TINYINT)")
    data.execute(sql_create)

    for url in ("http://google.com", "http://dealextreme.com",
            "http://saltalug.org.ar"):
        score = randrange(1, 6)
        sql_add = "INSERT INTO bookmarks (url, score) VALUES ('%s',%d)" % (
            url, score)
        data.execute(sql_add)

    data.close()

    data = Data_manager(dbfile)
    print("First: %s" % data.query_first('SELECT * FROM bookmarks'))
    print("All:")
    for row in data.query_all('SELECT * FROM bookmarks'):
        print("    %s" % row)

    print("Deleting all urls with score == 1")

    data.execute(u"DELETE FROM bookmarks WHERE score == 1")
    data.close()
