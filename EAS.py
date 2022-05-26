import numpy as np
from Taper2d import taper2d
np.seterr(divide='ignore', invalid='ignore')
#EAS-相关系数法

def calculateEAS(dataset, x_spacing, y_spacing, xsize, ysize):

    Vxy = dataset[:, 1]
    Vxy = Vxy.astype(float)
    Vxz = dataset[:, 2]
    Vxz = Vxz.astype(float)
    Vyz = dataset[:, 4]
    Vyz = Vyz.astype(float)
    Vz = dataset[:, 6]
    Vz = Vz.astype(float)
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

    len_x = ((x_e - x_s) / x_spacing) + 1
    len_y = ((y_e - y_s) / y_spacing) + 1
    len_x = int(len_x)
    len_y = int(len_y)

    xx1 = (xsize - 1)/2
    yy1 = (ysize - 1)/2
    xx = int(xx1)
    yy = int(yy1)
    xnumber = int(len_x + 2*xx)
    ynumber = int(len_y + 2*yy)

    EAS = Vxz ** 2 + Vyz ** 2 + ((2 * Vxy) ** 2)

    expEAS = taper2d(EAS, x, y, xsize, ysize, x_spacing, y_spacing)
    expVz = taper2d(Vz, x, y, xsize, ysize, x_spacing, y_spacing)

    RRR = np.zeros((xnumber, ynumber), dtype=float)
    for j in range(yy, ynumber - yy):
        for i in range(xx, xnumber - xx):
            ASM_cal = expEAS[i - xx: i + xx + 1, j - yy: j + yy + 1]
            ASM_m = np.mean(ASM_cal)
            Vzz_cal = expVz[i - xx: i + xx + 1, j - yy: j + yy + 1]
            Vzz_m = np.mean(Vzz_cal)
            ASM_cal2 = ASM_cal - ASM_m
            Vzz_cal2 = Vzz_cal - Vzz_m
            Vzz_ASM = ASM_cal2 * Vzz_cal2
            Vzz_ASM2 = Vzz_ASM.sum()

            ASM_cal3 = ASM_cal2 * ASM_cal2
            ASM_cal4 = ASM_cal3.sum()
            Vzz_cal3 = Vzz_cal2 * Vzz_cal2
            Vzz_cal4 = Vzz_cal3.sum()
            Vzz_ASM3 = ASM_cal4 * Vzz_cal4

            r_cal = Vzz_ASM2/(Vzz_ASM3**0.5)
            RRR[i][j] = RRR[i][j] + r_cal

    R5 = np.unique(RRR)
    R1 = max(R5)
    R2 = min(R5)
    R3 = 0.35*(R1 - R2)
    R4 = R2 + R3
    for k in range(0, len_y):
        for l in range(0, len_x):
            if RRR[l][k] > R4:
                RRR[l][k] = R1

    for i in range(xx, xx + len_x):
        for j in range(yy, yy + len_y):
            RX0 = RRR[i][j] + RRR[i+1][j] + RRR[i][j+1] + RRR[i-1][j] + RRR[i][j-1]
            if RX0 >= 0.5:
                RRR[i][j] = R1

    RR = RRR[xx: xx + len_x, yy: yy + len_y]
    return RR