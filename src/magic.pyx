# file: magic.pyx

cimport cmagic

# Flag constants for open and setflags
MAGIC_NONE = NONE = 0
MAGIC_DEBUG = DEBUG = 1
MAGIC_SYMLINK = SYMLINK = 2
MAGIC_COMPRESS = COMPRESS = 4
MAGIC_DEVICES = DEVICES = 8
MAGIC_MIME_TYPE = MIME_TYPE = 16
MAGIC_CONTINUE = CONTINUE = 32
MAGIC_CHECK = CHECK = 64
MAGIC_PRESERVE_ATIME = PRESERVE_ATIME = 128
MAGIC_RAW = RAW = 256
MAGIC_ERROR = ERROR = 512
MAGIC_MIME_ENCODING = MIME_ENCODING = 1024
MAGIC_MIME = MIME = 1040
MAGIC_APPLE = APPLE = 2048

MAGIC_NO_CHECK_COMPRESS = NO_CHECK_COMPRESS = 4096
MAGIC_NO_CHECK_TAR = NO_CHECK_TAR = 8192
MAGIC_NO_CHECK_SOFT = NO_CHECK_SOFT = 16384
MAGIC_NO_CHECK_APPTYPE = NO_CHECK_APPTYPE = 32768
MAGIC_NO_CHECK_ELF = NO_CHECK_ELF = 65536
MAGIC_NO_CHECK_TEXT = NO_CHECK_TEXT = 131072
MAGIC_NO_CHECK_CDF = NO_CHECK_CDF = 262144
MAGIC_NO_CHECK_TOKENS = NO_CHECK_TOKENS = 1048576
MAGIC_NO_CHECK_ENCODING = NO_CHECK_ENCODING = 2097152

MAGIC_NO_CHECK_BUILTIN = NO_CHECK_BUILTIN = 4173824


cdef class Magic:

    cdef cmagic.magic_set * _c_magic_t

    def __cinit__(self):
        self._c_magic_t = NULL

    cdef open(self, int flags):
        self._c_magic_t = cmagic.magic_open(flags)
        cmagic.magic_load(self._c_magic_t, NULL)

    cdef load(self, char *path):
        cmagic.magic_load(self._c_magic_t, path)

    def from_buffer(self, object buf):
        """
        Returns a textual description of the contents of the argument passed
        as a buffer or None if an error occurred and the MAGIC_ERROR flag
        is set. A call to errno() will return the numeric error code.
        """
        cdef size_t c_buf_len = len(buf)
        cdef const char * c_buf = buf
        cdef const char * r = NULL
        r = cmagic.magic_buffer(self._c_magic_t, c_buf, c_buf_len)
        if r is not NULL:
            try: # attempt python3 approach first
                return str(r, 'utf-8')
            except:
                return r

    def __dealloc__(self):
        if self._c_magic_t is not NULL:
            cmagic.magic_close(self._c_magic_t)


def open(flags):
    magic = Magic()
    magic.open(flags)
    return magic
