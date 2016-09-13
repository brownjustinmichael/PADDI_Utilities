"""
This script takes a PADDI parameter_file and generates a restart dump file that has a perfect staircase structure in density.
"""

import argparse

import numpy as np
import scipy.signal as signal

from paddi_utils.data import Dump, Parameters

parser = argparse.ArgumentParser()

parser.add_argument("--parameter_file", default="parameter_file")
parser.add_argument("--dump_file", default=None)
parser.add_argument("--number", default=4, type=int)
parser.add_argument("--convolve", default=5, type=int)
parser.add_argument("--offset", default=0.0, type=float)

args = parser.parse_args()

# Load the parameters from file
params = Parameters.from_file(args.parameter_file)

# Use the dump file name from the parameters if one is not given
if args.dump_file is None:
	args.dump_file = params["name_of_input_restart_file"] + ".cdf"

# Create the dump file object
dump = Dump(params, args.dump_file, mode="w")

# Start the buoyancy fields with weak perturbations
for var in ["Chem", "Temp"]:
	dump[var][:] = (np.random.random(dump[var].shape) - 0.5) * 1.0e-3

# Start the velocity fields with extremely small perturbations
for var in ["ux", "uy"]:
	dump[var][:] = (np.random.random(dump[var].shape) - 0.5) * 1.0e-30
	dump[var][0,0,0,:] = 0.0

# Several modes in the simulation are 0 by construction
for var in ["Temp", "Chem", "ux", "uy", "uz"]:
	dump[var][0,0,0,:] = 0.0
	dump[var][params["max_degree_of_y_fourier_modes"],:,:,:] = 0.0
	dump[var][:,:,params["max_degree_of_z_fourier_modes"],:] = 0.0

# Construct the spectral dimension arrays from the dump file
kx = np.array(dump["kx"]).reshape((1, dump["kx"].size, 1, 1))
ky = np.array(dump["ky"]).reshape((dump["ky"].size, 1, 1, 1))
kz = np.array(dump["kz"]).reshape((1, 1, dump["kz"].size, 1))

# Ensure that the field is divergence free
dump["uz"][:] = -(kx * dump["ux"][:] + ky * dump["uy"][:]) / kz
dump["uz"][:,:,0,:] = 0.0

# Construct the layer profile in physical space
nz = params["max_degree_of_z_fourier_modes"] * 2
z = np.arange(0.0, nz * 2) * params["z_extent_of_the_box"] / nz - args.offset
layer = (np.floor(z * args.number / params["z_extent_of_the_box"]))
layer *= params["z_extent_of_the_box"] / args.number

# Smooth the profile by convolving with a boxcar
layer = (signal.convolve(layer, signal.boxcar(args.convolve), mode="same") / args.convolve)[:dump["kz"].size]
z = z[:dump["kz"].size]

# Using the layer profile, construct the actual buoyant fields in fourier space
thermal = np.fft.fft(params["thermal_stratif_param"] * (layer - z)) / (dump["kz"].size)
compositional = np.fft.fft(params["compositional_stratif_param"] * (layer - z)) / (dump["kz"].size)

# Reshape the complex arrays into real arrays that can be loaded into a netCDF file
thermal = np.array([[np.array([np.real(thermal), np.imag(thermal)]).T]])
compositional = np.array([[np.array([np.real(compositional), np.imag(compositional)]).T]])

# Resize the 1D arrays into 3D arrays padded with 0.0
thermal.resize((params["max_degree_of_y_fourier_modes"] * 2, params["max_degree_of_x_fourier_modes"] + 1, params["max_degree_of_z_fourier_modes"] * 2, 2))
compositional.resize((params["max_degree_of_y_fourier_modes"] * 2, params["max_degree_of_x_fourier_modes"] + 1, params["max_degree_of_z_fourier_modes"] * 2, 2))

# Set the dump file variables to the new arrays
dump["Temp"][:] += thermal
dump["Chem"][:] += compositional

dump.close()
