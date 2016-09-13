"""
This module provides a class designed to read from a compressed j__data file output from PADDI.
"""
from libc.stdlib cimport malloc, free
import numpy as np
import netCDF4 as nc

cimport numpy as np

cimport jutils


cdef class CompressedFile(object):
	"""
	This context manager is used to more conveniently read the compressed data files. The syntax is usually as follows::

		with CompressedFile(file_name) as file:
			while (True):
				# Read each compressed entry
				magic, data, iteration, time, dt = file.read()

	:type file_name: :class:`str`
	:param file_name: The name of the file to read from
	:type clen: :class:`int`
	:param clen: The number of characters in a string in the compressed file
	"""
	# The list of fortran file identifiers in use
	ius = [0]

	# Some declarations for cython
	cdef int iu
	cdef int numx
	cdef int numy
	cdef int numz

	cdef char* file_name
	cdef int clen
	cdef int previous
	cdef int index

	# For speed, use a memoryview
	cdef float[:,:,:,:] temp_data

	def __init__(self, file_name, clen=20):
		bytes = file_name.encode()
		self.file_name = bytes
		self.clen = clen
		self.previous = -1
		self.index = -1

	def __enter__(self):
		"""
		Open the file, returning this object as a handle

		:rtype: :class:`CompressedFile`
		:return: This object as a handle to the file
		"""
		global temp_data

		self.iu = 0

		# Declare variables for cython
		cdef int npde
		cdef int ninfo = 10

		cdef float[10] finfo
		string = (" "*self.clen*10).encode()
		cdef char* cinfo = string

		# Find an unused fortran file id
		while self.iu in CompressedFile.ius:
			self.iu += 1

		CompressedFile.ius.append(int(self.iu))

		# Try opening the file
		ierr = jutils.jcopen(self.iu, jutils.JC3D, self.file_name, "r")

		if ierr < 0:
			raise FileNotFoundError()

		# Read off the information to get the shape of the array
		jutils.jcrinfo2_(&self.iu, &self.numx, &self.numy, &self.numz, &npde, &ninfo, finfo, cinfo, self.clen)

		# Allocate the memory for the memoryview
		self.temp_data = np.ascontiguousarray(np.empty((1,) + self.shape(), dtype=np.float32))

		return self

	def __exit__(self, type, value, traceback):
		"""
		Exit the context manager with the usual parameters
		"""
		jutils.jcclose(self.iu)

		index = CompressedFile.ius.index(self.iu)
		CompressedFile.ius.pop(index)

	def shape(self):
		"""
		Return the shape of the compressed data as (z, x, y)

		:rtype: :class:`tuple` of :class:`int`
		:return: The shape of the compressed data
		"""
		return (self.numz, self.numx, self.numy)

	def read(self):
		"""
		Read one compressed entry from the file, using the jutils package.

		:rtype: :class:`int`, :class:`numpy.memoryview`, :class:`int`, :class:`float`, :class:`float`
		:return: The magic number identifier for the entry, the memoryview to the data, the timestep number from the run, the time at that timestep, the timestep duration at that timestep
		"""
		# Declare the inputs and outputs for cython
		cdef int numx = self.numx
		cdef int numy = self.numy
		cdef int numz = self.numz

		cdef int iteration
		cdef float time
		cdef float dt

		# Use the jutils jcread script to read the compressed data entry
		magic = jutils.jcread(self.iu, &iteration, &time, &dt, &self.temp_data[0,0,0,0], &self.numx, &self.numy, &self.numz)

		# If magic is less than zero, we've reached the end of the file (or there's been an error)
		if magic < 0:
			raise EOFError("End of file")

		return magic, self.temp_data, iteration, time, dt

class CompressedData(object):
	"""
	An object designed to read a series of compressed output files from PADDI and extract data from them. Note that in general, these files are too large to read into memory, so the best way to access these results are to use the :func:`CompressedData.to_netcdf` method to convert the compressed data to a netcdf file, which can then be accessed as normal.

	:type files: :class:`list` of :class:`str`
	:param files: A collection of file names to be read in order
	:type format: :class:`dict` with :class:`int` keys and :class:`str` values
	:param format: A format to use to translate the integer "magic" numbers from jutils to a string; if `None`, instead use :attr:`CompressedData.default_format`
	"""
	default_format = {jutils.JPTEMP: "Temp",
					  jutils.JPCHEM: "Chem",
					  jutils.JPVELX: "ux",
					  jutils.JPVELY: "uy",
					  jutils.JPVELZ: "uz",
					  jutils.JPBX: "vortx",
					  jutils.JPBY: "vorty",
					  jutils.JPBZ: "vortz"}
	"""A default format to use for converting jutils "magic" numbers to strings. This can be overridden."""

	def __init__(self, files, format=None):
		# Use default format if one is not provided
		if format is None:
			format = CompressedData.default_format

		# Get the shape of the data, and check whether files is a single file or a list of files
		self.shape = None
		try:
			with CompressedFile(files[0]) as file:
				self.shape = file.shape()
		except FileNotFoundError:
			files = [files]
			with CompressedFile(files[0]) as file:
				self.shape = file.shape()			

		self.format = format
		self.files = files

	def extract_modes(self, *args):
		"""
		Extract the modes of the simulation. Note that these modes should be specified as (n, m, l), where l is the positive integer x-directional mode number, and m and n are the (not necessarily positive) integer y- and z-directional mode numbers. This is to be consistent with PADDI's choice of the "real" axis when taking the FFT.

		:type args: :class:`tuple` of 3 :class:`int`
		:param args: Any number of triples that can represent modes; note that a negative x mode number will index backwards as usual and so will correspond to a high spatial frequency

		:rtype: :class:`dict` with :class:`str` keys and :class:`dict` values with :class:`tuple` of 3 :class:`int` keys and :class:`list` of :class:`complex` values
		:return: A dictionary, keyed by the string representation of the field, whose values are themselves dictionaries that have mode number tuple keys and time series values of the complex amplitudes of those modes
		"""
		modes = {}

		# Iterate over the files
		for file_name in self.files:
			try:
				with CompressedFile(file_name) as file:
					while (True):
						# Read each compressed entry
						magic, data, iteration, time, dt = file.read()

						# Perform the fft, using the last axis as the "real" axis
						data = np.fft.rfftn(np.asarray(data) / (data.shape[1]) / (data.shape[2]) / (data.shape[3]))

						# Iterate over the modes and extract the relevant ones to return
						for mode in args:
							if self.format[magic] not in modes:
								modes[self.format[magic]] = {}
							if mode not in modes[self.format[magic]]:
								modes[self.format[magic]][mode] = []
							modes[self.format[magic]][mode].append(data[(0,) + mode])

			except EOFError:
				pass

		return modes

	def to_netcdf(self, *args, **kwargs):
		"""
		Convert the compressed data into a netcdf file (effectively, use this to reconstruct a lower resolution simdat file). This method can also be used to easily "uncompress" the file, but this is not recommended as it is likely to be quite large.

		:param args: Passed to :class:`netCDF4.Dataset` constructor
		:param kwargs: Passed to :class:`netCDF4.Dataset` constructor

		:rtype: :class:`netCDF4.Dataset`
		:return: The netcdf file object associated with the newly created file
		"""
		# Construct the dataset
		obj = nc.Dataset(mode="w", *args, **kwargs)

		# Create the dimensions
		time = obj.createDimension("time", None)
		z = obj.createDimension("Z", self.shape[0])
		y = obj.createDimension("Y", self.shape[2])
		x = obj.createDimension("X", self.shape[1])

		# Add a variable for each key in the format
		for key in self.format:
			obj.createVariable(self.format[key], "f4", ("time", "Z", "Y", "X"))

		# Iterate over the files
		prev_iteration = None
		index = -1
		for file_name in self.files:
			try:
				with CompressedFile(file_name) as file:
					while (True):
						# Read each compressed entry
						magic, data, iteration, time, dt = file.read()

						# If the iteration increases, increase the index
						if iteration != prev_iteration:
							prev_iteration = iteration
							index += 1

						# Record the data
						obj[self.format[magic]][file.index] = np.asarray(data)
			except EOFError:
				pass

		return obj

