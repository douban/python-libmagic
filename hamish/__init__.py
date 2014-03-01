# -*- coding: utf-8 -*-
import os
import threading
import _magic

__version__ = '0.0.1'


def open(mime=False, magic_file=None,
         mime_encoding=False,
         keep_going=False):
    flags = _magic.MAGIC_NONE
    if mime:
        flags |= _magic.MAGIC_MIME_TYPE
    elif mime_encoding:
        flags |= _magic.MAGIC_MIME_ENCODING
    if keep_going:
        flags |= _magic.MAGIC_CONTINUE
    m = _magic.open(flags)
    if magic_file:
        m.load(magic_file)
    else:
        path = os.path.realpath(__file__).rsplit('/', 2)[0]
        path = os.path.join(path, 'misc', 'magic.mgc')
        m.load(path)
    return m


instances = threading.local()


def _get_magic_type(mime):
    i = instances.__dict__.get(mime)
    if i is None:
        i = instances.__dict__[mime] = open(mime=mime)
    return i


def from_file(filename, mime=False):
    """"
    Accepts a filename and returns the detected filetype.  Return
    value is the mimetype if mime=True, otherwise a human readable
    name.

    >>> magic.from_file("testdata/test.pdf", mime=True)
    'application/pdf'
    """
    m = _get_magic_type(mime)
    return m.from_file(filename)


def from_buffer(buffer, mime=False):
    """
    Accepts a binary string and returns the detected filetype.  Return
    value is the mimetype if mime=True, otherwise a human readable
    name.

    >>> magic.from_buffer(open("testdata/test.pdf").read(1024))
    'PDF document, version 1.2'
    """
    m = _get_magic_type(mime)
    return m.from_buffer(buffer)
