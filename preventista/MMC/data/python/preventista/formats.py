#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from time import localtime, strftime, strptime
from calendar import timegm
from debug import debug

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR 
WEEK = 7 * DAY

class Date(float):
    def __new__(cls, datetime):
        if isinstance(datetime, basestring):
            if u"-" in datetime:
                date_float = timegm(strptime(datetime, "%Y-%m-%d"))
            else:
                date_float = timegm(strptime(datetime, "%d/%m/%Y"))
        else:
            date_float = datetime

        debug("formats:Date:__new__::datetime: %s" % datetime)
        newdate = float.__new__(cls, date_float)
        return newdate

    def __init__(self, datetime):
        """
            number:    the date number / date string
        """

    def __rep__(self):
        return strftime("%d/%m/%Y", localtime(self))

    def __str__(self):
        return self.__rep__()



class Number(float):

    def __new__(cls, number, thosep="", decsep=",", decqua=2):
        if isinstance(number, basestring):
            number = number.replace(thosep, "")
            number = number.replace(decsep, ".")
        number = float.__new__(cls, number)
        number._thosep = thosep
        number._decsep = decsep
        number._decqua = decqua
        return number

    def __init__(self, number, thosep="", decsep=",", decqua=2):
        """
            number:     the float number
            thosep:     the symbol to mark shousands
            decsep:     the symbol to mark the end of the integer part
            decqua:     if int forces zero filling
        """

    def __rep__(self):
        number = round(self, self._decqua)
        fmstr = u"%%i%s%%s" % self._decsep
        string = fmstr % (number, decimals(number, self._decqua))
        return string

    def __str__(self):
        return self.__rep__()


def decimals(number, amount):
    alldecimals = str(round(number - int(number), amount))[2:]
    alldecimals = alldecimals.ljust(amount).replace(" ", "0")
    return alldecimals[:amount]


def main():
    for n in [10.113456 ** i for i in xrange(10)]:
        print(n)
        print(Number(n, ".", ".", 2))

if __name__ == "__main__":
    exit(main())
