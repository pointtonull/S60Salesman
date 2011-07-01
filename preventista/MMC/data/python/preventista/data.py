#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from debug import debug
from itertools import chain
import csv
import e32db
import re


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


    def query(self, statement):
        """
        Executes a query and returns a rows generator that will iterate all
        the result rows.
        """
        try:
            self.db_view.prepare(self.db_object, statement)
        except:
            debug("Query failed: %s" % statement)
            raise
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

        try:
            result = self.db_object.execute(statement)
        except SymbianError, error:
            debug("Error %s on: %s "% (error, statement))
            raise

        self._changes += 1
        return result


    def csv_import(self, csv_file, table_name):
        """
        Imports the values from csv_file to the given table.

            csv_file   : file-like object
            table_name : the destination table
        """

        reader = csv_reader(csv_file)

        headers = reader.next()
        fields = u", ".join(headers)

        prelist = []
        for i in xrange(20):
            try:
                prelist.append(reader.next())
            except StopIteration:
                break

        values_fmt = guest_type(prelist)

        for row in chain(prelist, reader):
            row = (escape(column) for column in row)
            values = values_fmt % tuple(row)
            values = values.decode("latin-1", "ignore")
            statement = u"INSERT INTO %s" % table_name
            statement += u" (%s)" % fields
            statement += u" VALUES (%s)" % values
            self.execute(statement)

        return True


    def csv_export(self, csv_file, statement):
        """
        Export the values of the fields from table to the csv_file.

            csv_file   : file-like object
            statement  : the select query to execute, if fields are explicit
                         headers will be included in csv file
        """
        query_regex = r"(?im)SELECT\s*([\w,\s]*?)\*?\s+FROM\s+?[\w,\s]+"
        query = re.search(query_regex, statement)
        assert query
        headers = [header.strip() 
            for header in query.group(1).upper().split(",")]

        if headers:
            csv_file.write("%s\n" % ";".join(headers))

        for row in self.query(statement):
            values = [u"'%s'" % value for value in row]
            line = u";".join(values) + u"\n"
            csv_file.write(line.encode("latin-1", "replace"))

        csv_file.flush()



def guest_type(rows):
    '''
    Some values rows --> formater string

    [
        ['224', '22', 'VIRGEN DE URJUPIÑA', '3.14159265', 'ACTIVO'],
        ['172', '23', 'ZULMA', '1.732050', 'ACTIVO']
    ]

    produces;
        u"""%s, %s, '%s', %s, '%s'"""
    '''

    types = (int, float, str)
    finaltypes = [list(types) for x in range(len(rows[0]))]
    for row in rows:
        for pos, value in enumerate(row):
            attempt = finaltypes[pos][0]
            try:
                attempt(value)
            except:
                del(finaltypes[pos][0])
                if not finaltypes[pos]:
                    debug("Error: guest_types: %s[%d]" % (row, pos))
                    assert finaltypes[pos]
                
    fmts = []
    type2fmt = {int: "%s", float: "%s", str: "'%s'"}
    for column in finaltypes:
        fmts.append(type2fmt[column[0]])

    return ", ".join(fmts)


def escape(value):
    """
    Try to escape special chars
    """
    specials = {
        r"'" : r"''"
    }
 
    if issubclass(type(value), list) or issubclass(type(value), tuple):
        return tuple((escape(item) for item in value))
    elif issubclass(type(value), int):
        value = "%d" % value
    elif issubclass(type(value), float):
        value = "%f" % value
    elif issubclass(type(value), basestring):
        pass
    else:
        raise ValueError(type(value))

    for especial, replacement in specials.iteritems():
        if especial in value:
            debug(value)
            value = value.replace(especial, replacement)
            debug(value)
    return value


def csv_reader(iterator):
    fields_re = r"(;|^)('?)(?P<value>.*?)\2(?=;|$)"
    for line in iterator:
        yield [field.group("value")
            for field in re.finditer(fields_re, line)]


def main():
    debug(u"Abriendo fichero de base de datos.")
    dbfile = ur"e:\data\movil\preventista.db"
    data = Data_manager(dbfile)

    debug(u"Intentando crear tabla clientes.")
    sql_create = (u"""CREATE TABLE clientes (
            COD_CLI INTEGER,
            NRO_ZON INTEGER,
            APNBR_CLI VARCHAR,
            DOM_PART_CLI VARCHAR,
            EST_CLI VARCHAR,
            CARACT_ZON VARCHAR
        )""")

    try:
        data.execute(sql_create)
    except SymbianError, error:
        if "KErrAlreadyExists" in error:
            debug(u"La tabla ya existe.")
        else:
            raise

    debug(u"Eliminando todos los registros")
    data.execute(u"DELETE FROM clientes")

    debug(u"Intentando importar los registros desde el csv a la tabla.")
    data.csv_import(open(r"e:\data\input\clientes.csv"), u"clientes")

    data = Data_manager(dbfile)
    debug(u"First: %s" % u', '.join((unicode(value)
        for value in data.query_first(u'SELECT * FROM clientes'))))
    debug(u"All:")
    counter = 0
    for row in data.query(u'SELECT * FROM clientes'):
        counter += 1
    debug(u"    repasados %d registros" % counter)

    debug(u"Exportando todos los registros a CSV con header")
    data.csv_export(open(r"e:\data\output\hclientes.csv", "w"),
        (u'SELECT COD_CLI, NRO_ZON, APNBR_CLI, DOM_PART_CLI, EST_CLI,'
         u'CARACT_ZON FROM clientes'))

    debug(u"Eliminando todos los registros con NRO_ZON != 18")
    data.execute(u"DELETE FROM clientes WHERE NRO_ZON <> 18")

    data.close()


"""
All types: int, float, long, str, unicode

    BIT                                     int        yes
    TINYINT                                 int        yes
    UNSIGNED           TINYINT              int        yes
    SMALLINT                                int        yes
    UNSIGNED           SMALLINT             int        yes
    INTEGER                                 int        yes
    UNSIGNED           INTEGER              int        yes
    COUNTER                                 int        yes
    BIGINT                                  long       yes
    REAL                                    float      yes
    FLOAT              EDbColReal64         float      yes
    DOUBLE             EDbColReal64         float      yes
    DOUBLE PRECISION   EDbColReal64         float      yes
    DATE               EDbColDateTime       float      yes
           with col_rawtime()               long       yes
    TIME               EDbColDateTime       float      yes
           with col_rawtime()               long       yes
    TIMESTAMP          EDbColDateTime       float      yes
           with col_rawtime()               long       yes
    CHAR(n)            EDbColText           Unicode    yes
    VARCHAR(n)         EDbColText           Unicode    yes
    LONG VARCHAR       EDbColLongText       Unicode    yes
    BINARY(n)          EDbColBinary         str        read only
    VARBINARY(n)       EDbColBinary         str        read only
    LONG VARBINARY     EDbColLongBinary     n/a        no

"""
