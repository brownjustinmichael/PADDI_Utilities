import argparse

import numpy as np
import scipy.signal as signal

from paddi_utils.data import Dump, Parameters

parser = argparse.ArgumentParser()

parser.add_argument("--parameter_file", default="parameter_file")
parser.add_argument("--dump_file", default=None)
parser.add_argument("--number", default=4)
parser.add_argument("--convolve", default=5)

args = parser.parse_args()

old_dump = Dump.from_file("DUMP01.cdf")
params = Parameters.from_file(args.parameter_file)

if args.dump_file is None:
	args.dump_file = params["name_of_input_restart_file"] + ".cdf"

dump = Dump(params, args.dump_file, mode="w")

for var in ["Chem", "Temp"]:
	dump[var][:] = (np.random.random(dump[var].shape) - 0.5) * 1.0e-3

for var in ["ux", "uy"]:
	dump[var][:] = (np.random.random(dump[var].shape) - 0.5) * 1.0e-30
	dump[var][0,0,0,:] = 0.0

for var in ["Temp", "Chem", "ux", "uy", "uz"]:
	dump[var][0,0,0,:] = 0.0
	dump[var][params["max_degree_of_y_fourier_modes"],:,:,:] = 0.0
	dump[var][:,:,params["max_degree_of_z_fourier_modes"],:] = 0.0

kx = np.array(dump["kx"]).reshape((1, dump["kx"].size, 1, 1))
ky = np.array(dump["ky"]).reshape((dump["ky"].size, 1, 1, 1))
kz = np.array(dump["kz"]).reshape((1, 1, dump["kz"].size, 1))

dump["uz"][:] = -(kx * dump["ux"][:] + ky * dump["uy"][:]) / kz
dump["uz"][:,:,0,:] = 0.0

print(np.max(dump["uz"]))
print(np.sum(kx * dump["ux"] + ky * dump["uy"] + kz * dump["uz"]))

nz = params["max_degree_of_z_fourier_modes"] * 2
z = np.arange(0, nz) * params["z_extent_of_the_box"] / nz
layer = (np.floor(z * args.number / params["z_extent_of_the_box"]))
layer *= params["z_extent_of_the_box"] / args.number
layer = signal.convolve(layer, signal.boxcar(args.convolve), mode="same") / args.convolve

thermal = np.fft.fft(params["thermal_stratif_param"] * (layer - z)) / (dump["kz"].size)
compositional = np.fft.fft(params["compositional_stratif_param"] * (layer - z)) / (dump["kz"].size)

thermal = np.array([[np.array([np.real(thermal), np.imag(thermal)]).T]])
compositional = np.array([[np.array([np.real(compositional), np.imag(compositional)]).T]])

thermal.resize((params["max_degree_of_y_fourier_modes"] * 2, params["max_degree_of_x_fourier_modes"] + 1, params["max_degree_of_z_fourier_modes"] * 2, 2))
compositional.resize((params["max_degree_of_y_fourier_modes"] * 2, params["max_degree_of_x_fourier_modes"] + 1, params["max_degree_of_z_fourier_modes"] * 2, 2))

dump["Temp"][:] += thermal
dump["Chem"][:] += compositional

dump.close()
