from io import BytesIO
import re
from operator import itemgetter
from itertools import groupby

import numpy as np
import pandas as pd

from paddi_utils.data.diagnostic import Parameters

class Profiles(np.ndarray):
    """
    A class used to read the Profile data from a PADDI run, usually ZPROF*. This class is designed to behave exactly as a :class:`numpy.ndarray` object, and so has access to all the members of that class. If given an :class:`int` index, the array returned will contain all the columns for that timestep. If given a :class:`str` index, the array returned will contain all timesteps for that column. The basic use of this class is as follows::

        import glob
        from paddi_utils.data import Profiles

        # Load the object from the file
        prof = Profiles(["path/to/file1", "path/to/file2", ...])
        # ... or ...
        prof = Profiles(glob.glob("location/of/files*"))

        # Index the Profiles object like a numpy array 
        # with indices first in time, then space
        # The following gives the full history of the
        # average temperature at the 128th grid point 
        prof["Temp_avg"][:,128]

    :type files: :class:`list` of :class:`str`
    :param files: A list of the file names to load, in the desired order to load them
    :type format: :class:`list` of :class:`tuple` of the form (:class:`str`, :class:`type`)
    :param format: The parameter--type pairs of the data to be read from the file; if `None`, instead use :attr:`Profiles.default_format`
    :type sort_by: :class:`tuple` of :class:`str`
    :param sort_by: The indices to group and sort the file lines by, in order
    :type step_regex: :class:`str`
    :param step_regex: The regex string to use to extract the step and timestep information (needs two "captures")
    :param args: Args passed to :class:`numpy.ndarray` constructor
    :param kwargs: Keyword args passed to :class:`numpy.ndarray` constructor
    """

    default_format = [("z1", np.float),
                      ("u1", np.float),
                      ("u2", np.float),
                      ("u3", np.float),
                      ("vort1", np.float),
                      ("vort2", np.float),
                      ("vort3", np.float),
                      ("Temp", np.float),
                      ("Chem", np.float),
                      ("u1_avg", np.float),
                      ("u2_avg", np.float),
                      ("u3_avg", np.float),
                      ("vort1_avg", np.float),
                      ("vort2_avg", np.float),
                      ("vort3_avg", np.float),
                      ("Temp_avg", np.float),
                      ("Chem_avg", np.float),]
    """The default format for a spectral output file. This can be overwritten if desired."""

    def __new__(cls, files, format=default_format, sort_by=("z1",), step_regex="#Step=(.*),Time=(.*)", idx=None, *args, **kwargs):
        times = []
        timesteps = []
        data = None
        i = 0

        # Iterate through the fiels
        for file_name in files:
            file_string = ""

            # Go line by line
            for line in open(file_name):
                # When the end of a block is reached, log the results
                if idx is not None and i > idx:
                    break

                if line.lstrip() is "":
                    # Record the time and array information]
                    time, timestep, array = cls.array_from_string(file_string, format=format, sort_by=sort_by, step_regex=step_regex)
                    file_string = ""

                    # Ignore empty blocks
                    if array is None:
                        continue

                    i += 1
                    if idx is not None and idx != i - 1:
                        continue

                    times.append(time)
                    timesteps.append(timestep)

                    if data is None:
                        data = array
                    else:
                        data = np.concatenate([data, array])
                else:
                    file_string += line

        # If there are still no data, return an empty array
        if data is None:
            obj = np.ndarray.__new__(cls, [])
        else:
            obj = np.ndarray.__new__(cls, data.shape, dtype=data.dtype, buffer=data.data, *args, **kwargs)

        # Add the time and parameter information to the new class
        obj.times = times
        obj.timesteps = timesteps
        obj.parameters = Parameters.from_header(files[0])

        return obj

    @staticmethod
    def array_from_string(string, format=default_format, sort_by=None, step_regex="#Step=(.*),Time=(.*)"):
        """
        This is a convenience method to clean up the instantiation. Given a string and the same format parameters as above, construct a correctly shaped array.

        :type format: :class:`list` of :class:`tuple` of the form (:class:`str`, :class:`type`)
        :param format: The parameter--type pairs of the data to be read from the file; if `None`, instead use :attr:`Profiles.default_format`
        :type sort_by: :class:`tuple` of :class:`str`
        :param sort_by: The indices to group and sort the file lines by, in order
        :type step_regex: :class:`str`
        :param step_regex: The regex string to use to extract the step and timestep information (needs two "captures")

        :rtype: :class:`float`, :class:`int`, :class:`numpy.ndarray`
        :return: The current simulation time, the current simulation timestep number, and the correctly shaped data array
        """
        # Read the data from the string
        try:
            # Python 3 with byte input
            array = np.genfromtxt(BytesIO(string.encode()), dtype=format, comments="#")
        except TypeError:
            # Python 2
            array = np.genfromtxt(BytesIO(unicode(string)), dtype=format, comments="#")

        dims = []
        if len(array) != 0:
            # Calculate the correct dimensions, given the sorting indices
            total = len(array)
            for key in sort_by:
                array = np.sort(array, order=key)
                dims.append(total // np.argmax(array[key] != array[key][0]))

            dims.reverse()
            dims = tuple(np.maximum(dims, 1))

            # Reshape the array
            array = array.reshape([1] + dims)

            # Extract the timing information
            comment = string.split("\n")[0]
            comment = comment.replace(" ","")

            result = re.search(step_regex, comment)

            timestep = int(result.groups()[0])
            time = float(result.groups()[1])

            return time, timestep, array
        else:
            # If there is no array; return None
            return None, None, None

