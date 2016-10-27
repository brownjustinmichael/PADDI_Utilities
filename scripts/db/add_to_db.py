from os.path import abspath
from glob import glob
from argparse import ArgumentParser

import numpy as np

from paddi_utils.db import Session, Simulation, OutputFile, Tag
from paddi_utils.data import Parameters

parser = ArgumentParser()
parser.add_argument("--parameter_file", default="parameter_file")
args = parser.parse_args()

session = Session()

params = Parameters.from_file(args.parameter_file)

sim = Simulation.from_params(params)

for type in OutputFile.filenames:
	default = OutputFile.filenames[type]
	for file in glob(default + "*"):
		sim.output_files.append(OutputFile(file=abspath(file), type=str(type)))

try:
	data = np.genfromtxt("shear_file.dat", delimiter=", ", dtype=[("t", np.float), ("u", np.float), ("v", np.float), ("phi", np.float)])
	sim.tags.append(Tag(name="period", value=np.max(data["t"]) + data["t"][-1] - data["t"][-2]))
	umax = np.max(data["u"])
	sim.tags.append(Tag(name="Ri", value=(params["B_therm"] * params["S_therm"] - params["B_comp"] * params["S_comp"]) / umax ** 2))
	sim.tags.append(Tag(name="Pe", value=umax * params["Gammaz"] ** 2 / 2 / np.pi))
except FileNotFoundError:
	pass

session.add(sim)
session.commit()