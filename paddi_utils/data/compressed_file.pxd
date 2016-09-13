cdef class CompressedFile:
	cdef int iu
	cdef int numx
	cdef int numy
	cdef int numz

	cdef char* file_name
	cdef int clen
	cdef public int read(self, float*)