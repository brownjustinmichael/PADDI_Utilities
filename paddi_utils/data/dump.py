import numpy as np
import netCDF4 as nc

from paddi_utils.data.diagnostic import Parameters

class Dump(nc.Dataset):
	"""
	A representation of a PADDI dumpfile that is editable
	
	:type parameters: :class:`parameters.Parameters`
	:param parameters: The input parameters to initiate a new dump file (raises a RuntimeError if this does not match those in an existing file, if provided)
	:type file_name: :class:`str`
	:param file_name: The name of the file to open; if `None`, instead use `parameters.name_of_input_restart_file`
	:type mode: :class:`str`
	:param mode: "r" to read, "w" to write, or "a" to edit
	:param args: Passed to :class:`nc.Dataset` constructor
	:param kwargs: Passed to :class:`nc.Dataset` constructor
	"""

	def __init__(self, parameters, file_name=None, mode="w", *args, **kwargs):
		if file_name is None:
			file_name = parameters.name_of_input_restart_file

		super(Dump, self).__init__(file_name, mode=mode, format="NETCDF3_64BIT", *args, **kwargs)

		if mode is "w":
			kx = self.createDimension("l", parameters["max_degree_of_x_fourier_modes"] + 1)
			ky = self.createDimension("m", parameters["max_degree_of_y_fourier_modes"] * 2)
			kz = self.createDimension("n", parameters["max_degree_of_z_fourier_modes"] * 2)
			ri = self.createDimension("ri", 2)

			for parameter in parameters:
				dtypes = [dtype for name, dtype in parameters.format if name == parameter]
				if len(dtypes) > 0:
					dtype = dtypes[0]
				else:
					dtype = type(parameters[parameter])

				if parameter in parameters.param_translation:
					parameter = parameters.param_translation[parameter]

				if dtype is int:
					self.createVariable(parameter, "i4", tuple())
				elif dtype is float:
					self.createVariable(parameter, "f8", tuple())
				else:
					print("WARNING: Unknown datatype %s for %s, skipping" % (str(dtype), parameter))
					continue

				self[parameter][:] = parameters[parameter]

			self.createVariable("kx", "f8", ("l",))
			kx0 = 2.0 * np.pi / self["Gammax"][:]
			self["kx"][:] = np.arange(0.0, kx0 * kx.size, kx0)

			self.createVariable("ky", "f8", ("m",))
			ky0 = 2.0 * np.pi / self["Gammay"][:]
			self["ky"][:ky.size // 2 + 1] = np.arange(0.0, ky0 * (ky.size // 2 + 1), ky0)
			self["ky"][ky.size // 2 + 1:] = ky0 * np.array(range(-(ky.size // 2 - 1), 0))
			
			self.createVariable("kz", "f8", ("n",))
			kz0 = 2.0 * np.pi / self["Gammaz"][:]
			self["kz"][:kz.size // 2 + 1] = np.arange(0.0, kz0 * (kz.size // 2 + 1), kz0)
			self["kz"][kz.size // 2 + 1:] = kz0 * np.array(range(-(kz.size // 2 - 1), 0))

			self.createVariable("ri", "i4", ("ri",))
			self["ri"][:] = [0, 1]

			for var in ["Chem", "Temp", "ux", "uy", "uz"]:
				self.createVariable(var, "f8", ("m", "l", "n", "ri"))
		else:
			for parameter in parameters:
				if parameter in Parameters.param_translation:
					if self[Parameters.param_translation[parameter]][:] != parameters[parameter]:
						raise RuntimeError("Parameter mismatch in dump file construction")

	@classmethod
	def from_file(cls, file_name):
		data = nc.Dataset(file_name)

		parameters = Parameters.from_nc(data)

		obj = cls(parameters, file_name=file_name, mode="a")

		for key in data.variables:
			obj[key][:] = data[key][:]

		return obj