import h5py, numpy as np
from pathlib import Path
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
for p in sorted((R/"data/nisar").glob("*.h5")):
    f=h5py.File(p,"r"); s=f["science/LSAR/GCOV/metadata/sourceData/swaths/frequencyA"]
    print("==",p.name[:60])
    for k in ["nearRangeIncidenceAngle","farRangeIncidenceAngle","centerFrequency","acquiredRangeBandwidth","rangeResolution","sceneCenterGroundRangeSpacing"]:
        print(" ",k,s[k][()])
    i=f["science/LSAR/identification"]
    for k in ["trackNumber","frameNumber","absoluteOrbitNumber","orbitPassDirection","zeroDopplerStartTime"]:
        print(" ",k,i[k][()])
    f.close()