import numpy as np
import math

def dms_to_rad(dms):
    dms_split = math.modf(dms)

    ms = str(round(dms_split[0],4)) + "0000"

    d = float(str(dms_split[1]))
    m = float(ms[2:4])
    s = float(ms[4:6])
    print(d)
    print(m)
    print(s)
    decimal = d + m/60 + s/3600

    rad = math.radians(decimal)
    return rad

dms_to_rad(229.114)