import h5py, numpy as np
from pathlib import Path
p=next(Path(r"E:\ai_project\30days_challenge\day14_borges\data\nisar").glob("*20260620*.h5"))
f=h5py.File(p,"r"); g=f["science/LSAR/GCOV/grids/frequencyA"]
print("projection", g["projection"][()])
print("xspacing", g["xCoordinateSpacing"][()], "yspacing", g["yCoordinateSpacing"][()])
x=g["xCoordinates"][:]; y=g["yCoordinates"][:]
print("x", x[0], x[-1], len(x)); print("y", y[0], y[-1], len(y))
print("center freq", f["science/LSAR/GCOV/metadata/sourceData/swaths/frequencyA/centerFrequency"][()])
print("bandwidth", f["science/LSAR/GCOV/metadata/sourceData/swaths/frequencyA/acquiredRangeBandwidth"][()])
print("pol", g["listOfPolarizations"][:], "terms", g["listOfCovarianceTerms"][:])
print("mask uniq", np.unique(g["mask"][::200,::200],return_counts=True))
print("orbit pass", f["science/LSAR/identification/orbitPassDirection"][()])
print("bbox", f["science/LSAR/identification/boundingPolygon"][()][:300])
print("attrs HHHH", dict(g["HHHH"].attrs))