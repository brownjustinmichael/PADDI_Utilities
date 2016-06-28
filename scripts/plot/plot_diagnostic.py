import glob

import matplotlib.pyplot as plt

from paddi_utils.plots import PlotArgumentParser
from paddi_utils.data import Diagnostic

parser = PlotArgumentParser()
args = parser.parse_args()

# If files have not been specified, use all files named OUT* in the current directory
if len(args.files) == 0:
    args.files = glob.glob("OUT*")

# Construct the Diagnostic data object
data = Diagnostic(args.files)

fig, (temp_axis, comp_axis) = plt.subplots(2, 1, figsize=(6, 6), sharex=True)

temp_axis.plot(data["t"], data["flux_Temp"])
temp_axis.set_ylabel("Temperature Flux")
temp_axis.set_yscale("log")

comp_axis.plot(data["t"], data["flux_Chem"])
comp_axis.set_ylabel("Composition Flux")
comp_axis.set_xlabel("Time")
comp_axis.set_yscale("log")

parser.exit(fig)