import csv
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
            self.db_object.open(dbfile)
        except:
            self.db_object.create(dbfile)
            self.db_object.open(dbfile)

        self._changes = 0


    def _get_row(self):
        """
        Returns the current row.
        """
        self.db_view.get_line()
        row = []
        for i in xrange(self.db_view.col_count()):
            try:
                row.append(self.db_view.col(i + 1))
            except TypeError:
                row.append(None)
        return tuple(row)


    def query_first(self, statement):
        """
        Executes a query and retrieve the first resulting row.
        """
        self.db_view.prepare(self.db_object, statement)
        self.db_view.first_line()
        return self._get_row()


    def query_all(self, statement):
        """
        Executes a query and returns a rows generator that will iterate all
        the result rows.
        """
        self.db_view.prepare(self.db_object, statement)
        self.db_view.first_line()

        for i in xrange(self.db_view.count_line()):
            yield self._get_row()
            self.db_view.next_line()


    def close(self):
        """
        Close the database. Will compact the file in any change were made.
        """
        if self._changes > 10:
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

        result = self.db_object.execute(statement)
        self._changes += 1
        return result


    def csv_import(self, csv_file, table_name):
        """
        Imports the values from csv_file to the given table.

            csv_file   : file-like object
            table_name : the destination table
        """

        reader = csv.reader(csv_file, delimiter=';', quoting=csv.QUOTE_ALL,
            quotechar="'")
        headers = reader.next()
        fields = ", ".join(headers)
        return


    def csv_export(self, csv_file, table_name, fields):
        """
        Export the values of the fields from table to the csv_file.

            csv_file   : file-like object
            table_name : source of data
            fields     : the columns names to be includeds
        """
        return



def main():
    from random import randrange

    dbfile = u"e:\\prueba.db"
    data = Data_manager(dbfile)
    sql_create = (u"""CREATE TABLE bookmarks (
            id COUNTER,
            url VARCHAR(40),
            score UNSIGNED TINYINT
        )""")

    try:
        data.execute(sql_create)
    except SymbianError, error:
        if "KErrAlreadyExists" in error:
            pass
        else:
            raise

    protocols = ("http://", "https://", "ftp://", "ftps://")
    prefixes = ("", "www.", "mirror.", "secure.")
    names = ("wikipedia", "google", "twitter", "debian", "fsf", "saltalug",
            "yahoo", "amazon", "terra", "ding", "facebook")
    clases = ("", "org", ".com", ".net", ".gov", ".tur", ".tv")
    locations = ("", ".us", ".ar", ".uy", ".cl", ".ch", ".la", ".uk",
        ".es", ".bo", ".pe", ".co", ".ve")

    print("Trying to insert tons of regs to the database.")
    for protocol in protocols:
        for prefix in prefixes:
            for name in names:
                for clase in clases:
                    for location in locations:
                        url = "".join((protocol, prefix, name, clase, location))
                        score = randrange(1, 6)
                        sql_add = (u"INSERT INTO bookmarks (url, score)"
                            "VALUES ('%s', %d)" % (url, score))
                        data.execute(sql_add)
    data.close()

    data = Data_manager(dbfile)
    print("First: %s, %s" % tuple(data.query_first(
        u'SELECT url, score FROM bookmarks')))
    print("All:")
    counter = 0
    for row in data.query_all(u'SELECT url, score FROM bookmarks'):
        counter += 1
    print("    repasados %d registros" % counter)

    print("Deleting all urls with score < 3")

    data.execute(u"DELETE FROM bookmarks WHERE score < 3")
    data.close()

"""
BIT                 int
TINYINT             int
UNSIGNED TINYINT    int
SMALLINT            int     yes
UNSIGNED SMALLINT   int     yes
INTEGER     int     yes
UNSIGNED INTEGER     int     yes
COUNTER     te)     int     yes
BIGINT     long     yes
REAL     float     yes
FLOAT     EDbColReal64     float     yes
DOUBLE     EDbColReal64     float     yes
DOUBLE PRECISION     EDbColReal64     float     yes
DATE     EDbColDateTime     float

(or long, with col_rawtime()
    yes
TIME     EDbColDateTime     float

(or long, with col_rawtime()
    yes
TIMESTAMP     EDbColDateTime     float

(or long, with col_rawtime()
    yes
CHAR(n)     EDbColText     Unicode     yes
VARCHAR(n)     EDbColText     Unicode     yes
LONG VARCHAR     EDbColLongText     Unicode     yes
BINARY(n)     EDbColBinary     str     read only
VARBINARY(n)     EDbColBinary     str     read only
LONG VARBINARY     EDbColLongBinary     n/a     no
"""
