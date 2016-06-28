import glob

import numpy as np
import pandas as pd

class Parameters(object):
    default_format = [("thermal_buoyancy", np.float),
                      ("chemical_buoyancy", np.float),
                      ("viscous_diffusion", np.float),
                      ("thermal_diffusion", np.float),
                      ("compositional_diffusion", np.float),
                      ("thermal_stratification", np.float),
                      ("chemical_stratification", np.float),
                      ("length", np.float),
                      ("width", np.float),
                      ("height", np.float),
                      ("CFL", np.float),
                      ("timestep_max", np.float),
                      ("timestep_init", np.float),
                      ("Lmax", np.int),
                      ("Mmax", np.int),
                      ("Nmax", np.int),
                      ("Nx", np.int),
                      ("Ny", np.int),
                      ("Nz", np.int),
                      ("number_of_tasks_1st_transpose", np.int),
                      ("number_of_tasks_2nd_transpose", np.int)]

    """Read the parameter information for the run"""
    def __init__(self, parameter_strings, format=default_format):
        super(Parameters, self).__init__()
        for line, (key, dtype) in zip(parameter_strings[12:33], format):
            setattr(self, key, dtype(line.split()[-1]))

    @classmethod
    def from_file(cls, file_name, format=default_format):
        file = open(file_name, "r")
        string = [file.readline() for i in range(41)]
        return cls(string, format=format)


class Diagnostic(pd.DataFrame):
    """A class used to read the Diagnostic data from a PADDI run, usually OUT*"""

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

    def __init__(self, files, format=default_format):
        file_data = []
        for file_name in files:
            array = np.genfromtxt(file_name, dtype=format)
            file_data.append(pd.DataFrame(array))

        super(Diagnostic, self).__init__(pd.concat(file_data))

        self.parameters = Parameters.from_file(files[0])




