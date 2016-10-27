from argparse import ArgumentParser

import numpy as np
from netCDF4 import Dataset

from paddi_utils.data import Parameters

parser = ArgumentParser()
parser.add_argument("file")
parser.add_argument("field")

args = parser.parse_args()

data = Dataset("test.nc")
params = Parameters.from_file("parameter_file")

out = Dataset("out.nc", "w")
z = out.createDimension("Z", params["nz"] - 2)
records = out.createDimension("time")
out.createVariable("gradT", "f8", ("time", "Z"))
out.createVariable("gradmu", "f8", ("time", "Z"))
out.createVariable("dfluxT", "f8", ("time", "Z"))
out.createVariable("dfluxmu", "f8", ("time", "Z"))
out.createVariable("afluxT", "f8", ("time", "Z"))
out.createVariable("afluxmu", "f8", ("time", "Z"))

for i in range(len(data["Temp"])):
	out["gradT"][i] = np.mean(data["Temp"][i][2:,:,:] - data["Temp"][i][:-2,:,:], axis=(1,2)) / (params["Gammaz"] / np.float(params["nz"])) + params["S_therm"]
	out["gradmu"][i] = np.mean(data["Chem"][i][2:,:,:] - data["Chem"][i][:-2,:,:], axis=(1,2)) / (params["Gammaz"] / np.float(params["nz"])) + params["S_comp"]
	# gradrho = -params["B_therm"] / params["D_visc"] * gradT + params["B_comp"] / params["D_visc"] * gradmu

	out["dfluxT"][i] = -params["D_therm"] * out["gradT"][i]
	out["dfluxmu"][i] = -params["D_comp"] * out["gradmu"][i]

	out["afluxT"][i] = np.mean(data["Temp"][i] * data["uz"][i], axis=(1,2))[1:-1]
	out["afluxmu"][i] = np.mean(data["Chem"][i] * data["uz"][i], axis=(1,2))[1:-1]

out.close()