"""
Plot the history of a given energy spectrum for a PADDI simulation.
"""

import glob

import matplotlib.pyplot as plt

from paddi_utils.plots import PlotArgumentParser
from paddi_utils.data import Spectra

parser = PlotArgumentParser()
parser.add_argument("--field", default="energy_Chem")
args = parser.parse_args()

# If files have not been specified, use all files named Z_SPEC* in the current directory
if len(args.files) == 0:
    args.files = glob.glob("Z_SPEC*")

# Construct the Diagnostic data object
data = Spectra(args.files)

fig, axis = plt.subplots(1, 1, figsize=(6, 4))

# Plot a faded history of the spectrum
for dataframe in data:
	axis.plot(dataframe["k0"], dataframe[args.field], alpha=0.3, color="black")

# Plot the most recent spectrum in red
axis.plot(data[-1]["k0"], dataframe[args.field], color="red")

axis.set_yscale("log")

parser.save(fig)