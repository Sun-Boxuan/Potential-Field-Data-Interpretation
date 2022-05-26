import numpy as np
import math

np.seterr(divide='ignore', invalid='ignore')
#归一化方向总水平导数法
def calculateNEDT(dataset, x_spacing, y_spacing, calp):

    Vxy = dataset[:, 1]
    Vxy = Vxy.astype(float)
    Vxz = dataset[:, 2]
    Vxz = Vxz.astype(float)
    Vyz = dataset[:, 4]
    Vyz = Vyz.astype(float)
    Vzz = dataset[:, 5]
    Vzz = Vzz.astype(float)
    x = dataset[:, 7]
    y = dataset[:, 8]

    x_s = x[0]
    x_e = x[-1]
    y_s = y[0]
    y_e = y[-1]
    x_s = float(x_s)
    x_e = float(x_e)
    y_s = float(y_s)
    y_e = float(y_e)
    x_spacing = float(x_spacing)
    y_spacing = float(y_spacing)
    calp = float(calp)

    len_x = ((x_e - x_s) / x_spacing) + 1
    len_y = ((y_e - y_s) / y_spacing) + 1
    len_x = int(len_x)
    len_y = int(len_y)
    len = len_y*len_x

    EDT = np.zeros((len), dtype=float)

    for i in range(0, len):
        edt_1 = (((Vxy[i])**2)*2 + (Vxz[i])**2 + (Vyz[i])**2)**0.5
        EDT[i] = edt_1 + EDT[i]
    edt = max(EDT)
    NEDT = np.zeros((len), dtype=float)

    for i in range(0, len):
        nedt_1 = math.atan((EDT[i])/(abs(Vzz[i]) + (calp*edt)))
        NEDT[i] = nedt_1 + NEDT[i]

    NEDT = NEDT.reshape(-1, 1)

    return NEDT
