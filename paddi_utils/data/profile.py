from io import StringIO
import re
from operator import itemgetter
from itertools import groupby

import numpy as np
import pandas as pd

from paddi_utils.data.diagnostic import Parameters

class Profiles(np.ndarray):
    """A class used to read the Spectral data from a PADDI run, usually Z_SPEC* or XY_SPEC"""

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

    def __new__(cls, files, format=default_format, sort_by=("z1",), step_regex="#Step=(.*),Time=(.*)", *args, **kwargs):
        times = []
        timesteps = []
        data = None

        for file_name in files:
            file_string = ""
            for line in open(file_name):
                if line.lstrip() is "":
                    time, timestep, array = cls.array_from_string(file_string, format=format, sort_by=sort_by, step_regex=step_regex)
                    file_string = ""

                    if array is None:
                        continue
                    times.append(time)
                    timesteps.append(timestep)
                    if data is None:
                        data = array
                    else:
                        data = np.concatenate([data, array])
                else:
                    file_string += line

            time, timestep, array = cls.array_from_string(file_string, format=format, sort_by=sort_by, step_regex=step_regex)
            if array is None:
                continue
            times.append(time)
            timesteps.append(timestep)
            if data is None:
                print(data.shape)
                data = array
            else:
                print(data.shape, array.shape)
                data = np.concatenate([data, array])
            file_string = ""

        if data is None:
            obj = np.ndarray.__new__(cls, [])
        else:
            obj = np.ndarray.__new__(cls, data.shape, dtype=data.dtype, buffer=data.data, *args, **kwargs)

        obj.times = times
        obj.timesteps = timesteps
        obj.parameters = Parameters.from_header(files[0])

        return obj

    @staticmethod
    def array_from_string(string, format=default_format, sort_by=None, step_regex="#Step=(.*),Time=(.*)"):
        dims = []
        try:
            array = np.genfromtxt(StringIO(str(string)), dtype=format, comments="#")
        except TypeError:
            array = np.genfromtxt(StringIO(unicode(string)), dtype=format, comments="#")

        if len(array) != 0:
            total = len(array)
            for key in sort_by:
                array = np.sort(array, order=key)
                dims.append(total // np.argmax(array[key] != array[key][0]))

            dims.reverse()
            array = array.reshape([1] + dims)

            comment = string.split("\n")[0]
            comment = comment.replace(" ","")

            result = re.search(step_regex, comment)

            timestep = int(result.groups()[0])
            time = float(result.groups()[1])

            return time, timestep, array
        else:
            return None, None, None

