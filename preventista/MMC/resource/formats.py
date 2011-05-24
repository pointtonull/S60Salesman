#!/usr/bin/env python
#-*- coding: UTF-8 -*-

class Number(float):

    def __new__(cls, number, thosep="", decsep=",", decqua=2):
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
        fmstr = "%%i%s%%s" % self._decsep
        string = fmstr % (number, decimals(number, self._decqua))
        return string

    def __str__(self):
        return self.__rep__()


def decimals(number, amount):
    alldecimals = str(round(number - int(number), amount))[2:]
    alldecimals = alldecimals.ljust(amount, "0")
    return alldecimals[:amount]


def main():
    for n in [10.113456 ** i for i in xrange(10)]:
        print(n)
        print(Number(n, ".", "."))
        print(Number(n, ".", ".", 2))

if __name__ == "__main__":
    exit(main())