from io import StringIO

import numpy as np
import pandas as pd

from paddi_utils.data.profile import Profiles

class Spectra(Profiles):
    """A class used to read the Profile data from a PADDI run, usually ZPROF*"""

    default_format = [("energy_u1", np.float),
                      ("energy_u2", np.float),
                      ("energy_u3", np.float),
                      ("energy_u", np.float),
                      ("energy_Temp", np.float),
                      ("energy_Chem", np.float)]

    def __new__(cls, files, dims=1, format=default_format):
        format = [("k%i" % i, np.float) for i in range(dims)] + format

        sort_by = ["k%i" % i for i in range(dims)]

        return Profiles.__new__(cls, files, format=format, sort_by=sort_by, 
                                      step_regex="#Timstep=(.*)time=(.*)")


