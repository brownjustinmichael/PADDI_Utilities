from io import StringIO

import numpy as np
import pandas as pd

from paddi_utils.data.profiles import Profiles

class Spectra(Profiles):
    """
    A class used to read the spectral data from a PADDI run, usually Z_SPEC* or XY_SPEC*. This has the same interface as :class:`Profiles`; however, a Spectra object can have more than one index. The spectral file is assumed to have dims additional columns, which are given the keys "k0", "k1",... These are prepended into the format. The basic use of this class is as follows::

        import glob
        from paddi_utils.data import Spectra

        # Load the object from the file
        prof = Spectra(["path/to/file1", "path/to/file2", ...])
        # ... or ...
        prof = Spectra(glob.glob("location/of/files*"))

        # Index the Specta object like a numpy array with 
        # indices first in time, then wave number space
        # In the case of multiple spectral dimensions, add 
        # additional indices to the end
        # The following gives the time history of the 
        # thermal energy of the 0,2 mode
        prof["energy_Temp"][:,0,2]

    :type files: :class:`list` of :class:`str`
    :param files: A list of the file names to load, in the desired order to load them
    :type format: :class:`list` of :class:`tuple` of the form (:class:`str`, :class:`type`)
    :param format: The parameter--type pairs of the data to be read from the file; if `None`, instead use :attr:`Spectra.default_format`
    :type dims: :class:`int`
    :param dims: The number of spectral dimensions to load (1 for Z_SPEC, 2 for XY_SPEC)
    :param args: Args passed to :class:`numpy.ndarray` constructor
    :param kwargs: Keyword args passed to :class:`numpy.ndarray` constructor
    """

    default_format = [("energy_u1", np.float),
                      ("energy_u2", np.float),
                      ("energy_u3", np.float),
                      ("energy_u", np.float),
                      ("energy_Temp", np.float),
                      ("energy_Chem", np.float)]
    """The default format for the columns in a spectral file. This can be overwritten if desired."""

    def __new__(cls, files, dims=1, format=default_format, *args, **kwargs):
        # For each dimension, prepend that to the format
        format = [("k%i" % i, np.float) for i in range(dims)] + format

        # Pass an argument to sort and group the data by the wave number columns
        sort_by = ["k%i" % i for i in range(dims)]

        return Profiles.__new__(cls, files, format=format, sort_by=sort_by, 
                                step_regex="#Timstep=(.*)time=(.*)", *args, **kwargs)


