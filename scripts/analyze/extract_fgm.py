import numpy as np
from scipy.optimize import curve_fit
import sqlalchemy
from sqlalchemy import func

import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib.colors import LogNorm

from paddi_utils.data import Parameters, Diagnostic, Spectra
from paddi_utils.db import Session, Simulation, OutputFile, Tag


# A typical guess for exp as (a, l)
guess = (1.0e-5, -5.)


def exp(x, a, l):
	"""A simple function to use for curve fitting"""
    return a * np.exp(10.**l * x)


# Open a SQL session
session = Session()

# Query for the first output file of each simulation
q = session.query(Simulation).order_by(func.rand())
# Add additional filters as desired
q = q.filter(Simulation.compositional_stratif_param == -3.0)
q = q.filter(Simulation.z_extent_of_the_box == 25.0)


goal_tags = ["linear_growth", "linear_amplitude", "linear_kx", "linear_ky", "linear_kz"]

for sim in q.all():
    # Check if simulation results are already in the database
    tags = {tag.name: tag for tag in sim.tags}

    found = True
    for tag in goal_tags:
    	if tag not in tags:
    		found = False

    if found:
    	continue

    for tag in goal_tags:
    	if tag in tags:
    		session.delete(tags[tag])
    		tags.pop(tag)

    # If the results are already in the database, simply extract them
    if found:
    	raise RuntimeError("Not yet implemented")
	diagnostic_files = []
	xy_files = []
	z_files = []
	for file in sim.output_files:
	    if file.type == "diagnostic":
	        diagnostic_files.append(file.file)
        if file.type == "xyspec":
            xy_files.append(file.file)
        if file.type == "zspec":
            z_files.append(file.file)
    diagnostic_files.sort()
    xy_files.sort()
    z_files.sort()
	try:
	    d = Diagnostic(diagnostic_files)
	except IOError:
	    print("Couldn't find file")
	    continue
	plt.plot(d["t"][::100], d["Temp_max"][::100])
	plt.yscale("log")
	plt.show()
	median = np.sqrt(np.max(d["Temp_max"]) * np.min(d["Temp_max"]))
	idx = np.argmax(d["Temp_max"] > median)
	# Check if this is a decaying simulation
	if idx == 0:
		print("Decay")

		sim.tags.append(Tag(name="linear_amplitude", value=0.0))
		sim.tags.append(Tag(name="linear_growth", value=0.0))
		sim.tags.append(Tag(name="linear_kx", value=0.0))
		sim.tags.append(Tag(name="linear_ky", value=0.0))
		sim.tags.append(Tag(name="linear_kz", value=0.0))
	else:
		# Set the lower bound to the the global minimum
		argmin = np.argmin(d["Temp_max"][:])
		# Set the upper bound to be where the max temperature exceeds unity
		# Since the temperature is unitless, this is a good value to indicate 
		# That the system has become nonlinear
		argmax = np.argmax(d["Temp_max"][:] > 1.0e0)
		print(argmin, argmax)
		# Calculate the best exponential fit to the linear region
		params, cov = curve_fit(exp, d["t"][argmin:argmax], d["Temp_max"][argmin:argmax], p0=guess, method="dogbox", sigma=1/d["Temp_max"][argmin:argmax])
		print(params)
		print(cov)

		a, l = params
		l = 10.0 ** l

	    plt.plot(d["t"][:], d["Temp_max"][:])
	    plt.plot(d["t"][argmin:argmax], a * np.exp(l * d["t"][argmin:argmax]))
	    plt.yscale("log")
	    plt.ylim((np.min(d["Temp_max"])/2, np.max(d["Temp_max"]*2)))
	    plt.show()

		# Read the XY spectra
		xy = Spectra(xy_files, dims=2, idx=idx//200)
		# Determine the mode with the most energy
		maxidx = np.unravel_index(xy["energy_u3"][idx].argmax(), xy["energy_u3"][idx].shape)
		# Should print the strongest mode's wavenumbers
		kx = xy["k0"][idx][maxidx]
		ky = xy["k1"][idx][maxidx]

		# Read the Z spectra
		z = Spectra(z_files, idx=idx//200)
		# Determine the mode with the most energy
		maxidx = np.unravel_index(z["energy_u3"][idx].argmax(), z["energy_u3"][idx].shape)
		# Should print the strongest mode's wavenumbers
		kz = xy["k0"][idx][maxidx]

		print(kx, ky, kz)

		sim.tags.append(Tag(name="linear_amplitude", value=params[0]))
		sim.tags.append(Tag(name="linear_growth", value=10.0**params[1]))
		sim.tags.append(Tag(name="linear_kx", value=kx))
		sim.tags.append(Tag(name="linear_ky", value=ky))
		sim.tags.append(Tag(name="linear_kz", value=kz))

	session.commit()



