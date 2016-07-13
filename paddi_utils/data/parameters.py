import numpy as np
import f90nml

class Parameters(object):
    """
    Read the parameter information for the a PADDI run

    :type format: :class:`list` of :class:`tuple` of the form (:class:`str`, :class:`type`)
    :param format: The parameter--type pairs of the data to be contained within the Parameters object; if `None`, instead use :attr:`Parameters.default_format`
    :param kwargs: A dictionary containing parameter--value pairs
    """

    default_format = [("thermal_buoyancy_param", np.float),
                      ("compositional_buoyancy_param", np.float),
                      ("viscous_diffusion_coeff", np.float),
                      ("thermal_diffusion_coeff", np.float),
                      ("compositional_diffusion_coeff", np.float),
                      ("thermal_stratif_param", np.float),
                      ("compositional_stratif_param", np.float),
                      ("x_extent_of_the_box", np.float),
                      ("y_extent_of_the_box", np.float),
                      ("z_extent_of_the_box", np.float),
                      ("cfl_safety_factor", np.float),
                      ("maximum_time_step_length", np.float),
                      ("initial_time_step_length", np.float),
                      ("max_degree_of_x_fourier_modes", np.int),
                      ("max_degree_of_y_fourier_modes", np.int),
                      ("max_degree_of_z_fourier_modes", np.int),
                      ("nx", np.int),
                      ("ny", np.int),
                      ("nz", np.int),
                      ("number_of_tasks_1st_transpose", np.int),
                      ("number_of_tasks_2nd_transpose", np.int),
                      ("istep", np.int),
                      ("dt", np.float),
                      ("time", np.float)]
    """A default format for PADDI runs; this can be overloaded if needed"""

    nc_format = [("thermal_buoyancy_param", np.float),
                 ("compositional_buoyancy_param", np.float),
                 ("viscous_diffusion_coeff", np.float),
                 ("thermal_diffusion_coeff", np.float),
                 ("compositional_diffusion_coeff", np.float),
                 ("thermal_stratif_param", np.float),
                 ("compositional_stratif_param", np.float),
                 ("x_extent_of_the_box", np.float),
                 ("y_extent_of_the_box", np.float),
                 ("z_extent_of_the_box", np.float),
                 ("istep", np.int),
                 ("dt", np.float),
                 ("time", np.float)]
    """A default format for reading netcdf files; this can be overloaded if needed"""

    param_translation = {"x_extent_of_the_box": "Gammax",
                         "y_extent_of_the_box": "Gammay",
                         "z_extent_of_the_box": "Gammaz",
                         "thermal_buoyancy_param": "B_therm",
                         "compositional_buoyancy_param": "B_comp",
                         "viscous_diffusion_coeff": "D_visc",
                         "thermal_diffusion_coeff": "D_therm",
                         "compositional_diffusion_coeff": "D_comp",
                         "thermal_stratif_param": "S_therm",
                         "compositional_stratif_param": "S_comp",
                         "istep": "istep",
                         "time": "time",
                         "dt": "dt"}
    """A dictionary that translates from the parameter names in the parameter file (keys) and the names in the netCDF files (values)"""

    def __init__(self, format=None, **kwargs):
        if format is None:
            format = Parameters.default_format

        super(Parameters, self).__init__()
        self.format = format

        self.istep = 0
        self.dt = 0.0
        self.time = 0.0

        for key in kwargs:
            setattr(self, key, kwargs[key])

        factor = 3
        if "dealias" in kwargs:
            if not kwargs["dealias"]:
                factor = 4

        for direction in ["x", "y", "z"]:
            if "n" + direction not in kwargs:
                setattr(self, "n" + direction, kwargs["max_degree_of_%s_fourier_modes" % direction] * factor)

        for key, type in format:
            try:
                getattr(self, key)
            except AttributeError:
                raise RuntimeError("Parameters not initialized correctly, missing %s" % key)

    @classmethod
    def from_header(cls, file_name, format=None, skip=12):
        """
        Generate a :class:`Parameters` object from the header of the ASCII file given. The first skip lines are ignored, and the next lines will be read until each entry in format is filled. The parameter value is assumed to be the last entry after :func:`~str.split` is called on the line.

        :type file_name: :class:`str`
        :param file_name: The name of the ASCII file from which the header should be read
        :type format: :class:`list` of :class:`tuple` of the form (:class:`str`, :class:`type`)
        :param format: The parameter--type pairs of the data to be contained within the Parameters object; if `None`, instead use :attr:`Parameters.default_format`
        :type skip: :class:`int`
        :param skip: The number of lines that should be skipped at the start of the file

        :return type: :class:`Parameters`
        :return: An instance of the Parameters class built from the ASCII header
        """
        if format is None:
            format = default_format

        # Read the file, skipping the first skip lines
        file = open(file_name, "r")
        strings = [file.readline() for i in range(skip + len(format))][skip:]

        # Set the parameters sequentially based on the contents of the file header
        params = {}
        for line, (key, dtype) in zip(strings, format):
            params[key] = dtype(line.split()[-1])

        return cls(format=format, **params)

    @classmethod
    def from_file(cls, file_name, format=None):
        """
        Generate a :class:`Parameters` object from a namelist file

        :type file_name: :class:`str`
        :param file_name: The name of the namelist file from which the header should be read
        :type format: :class:`list` of :class:`tuple` of the form (:class:`str`, :class:`type`)
        :param format: The parameter--type pairs of the data to be contained within the Parameters object; if `None`, instead use :attr:`Parameters.default_format`

        :return type: :class:`Parameters`
        :return: An instance of the Parameters class built from the namelist file
        """
        if format is None:
            format = cls.default_format

        file = open(file_name, "r")
        params = f90nml.read(file)["input_values"]

        return cls(format=format, **params)

    @classmethod
    def from_nc(cls, dataset, format=None, translation=None):
        """
        Generate a :class:`Parameters` object from a given netCDF file.

        :type file_name: :class:`str`
        :param file_name: The name of the netCDF file from which the header should be read
        :type format: :class:`list` of :class:`tuple` of the form (:class:`str`, :class:`type`)
        :param format: The parameter--type pairs of the data to be contained within the Parameters object; if `None`, instead use :attr:`Parameters.nc_format`
        :type translation: :class:`dict` of :class:`str` with :class:`str` as keys
        :param translation: The dictionary used to translate the variables in the netCDF file to parameter names for the :class:`Parameters` class with netCDF parameter names as values; if `None`, use :attr:`Parameters.param_translation`

        :return type: :class:`Parameters`
        :return: An instance of the Parameters class build from the netCDF file
        """
        if format is None:
            format = cls.nc_format

        if translation is None:
            translation = cls.param_translation

        params = {}
        for key, dtype in format:
            if key in Parameters.param_translation:
                params[key] = dataset[cls.param_translation[key]][:]
            else:
                params[key] = dataset[key][:]

        # A few paramaters tend to be mising in the netCDF files, but they can be filled in
        params["max_degree_of_x_fourier_modes"] = dataset.dimensions["l"].size - 1
        params["max_degree_of_y_fourier_modes"] = dataset.dimensions["m"].size // 2
        params["max_degree_of_z_fourier_modes"] = dataset.dimensions["n"].size // 2

        params["nx"] = (dataset.dimensions["l"].size - 1) * 2
        params["ny"] = dataset.dimensions["m"].size
        params["nz"] = dataset.dimensions["n"].size

        params["cfl_safety_factor"] = 0.0
        params["maximum_time_step_length"] = 0.0
        params["initial_time_step_length"] = 0.0
        params["number_of_tasks_1st_transpose"] = 0
        params["number_of_tasks_2nd_transpose"] = 0
        
        return cls(format=cls.default_format, **params)

    def __iter__(self):
        """
        Iterate over the format, giving parameter--type pairs

        :return type: :class:`iter`
        :return: An iterator over the parameter--type tuple pairs
        """
        return iter(self.format)
