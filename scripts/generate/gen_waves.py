import argparse

import numpy as np
from sympy.solvers import solve
from sympy import Symbol, I, E, diff, Derivative, N
from sympy.physics.vector import ReferenceFrame, Vector, divergence, gradient

from paddi_utils.data import Parameters

# Read any parameters from the command line
parser = argparse.ArgumentParser()

parser.add_argument("--parameter_file", default="parameter_file")
parser.add_argument("--n_modes", type=int, default=None)
parser.add_argument("--out_file", default=None)
parser.add_argument("--limit", type=float, default=10.0)

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

freq = 10.0 ** np.arange(-5,5,0.01)
dist = (freq ** -2) / 1.0e3

print(dist)

f = open(args.out_file, "w")

angs = []

d = Dump(params)

kx = d["kx"]
ky = d["ky"]
kz = d["kz"]

q = 0
while q < args.n_modes:
	i = np.floor(np.random.rand() * kx.size)
	j = np.floor(np.random.rand() * ky.size)
	k = np.floor(np.random.rand() * (kz.size - 1)) + 1
	sign = np.floor(np.random.rand() * 2)
	sign = 1 if sign > 0 else -1

	if i == 0 and j == 0:
		continue

	if 2.0 * np.pi / abs(kx[i]) < args.limit:
		continue

	if 2.0 * np.pi / abs(ky[j]) < args.limit:
		continue

	print(args.limit)
	if 2.0 * np.pi / abs(kz[k]) < args.limit:
		print("WAVELENGTH: ", 2.0 * np.pi / abs(kz[k]))
		continue

	q += 1

	print(i, j, k)
	print(2.0 * np.pi / kx[i], 2.0 * np.pi / ky[j], 2.0 * np.pi / kz[k])

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
	Uz = dist[np.argmax(freq > abs(ang_value))]
	print(ang_value, Uz)

	subs += (("Uz", Uz),)

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

import matplotlib.pyplot as plt

# hist, bin_edges = np.histogram(angs)

# plt.plot(bin_edges[:-1], hist)

# plt.show()
# plt.show()
