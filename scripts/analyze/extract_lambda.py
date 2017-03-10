import numpy as np
from scipy.optimize import curve_fit
import sqlalchemy

import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib.colors import LogNorm

from paddi_utils.data import Parameters, Diagnostic
from paddi_utils.db import Session, Simulation, OutputFile, Tag

def exp(x, a, l):
    return a * np.exp(10.**l * x)


session = Session()

stmt = session.query(OutputFile.sim_id.label("sim_id"), sqlalchemy.func.min(OutputFile.iter).label("first")).filter(OutputFile.type== "diagnostic").group_by(OutputFile.sim_id).subquery()
q = session.query(OutputFile).join(stmt, OutputFile.sim_id == stmt.c.sim_id).filter(OutputFile.type == "diagnostic", stmt.c.first == OutputFile.iter).order_by(OutputFile.id.desc())

Ris = []
pds = []
lambdas = []
bfs = []

#for result in q.all():
#    sim = result.simulation
#    if sim.compositional_stratif_param != -2.0:
#        continue
#    if sim.z_extent_of_the_box != 50.0:
#        continue
#
#    for tag in result.simulation.tags:
#        if tag.name.startswith("linear"):
#            print("Removing", tag.name)
#            session.delete(tag)
#
#session.commit()

for result in q.all():
    print(result)
    sim = result.simulation

    if sim.compositional_stratif_param != -3.0:
        continue
    if sim.z_extent_of_the_box != 25.0:
        continue


    found = False
    pd = None
    Ri = None

    print("searching tags")
    for tag in sim.tags:
        if tag.name == "linear_growth":
            lambdas.append(tag.value)
            found = True
        if tag.name == "Ri":
            Ri = tag.value
            Ris.append(tag.value)
        if tag.name == "period":
            pd = tag.value
            pds.append(tag.value)
    bfs.append(np.sqrt(sim.thermal_buoyancy_param * sim.thermal_stratif_param - sim.compositional_buoyancy_param * sim.compositional_stratif_param))
    print("Done")

    print(len(lambdas), Ri, pd)
    if found:
        continue

    diagnostic_files = []
    for file in sim.output_files:
        if file.type == "diagnostic":
            diagnostic_files.append(file.file)
    diagnostic_files.sort()
    d = Diagnostic(diagnostic_files)
    params_list = []
    std_list = []
    guess = (1.0e-5, -5.)
    argmin = np.argmin(d["Temp_max"][:])
    argmax = np.argmax(d["Temp_max"][:] > 1.0e0)
    if argmax == 0:
        argmax = len(d["t"][:])
    if np.max(d["Temp_max"]) < 5.0e-1:
        a, l = 0.0, 0.0
    else:
        a, l = 0.0, 0.0
        if argmin < argmax:
            print(argmin, argmax)
            params, cov = curve_fit(exp, d["t"][argmin:argmax], d["Temp_max"][argmin:argmax], p0=guess, method="dogbox", sigma=1/d["Temp_max"][argmin:argmax])
            print(params)
            print(cov)

            a, l = params
            l = 10.0 ** l
        print(a,l)
    plt.plot(d["t"][:], d["Temp_max"][:])
    plt.plot(d["t"][argmin:argmax], a * np.exp(l * d["t"][argmin:a
rgmax]))
    plt.yscale("log")
    plt.ylim((np.min(d["Temp_max"])/2, np.max(d["Temp_max"]*2)))
    plt.show()
    sim.tags.append(Tag(name="linear_amplitude", value=a))
    sim.tags.append(Tag(name="linear_growth", value=l))
    lambdas.append(l)
    session.commit()

session.commit()

fig = plt.figure()

print(pds, bfs)
pds = np.array(pds)
#triang = tri.Triangulation(np.log10(2.0 * np.pi / pds), np.log10(Ris) + 1)
#trip = plt.tripcolor(triang, lambdas, shading='gouraud', norm=LogNorm(vmax=10.0, vmin=1.0e-6))
scatter = plt.scatter(np.array(2.0 * np.pi / pds), Ris, s=100, c=lambdas, norm=LogNorm(vmax=10.0, vmin=1.0e-6))
ycoord = np.array([np.min(Ris), np.max(Ris)])
plt.plot(2.0 * np.pi * np.max(bfs) + 0.0 * ycoord, ycoord, color="black")
plt.plot(2.0 * np.pi * np.max(bfs)/20. + 0.0 * ycoord, ycoord, color="black", ls="--")

plt.xscale("log")
plt.yscale("log")

plt.xlabel("$\omega$")
plt.ylabel("Ri")

plt.xlim((1.e-3, 1.e2))
plt.ylim((0.667e-1, 1.5e4))

cb = plt.colorbar(scatter)
cb.set_label("$\lambda$")
#plt.show()

plt.savefig("lambda.pdf")