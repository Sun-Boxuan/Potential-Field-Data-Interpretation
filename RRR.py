import numpy as np
import math
from Taper2d import taper2d

np.seterr(divide='ignore', invalid='ignore')
#相关系数法
def calculateRRR(dataset, x_spacing, y_spacing, calp, xsize, ysize):

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
    xsize = float(xsize)
    ysize = float(ysize)

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

    xx1 = (xsize - 1)/2
    yy1 = (ysize - 1)/2
    xx = int(xx1)
    yy = int(yy1)
    xnumber = int(len_x + 2*xx)
    ynumber = int(len_y + 2*yy)

    EDT = np.zeros((len), dtype=float)

    for i in range(0, len):
        edt_1 = (((Vxy[i])**2)*2 + (Vxz[i])**2 + (Vyz[i])**2)**0.5
        EDT[i] = edt_1 + EDT[i]
    edt = max(EDT)
    NEDT = np.zeros((len), dtype=float)

    for i in range(0, len):
        nedt_1 = math.atan((EDT[i])/(abs(Vzz[i]) + (calp*edt)))
        NEDT[i] = nedt_1 + NEDT[i]

    expEDT = taper2d(EDT, x, y, xsize, ysize, x_spacing, y_spacing)
    expNEDT = taper2d(NEDT, x, y, xsize, ysize, x_spacing, y_spacing)
    RRR = np.zeros((xnumber, ynumber), dtype=float)

    for j in range(yy, ynumber - yy):
        for i in range(xx, xnumber - xx):
            EDT_cal = expEDT[i - xx: i + xx + 1, j - yy: j + yy + 1]
            EDT_m = np.mean(EDT_cal)
            NEDT_cal = expNEDT[i - xx: i + xx + 1, j - yy: j + yy + 1]
            NEDT_m = np.mean(NEDT_cal)
            EDT_cal2 = EDT_cal - EDT_m
            NEDT_cal2 = NEDT_cal - NEDT_m
            EDT_NEDT = EDT_cal2 * NEDT_cal2
            EDT_NEDT2 = EDT_NEDT.sum()

            EDT_cal3 = EDT_cal2 * EDT_cal2
            EDT_cal4 = EDT_cal3.sum()
            NEDT_cal3 = NEDT_cal2 * NEDT_cal2
            NEDT_cal4 = NEDT_cal3.sum()
            EDT_NEDT3 = EDT_cal4 * NEDT_cal4

            r_cal = EDT_NEDT2/(EDT_NEDT3**0.5)
            RRR[i][j] = RRR[i][j] + r_cal

    RR = RRR[xx: xx + len_x, yy: yy + len_y]

    return RR
