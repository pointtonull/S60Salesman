#!/usr/bin/env python
#-*- coding: UTF-8 -*-

def uniq(iterable):
    uniq_list = []
    for item in iterable:
        if item not in uniq_list:
            uniq_list.append(item)
    return uniq_list


def sorted(iterable):
    olist = list(iterable)
    olist.sort()
    return olist

def main():
    pass

if __name__ == "__main__":
    exit(main())
