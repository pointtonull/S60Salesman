#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
Smart interface for reading and writing dsv files.
"""

from DSV import DSV

class Data(object):
    def __init__(self, delimiter=None, qualifier=None, hasheader=None,
            quoteall=True, newline=None):
        self._delimiter = delimiter
        self._qualifier = qualifier
        self._hasheader = hasheader
        self._quoteall = quoteall
        self._newline = newline

    def fromfile(self, filename):
        data = open(filename).read()

        if self._newline is None:
            for posible in ("\r\n", "\n\r", "\n"):
                if posible in data:
                    self._newline = posible
                    data = data.replace(self._newline, "\n")
                    break
        else:
            data = data.replace(self._newline, "\n")

        if self._qualifier is None:
            self._qualifier = DSV.guessTextQualifier(data)

        data = DSV.organizeIntoLines(data, textQualifier=self._qualifier)

        if self._delimiter is None:
            self._delimiter = DSV.guessDelimiter(data)

        if self._hasheader is None:
            self._hasheader = DSV.guessHeaders(data)

        dsvlistoflists = DSV.importDSV(data, delimiter=self._delimiter,
            textQualifier=self._qualifier)

        columns = len(dsvlistoflists[0])
        if self._hasheader:
            header = dsvlistoflists.pop(0)
        else:
            header = range(1, columns + 1)

        dsvlistofdicts = []
        for row in dsvlistoflists:
            mapped_row = {}
            for column in xrange(columns):
                mapped_row[header[column]] = row[column]
            dsvlistofdicts.append(mapped_row)

        return dsvlistofdicts


    def tofile(self, filename, data, columns_order=None):
        """
        Data is a list of dicts as Data.fromfile returns.

        If columns order if given that will be the used order. else will be
        used the dict order (almos random).

        """

        if columns_order:
            headers = columns_order
        else:
            headers = data[0].keys()

        listoflists = []
        listoflists.append(headers)
        for dictrow in data:
            listrow = []
            for key in headers:
                listrow.append(dictrow[key])
            listoflists.append(listrow)

        asstring = DSV.exportDSV(listoflists, self._delimiter, self._qualifier,
            self._quoteall) 

        file = open(filename, "w")
        file.write(asstring)
        file.close()

        return filename


if __name__ == "__main__":
    data = Data()
    clientes = data.fromfile("../input/clientes.csv")
    print(clientes)

    header = ["COD_CLI", "NRO_ZON", "APNBR_CLI"]
    print(data.tofile("../output/prueba.csv", clientes, header))
