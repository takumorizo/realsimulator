#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pysam
import contextlib

class BamReader(object):
    """docstring for BamReader"""
    def __init__(self):
        super(BamReader, self).__init__()
        self.__pysam_bam       = None
        self.__pysam_reads     = None
        self.__prepared        = False
        self.__searching       = False
        self.__within_interval = True
        self.__use_unmapped    = True
        self.__Chr   = None
        self.__start = None
        self.__end   = None
        self.__f     = None
        self.__F     = None

    @property
    def bam(self):
        return self.__pysam_bam

    def __iter__(self):
        return self

    def next(self):
        if not self.__prepared:
            raise Exception("Bam file not prepared.")
        if not self.__searching:
            raise Exception("Non searching reads.")
        read = self.__pysam_reads.next()
        while not self.__is_read_proper(read, self.__f, self.__F, self.__Chr, self.__start, self.__end, self.__use_unmapped):
            read = self.__pysam_reads.next()
        return read

    def __is_read_proper(self, read, f, F, Chr, start, end, use_unmapped):
        pass_filter = (read.flag & f) == f and (read.flag & F) == 0
        pass_interval = (not self.__within_interval) or self.__within_region(read, Chr, start, end, use_unmapped = use_unmapped)

        return pass_filter and pass_interval

    @contextlib.contextmanager
    def prepare(self, bam_path):
        try:
            self.open(bam_path)
            yield
        finally:
            self.close()

    def open(self, bam_path):
        self.__pysam_bam = pysam.AlignmentFile(bam_path, 'rb')
        self.__prepared = True

    def close(self):
        self.__pysam_bam.close()
        self.__pysam_bam = None
        self.__prepared = False

    def search(self, Chr, start, end, f_flag = 2, F_flag = 3840, within = True, use_unmapped = True):
        assert ((start is None) ^ (end is None)) == False

        if not self.__prepared:
            raise Exception("Bam file not prepared.")

        self.__searching  = True
        self.__within_interval = within
        self.__use_unmapped    = use_unmapped
        self.__Chr   = Chr
        if start is not None and end is not None:
            self.__start = max(start, 0)
            self.__end   = min(max(end, 0), self.__pysam_bam.lengths[self.__pysam_bam.get_tid(Chr)])
        else:
            self.__start = 0
            self.__end   = self.__pysam_bam.lengths[self.__pysam_bam.get_tid(Chr)]

        self.__f     = f_flag
        self.__F     = F_flag
        self.__pysam_reads = self.__pysam_bam.fetch(Chr, self.__start, self.__end)
        return self

    ## more control is needed
    def __within_region(self, read, Chr, start, end, use_unmapped = True):
        if read.cigarstring is None:
            return use_unmapped
        else:
            is_same_chr = (Chr == self.__pysam_bam.header['SQ'][read.reference_id]['SN'])
            # sys.stderr.writelines("start, read.reference_start, read.infer_query_length(): " + str( (start, read.reference_start, read.infer_query_length()) ) + '\n')
            # sys.stderr.writelines("read:  " + str( read ) + '\n')
            is_pos_in   = (start <= read.reference_start) and (read.reference_start + read.infer_query_length() <= end)
            return is_same_chr and is_pos_in

