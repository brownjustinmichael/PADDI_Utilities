import glob

import matplotlib.pyplot as plt

from paddi_utils.plots import PlotArgumentParser
from paddi_utils.data import Profiles

parser = PlotArgumentParser()
parser.add_argument("--field", type=str, default="rho_avg")
args = parser.parse_args()

# If files have not been specified, use all files named OUT* in the current directory
if len(args.files) == 0:
    args.files = glob.glob("ZPROF*")

# Construct the Profile data object
profile_data = Profiles(sorted(args.files))

fig, axis = plt.subplots(1, 1, figsize=(10, 6))

if args.field == "rho_avg":
    # Construct the density field from the parameters of the system
    rho = (-profile_data.parameters["B_therm"] / profile_data.parameters["D_visc"] * profile_data["Temp_avg"]
          + profile_data.parameters["B_comp"] / profile_data.parameters["D_visc"] * profile_data["Chem_avg"]
          + (-profile_data.parameters["S_therm"] + profile_data.parameters["S_comp"]) * profile_data["z1"])
else:
    rho = profile_data[args.field]

# Plot faded history of the density profile
for i, frame in enumerate(profile_data):
    axis.plot(rho[i], frame["z1"], alpha = 0.1, color="black")

# Plot the most recent density profile in red
axis.plot(rho[-1], profile_data[-1]["z1"], color="red")
axis.set_ylabel("z")
axis.set_xlabel("rho")

plt.show()
