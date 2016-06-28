import glob

import matplotlib.pyplot as plt

from paddi_utils.plots import PlotArgumentParser
from paddi_utils.data import Spectra

parser = PlotArgumentParser()
parser.add_argument("--field", default="energy_Chem")
args = parser.parse_args()

# If files have not been specified, use all files named OUT* in the current directory
if len(args.files) == 0:
    args.files = glob.glob("Z_SPEC*")

# Construct the Diagnostic data object
data = Spectra(args.files)

fig, axis = plt.subplots(1, 1, figsize=(6, 4))

color = "blue"

for dataframe in data:
	axis.plot(dataframe["k0"], dataframe[args.field], alpha=0.3, color=color)
axis.plot(data[-1]["k0"], dataframe[args.field], color=color)

# axis.set_ylabel("\mbox{%s}" % args.field)
axis.set_yscale("log")

parser.exit(fig)