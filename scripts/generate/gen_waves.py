"""
This script generates a spectrum of wave modes and puts them into a fortran-readable file.
"""

import argparse

import numpy as np
from sympy.solvers import solve
from sympy import Symbol, I, E, diff, Derivative, N
from sympy.physics.vector import ReferenceFrame, Vector, divergence, gradient

from paddi_utils.data import Parameters, Dump

# Read any parameters from the command line
parser = argparse.ArgumentParser()

parser.add_argument("--parameter_file", default="parameter_file")
parser.add_argument("--n_modes", type=int, default=None)
parser.add_argument("--out_file", default=None)
parser.add_argument("--limit", type=float, default=50.0)

args = parser.parse_args()

# Read the parameter file
params = Parameters.from_file(args.parameter_file)

if args.out_file is None:
	args.out_file = params["name_of_wave_modes_file"]

if args.n_modes is None:
	args.n_modes = params["number_of_wave_modes"]

# Construct the relevant symbols for the calculation
R = ReferenceFrame("R")

x = R[0] * R.x + R[1] * R.y + R[2] * R.z
t = Symbol("t")
ang = Symbol("ang")
k = Symbol("kx") * R.x + Symbol("ky") * R.y + Symbol("kz") * R.z

R0 = Symbol("R0")
Pr = Symbol("Pr")
tau = Symbol("tau")

U = Symbol("Ux") * R.x + Symbol("Uy") * R.y + Symbol("Uz") * R.z
u = U * E ** (I * (k.dot(x) + ang * t))
P = Symbol("P")
p = P * E ** (I * (k.dot(x) + ang * t))
Temp = Symbol("T")
temp = Temp * E ** (I * (k.dot(x) + ang * t))
Chem = Symbol("C")
chem = Chem * E ** (I * (k.dot(x) + ang * t))

du = 0. * R.x
for x in (R[0], R[1], R[2]):
	for vect in (R.x, R.y, R.z):
		du += diff(u.dot(vect), x, x) * vect

D_visc = 0.0
D_therm = 0.0
D_comp = 0.0
B_therm = Symbol("B_therm")
B_comp = Symbol("B_comp")
S_therm = Symbol("S_therm")
S_comp = Symbol("S_comp")

# Construct the equations
continuity = divergence(u, R)
momentum = I * ang * u + gradient(p, R) - B_therm * temp * R.z + B_comp * chem * R.z - D_visc * du
temperature = I * ang * temp + S_therm * u.dot(R.z) - D_therm * divergence(gradient(temp, R), R)
composition = I * ang * chem + S_comp * u.dot(R.z) - D_comp * divergence(gradient(chem, R), R)

# Solve the equations
# print(solve(temperature, "T"))
subT = solve(temperature, "T")[0]
# print(solve(composition, "C"))
subC = solve(composition, "C")[0]

# print(solve(momentum.dot(R.z).subs(Temp, subT).subs(Chem, subC), "P"))
subP = solve(momentum.dot(R.z).subs(Temp, subT).subs(Chem, subC), "P")[0]

# print(solve(momentum.dot(R.x).subs(P, subP), "Ux"))
subUx = solve(momentum.dot(R.x).subs(P, subP), "Ux")[0]
# print(solve(momentum.dot(R.y).subs(P, subP), "Uy"))
subUy = solve(momentum.dot(R.y).subs(P, subP), "Uy")[0]

# print(solve(solve(continuity, "Uz")[0].subs("Ux", subUx).subs("Uy", subUy) / Symbol("Uz") - 1, "ang"))
ang = solve(solve(continuity, "Uz")[0].subs("Ux", subUx).subs("Uy", subUy) / Symbol("Uz") - 1, "ang")[1]

# Create a distribution of frequencies
wns = 10.0**np.arange(-5,5,0.01)
dist = (wns**(-5.0/3.0)) / 1.0e3
angles = np.arange(-np.pi / 2.0, np.pi / 2.0, np.pi / 200.0)
prob = np.ones(len(angles))
prob[np.abs(angles) < np.pi / 4.0] = 0.0

# Open the output file
f = open(args.out_file, "w")

angs = []

# Create the spectral dimensions for the file
d = Dump(params)

kx = d["kx"]
ky = d["ky"]
kz = d["kz"]

# Generate n_modes worth of wave modes spanning parameter space
q = 0
nkx = np.argmax(kx[:] > 2.0 * np.pi / args.limit)
if nkx == 0:
	nkx = kx.size

nky = np.argmax(ky[:] > 2.0 * np.pi / args.limit)
if nky == 0:
	nky = ky.size // 2

nkz = np.argmax(kz[:] > 2.0 * np.pi / args.limit)
if nkz == 0:
	nkz = kz.size // 2

while q < args.n_modes:
	i = np.floor(np.random.rand() * nkx)
	j = np.floor(np.random.rand() * 2 * nky) - nky
	k = np.floor(np.random.rand() * 2 * nkz) - nkz
	if k == 0:
		continue

	sign = np.floor(np.random.rand() * 2)
	sign = 1 if sign > 0 else -1

	# Filter out any modes that cannot exist or that have wavelengths smaller than the limit provided
	if i == 0 and j == 0:
		continue

	wave_number = np.sqrt(kx[i]**2 + ky[j]**2 + kz[k]**2)
	# print(wave_number, np.max(kx), np.max(ky), np.max(kz), 2.0 * np.pi / args.limit)

	if 2.0 * np.pi / abs(wave_number) < args.limit:
		# print("Too small for limit")
		continue

	this_angle = np.arctan(kz[k] / np.sqrt(kx[i]**2.0 + ky[j]**2.0))
	if np.random.rand() > prob[np.argmax(this_angle < angles)]:
		continue

	q += 1

	# Use the equation results with the new parameters to get the actual values
	subs = (("ang", ang * sign), 
		    ("kx", kx[i]), 
		    ("ky", ky[j]), 
		    ("kz", kz[k]),
		    ("S_therm", params["S_therm"]), 
		    ("S_comp", params["S_comp"]), 
		    ("B_therm", params["B_therm"]), 
		    ("B_comp", params["B_comp"]))

	ang_value = ang.subs(subs) * sign
	angs.append(float(ang_value))
	Uz = dist[np.argmax(wns > wave_number)] / 4.0 / np.pi / wave_number**2

	subs += (("Uz", Uz),)

	# Print to the file in a format that fortran can read
	formats = (ang_value, 
		       i, j, k, 
		       np.real(complex(subUx.subs(subs))),
		       np.imag(complex(subUx.subs(subs))),
		       np.real(complex(subUy.subs(subs))),
		       np.imag(complex(subUy.subs(subs))),
		       np.real(complex(Uz)),
		       np.imag(complex(Uz)),
		       np.real(complex(subT.subs(subs))),
		       np.imag(complex(subT.subs(subs))),
		       np.real(complex(subC.subs(subs))),
		       np.imag(complex(subC.subs(subs))))

	f.write(("%f " + "%i " * 3 + "( %f , %f ) " * 5 + "\n") % formats)

f.close()
