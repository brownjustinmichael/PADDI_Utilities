import glob

import matplotlib.pyplot as plt

from paddi_utils.plots import PlotArgumentParser
from paddi_utils.data import Diagnostic, Spectra, Profiles

parser = PlotArgumentParser()
args = parser.parse_args()

# Construct the Diagnostic data object
diagnostic_data = Diagnostic(glob.glob("OUT*"))
spectral_data = Spectra(glob.glob("Z_SPEC*"))
profile_data = Profiles(glob.glob("ZPROF*"))

fig = plt.figure(figsize=(18, 10))

temp_axis = plt.subplot2grid((3, 4), (0, 0), colspan=2)
chem_axis = plt.subplot2grid((3, 4), (1, 0), colspan=2, sharex=temp_axis)
temp_spec_axis = plt.subplot2grid((3, 4), (0, 2))
chem_spec_axis = plt.subplot2grid((3, 4), (1, 2), sharex=temp_spec_axis)
u_spec_axis = plt.subplot2grid((3, 4), (2, 2), sharex=temp_spec_axis)
temp_prof_axis = plt.subplot2grid((3, 4), (0, 3))
chem_prof_axis = plt.subplot2grid((3, 4), (1, 3), sharey=temp_prof_axis)

ux_prof_axis = plt.subplot2grid((3, 4), (2, 0), sharey=temp_prof_axis)
uy_prof_axis = plt.subplot2grid((3, 4), (2, 1), sharey=temp_prof_axis)
rho_prof_axis = plt.subplot2grid((3, 4), (2, 3), sharey=temp_prof_axis)

temp_axis.plot(diagnostic_data["t"], diagnostic_data["flux_Temp"])
temp_axis.plot(diagnostic_data["t"], -diagnostic_data["flux_Temp"])
temp_axis.set_ylabel("flux\_Temp")
temp_axis.set_yscale("log")

chem_axis.plot(diagnostic_data["t"], diagnostic_data["flux_Chem"])
chem_axis.plot(diagnostic_data["t"], -diagnostic_data["flux_Chem"])
chem_axis.set_ylabel("flux\_Chem")
chem_axis.set_xlabel("t")
chem_axis.set_yscale("log")

for frame in spectral_data:
	temp_spec_axis.plot(frame["k0"], frame["energy_Temp"], alpha=0.1, color="black")
	chem_spec_axis.plot(frame["k0"], frame["energy_Chem"], alpha=0.1, color="black")
	u_spec_axis.plot(frame["k0"], frame["energy_u3"], alpha=0.1, color="black")

temp_spec_axis.plot(spectral_data[-1]["k0"], spectral_data[-1]["energy_Temp"], color="red")
temp_spec_axis.set_ylabel("energy\_Temp")
temp_spec_axis.set_ylim((10**-6, 10**2))
temp_spec_axis.set_yscale("log")

chem_spec_axis.plot(spectral_data[-1]["k0"], spectral_data[-1]["energy_Chem"], color="red")
chem_spec_axis.set_ylabel("energy\_Chem")
chem_spec_axis.set_ylim((10**-6, 10**2))
chem_spec_axis.set_yscale("log")

u_spec_axis.plot(spectral_data[-1]["k0"], spectral_data[-1]["energy_u3"], color="red")
u_spec_axis.set_ylabel("energy\_u3")
u_spec_axis.set_xlabel("k0")
u_spec_axis.set_ylim((10**-6, 10**2))
u_spec_axis.set_yscale("log")

profiles = [("u1_avg", ux_prof_axis),
            ("u2_avg", uy_prof_axis),
            ("Temp", temp_prof_axis),
            ("Chem", chem_prof_axis)]

for key, axis in profiles:
	for frame in profile_data:
		axis.plot(frame[key], frame["z1"], alpha = 0.1, color="black")
	axis.plot(profile_data[-1][key], profile_data[-1]["z1"], color="red")
	axis.set_ylabel("z")
	axis.set_xlabel(key)

rho = (-profile_data.parameters.thermal_buoyancy / profile_data.parameters.viscous_diffusion * profile_data["Temp_avg"]
      + profile_data.parameters.chemical_buoyancy / profile_data.parameters.viscous_diffusion * profile_data["Chem_avg"]
      + (-profile_data.parameters.thermal_stratification + profile_data.parameters.chemical_stratification) * profile_data["z1"])

for i, frame in enumerate(profile_data):
	rho_prof_axis.plot(rho[i], frame["z1"], alpha = 0.1, color="black")
rho_prof_axis.plot(rho[-1], profile_data[-1]["z1"], color="red")
rho_prof_axis.set_ylabel("z")
rho_prof_axis.set_xlabel("rho")

parser.exit(fig)

