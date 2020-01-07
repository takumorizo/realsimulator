#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ReadCollector(object):
    """docstring for ReadCollector"""
    def __init__(self):
        super(ReadCollector, self).__init__()
        self.__reads_dic   = {}
        self.__unique_id   = 0

    def __len__(self):
        return len(self.__reads_dic)

    def __contains__(self, ID):
        return (ID in self.__reads_dic)

    def __getitem__(self, ID):
        if ID not in self.__reads_dic:
            return (-1, [])
        else:
            return self.__reads_dic[ID]

    def __repr__(self):
        return str(self.__reads_dic)

    def push(self, read, id_editor = None):
        if id_editor is not None:
            ID =  id_editor(read.query_name)
        else:
            ID =  read.query_name

        if ID not in self.__reads_dic:
            self.__reads_dic[ID] = (self.__unique_id, [read])
        else:
            self.__reads_dic[ID][1].append(read)
        self.__unique_id += 1

    def clear(self, clear_unique_id = False):
        self.__reads_dic = {}
        if clear_unique_id:
            self.__unique_id = 0

    def __iter__(self):
        return self.__reads_dic.iteritems()
