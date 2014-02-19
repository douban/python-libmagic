# file: magic.pxd

cdef extern from "magic.h":

    cdef struct magic_set:
        pass

    magic_set *magic_open(int)
    void magic_close(magic_set *)

    const char *magic_getpath(const char *, int)
    const char *magic_file(magic_set *, const char *)
    const char *magic_descriptor(magic_set *, int)
    const char *magic_buffer(magic_set *, const void *, size_t)

    const char *magic_error(magic_set *)
    int magic_setflags(magic_set *, int)

    int magic_version()
    int magic_load(magic_set *, const char *)
    int magic_compile(magic_set *, const char *)
    int magic_check(magic_set *, const char *)
    int magic_list(magic_set *, const char *)
    int magic_errno(magic_set *)
