import numpy as np
import math

np.seterr(divide='ignore', invalid='ignore')
#归一化改进的方向总水平导数法
def calculateNEEDT(dataset, x_spacing, y_spacing, calp):

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

    EEDT = np.zeros((len), dtype=float)
    for i in range(0, len):
        eedt_1 = ((((Vxy[i] * Vzz[i])**2 + (Vxz[i] * Vzz[i])**2)**0.5)**2 + (((Vxy[i] * Vzz[i])**2 + ((Vyz[i] * Vzz[i])**2))**0.5)**2)**0.5
        EEDT[i] = eedt_1 + EEDT[i]
    eedt = max(EEDT)

    NEEDT = np.zeros((len), dtype=float)
    for i in range(0, len):
        mn1 = (((Vxz[i]) ** 2 + (Vyz[i]) ** 2 + (Vzz[i]) ** 2) ** 0.5) / 3
        needt_1 = math.atan((EEDT[i])/(mn1 + (calp*eedt)))
        NEEDT[i] = needt_1 + NEEDT[i]

    NEEDT = NEEDT.reshape(-1, 1)

    return NEEDT