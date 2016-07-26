import glob

import numpy as np
import pandas as pd

from paddi_utils.data.parameters import Parameters

class Diagnostic(pd.DataFrame):
    """
    A class used to read the Diagnostic data from a PADDI run, usually OUT*. This class is designed to behave exactly as the :class:`pandas.core.frame.DataFrame` class, so all of its members are accessible here.

    To access the attributes of a PADDI diagnostic file (e.g., "OUT01"), construct a :class:`.Diagnostic` object.::

        import glob
        from paddi_utils.data import Diagnostic

        # Load the object from the file
        diagnostic = Diagnostic(["path/to/file1", "path/to/file2", ...])
        # ... or ...
        diagnostic = Diagnostic(glob.glob("location/of/files*"))

        # Index the Diagnostic object like a pandas dataframe
        diagnostic["flux_Chem"][100:]
        diagnostic.iloc[100:]["flux_Chem"]
    
    :type files: :class:`list` of :class:`str`
    :param files: A list of diagnostic file names to open in time order
    :type format: :class:`list` of :class:`tuple` of the form (:class:`str`, :class:`type`)
    :param format: The column--type pairs of the data to be read from the diagnostic file; if `None`, instead use :attr:`Diagnostic.default_format`
    """

    default_format = [("istep", np.int),
                      ("t", np.float),
                      ("dt", np.float),
                      ("urms", np.float),
                      ("VORTrms", np.float),
                      ("TEMPrms", np.float),
                      ("CHEMrms", np.float),
                      ("flux_Temp", np.float),
                      ("flux_Chem", np.float),
                      ("Temp_min", np.float),
                      ("Temp_max", np.float),
                      ("Chem_min", np.float),
                      ("Chem_max", np.float),
                      ("u_min(1)", np.float),
                      ("u_max(1)", np.float),
                      ("u_min(2)", np.float),
                      ("u_max(2)", np.float),
                      ("u_min(3)", np.float),
                      ("u_max(3)", np.float),
                      ("VORT_min(1)", np.float),
                      ("VORT_max(1)", np.float),
                      ("VORT_min(2)", np.float),
                      ("VORT_max(2)", np.float),
                      ("VORT_min(3)", np.float),
                      ("VORT_max(3)", np.float),
                      ("u_max_abs", np.float),
                      ("VORT_max_abs", np.float),
                      ("uxrms", np.float),
                      ("uyrms", np.float),
                      ("uzrms", np.float),
                      ("VORTXrms", np.float),
                      ("VORTYrms", np.float),
                      ("VORTZrms", np.float),
                      ("diss_Temp", np.float),
                      ("diss_Chem", np.float)]
    """The default format of a diagnostic file, given as a list of column--type pairs"""

    def __init__(self, files, format=None):
        if format is None:
            format = Diagnostic.default_format

        # Construct an array from each file
        file_data = []
        for file_name in files:
            array = np.genfromtxt(file_name, dtype=format)
            file_data.append(pd.DataFrame(array))

        # If more than one array was constructed, concatenate the arrays
        if len(file_data) > 1:
            super(Diagnostic, self).__init__(pd.concat(file_data))
        elif len(file_data) == 1:
            super(Diagnostic, self).__init__(file_data[0])
        else:
            super(Diagnostic, self).__init__()

        # Gather parameters from the first file
        self.parameters = Parameters.from_header(files[0])
