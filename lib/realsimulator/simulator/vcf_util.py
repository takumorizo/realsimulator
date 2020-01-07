#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import distutils.util

def get_pyvcf_attribute(obj, attributes, start = 0, sep = '/'):
    if not isinstance(attributes, list) and start == 0:
        attributes = re.split(sep, attributes)
        return get_pyvcf_attribute(obj, attributes, start = 0, sep = '/')

    N = len(attributes)
    if   N - start <= 0:
        raise Exception("No attribute specified.")
    elif N - start == 1:
        first_attribute = attributes[start]
        if first_attribute in obj:
            return obj[first_attribute]
        else:
            return getattr(obj, first_attribute)
    elif N - start >  1:
        first_attribute = attributes[start]
        return get_pyvcf_attribute(get_pyvcf_attribute(obj, [first_attribute]), attributes, start = start + 1, sep = sep)

def hasing_record(record):
    return'/'.join(map(str, [record.CHROM, record.POS, record.ID, record.REF, record.ALT]))

def vcf_type_convertion(elem, type_string):
    if   type_string.lower() == 'integer':
        elem = int(elem)
    elif type_string.lower() == 'float':
        elem = float(elem)
    elif type_string.lower() == 'flag':
        elem = distutils.util.strtobool(elem)
    elif type_string.lower() == 'string':
        elem = elem
    return elem
