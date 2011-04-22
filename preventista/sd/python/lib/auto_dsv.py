#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from DSV import DSV

def import_dsv(filename):
    data = open(filename).read()
    data = data.replace("\r\n", "\n")
    qualifier = DSV.guessTextQualifier(data)
    data = DSV.organizeIntoLines(data, textQualifier=qualifier)
    delimiter = DSV.guessDelimiter(data)
    data = DSV.importDSV(data, delimiter=delimiter, textQualifier=qualifier)

    hasheader = DSV.guessHeaders(data)

    columns = len(data[0])
    if hasheader:
        header = data.pop(0)
    else:
        header = range(1, columns + 1)

    dsv = []
    for row in data:
        mapped_row = {}
        for column in xrange(columns):
            mapped_row[header[column]] = row[column]
        dsv.append(mapped_row)

    return dsv


def main():
    pass

if __name__ == "__main__":
    exit(main())
