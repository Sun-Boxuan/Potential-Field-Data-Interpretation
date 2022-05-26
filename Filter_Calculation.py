import numpy as np
from Taper2d import taper2d

def filter(Vxz, Vyz, Vzz, x, y, x_spacing, y_spacing, outx, outy, outz, outn, xsize, ysize, kt1, kt2, kt3, DS, NN, len_x, len_y):
# 滤波前期准备
    x_s = x[0]
    x_e = x[-1]
    y_s = y[0]
    y_e = y[-1]
    x_s = float(x_s)
    x_e = float(x_e)
    y_s = float(y_s)
    y_e = float(y_e)
    kt1 = float(kt1)
    kt2 = float(kt2)
    kt3 = float(kt3)
    x_spacing = float(x_spacing)
    y_spacing = float(y_spacing)

    len_x = int(len_x)
    len_y = int(len_y)

    xsize = float(xsize)
    ysize = float(ysize)
    xx1 = (xsize - 1) / 2
    yy1 = (ysize - 1) / 2
    xx = int(xx1)
    yy = int(yy1)

    Vxz = Vxz.reshape(len_x, len_y)
    Vyz = Vyz.reshape(len_x, len_y)
    Vzz = Vzz.reshape(len_x, len_y)

    (Vxz_y, Vxz_x) = np.gradient(Vxz)
    (Vyz_y, Vyz_x) = np.gradient(Vyz)
    (Vzz_y, Vzz_x) = np.gradient(Vzz)
    Vxyz = (Vxz_y + Vyz_x) / 2

    expVxz_x = taper2d(Vxz_x, x, y, xsize, ysize, x_spacing, y_spacing)
    expVyz_y = taper2d(Vyz_y, x, y, xsize, ysize, x_spacing, y_spacing)
    expVzz_x = taper2d(Vzz_x, x, y, xsize, ysize, x_spacing, y_spacing)
    expVzz_y = taper2d(Vzz_y, x, y, xsize, ysize, x_spacing, y_spacing)
    expVxyz = taper2d(Vxyz, x, y, xsize, ysize, x_spacing, y_spacing)

    Ah1 = ((Vxz_x ** 2) + (Vxyz ** 2)) ** 0.5
    theta1 = np.mean(Ah1)
    Ah2 = ((Vxyz ** 2) + (Vyz_y ** 2)) ** 0.5
    theta2 = np.mean(Ah2)
    Ah3 = ((Vzz_x ** 2) + (Vzz_y ** 2)) ** 0.5
    theta3 = np.mean(Ah3)

    x1 = x.reshape(-1, 1)
    y1 = y.reshape(-1, 1)
    outx1 = outx.reshape((-1, 1), order="F")
    outy1 = outy.reshape((-1, 1), order="F")
    outz1 = outz.reshape((-1, 1), order="F")
    outn1 = outn.reshape((-1, 1), order="F")

    PXY7 = np.zeros((len_x, len_y), dtype=float)
    PXY8 = np.zeros((len_x, len_y), dtype=float)
    PXY9 = np.zeros((len_x, len_y), dtype=float)

    for j in range(0, len_y):
        for i in range(0, len_x):
            expVxz_x_temp = expVxz_x[i: i + (2*xx+1), j: j + (2*yy+1)]
            expVxz_x_cal = expVxz_x_temp.reshape((-1, 1), order="F")
            expVxyz_temp = expVxyz[i: i + (2*xx+1), j: j + (2*yy+1)]
            expVxyz_cal = expVxyz_temp.reshape((-1, 1), order="F")
            expVyz_y_temp = expVyz_y[i: i + (2 * xx + 1), j: j + (2 * yy + 1)]
            expVyz_y_cal = expVyz_y_temp.reshape((-1, 1), order="F")
            expVzz_x_temp = expVzz_x[i: i + (2 * xx + 1), j: j + (2 * yy + 1)]
            expVzz_x_cal = expVzz_x_temp.reshape((-1, 1), order="F")
            expVzz_y_temp = expVzz_y[i: i + (2 * xx + 1), j: j + (2 * yy + 1)]
            expVzz_y_cal = expVzz_y_temp.reshape((-1, 1), order="F")

            Ah11 = ((expVxz_x_cal ** 2) + (expVxyz_cal ** 2)) ** 0.5
            theta11 = np.mean(Ah11)
            Ah12 = ((expVxyz_cal ** 2) + (expVyz_y_cal ** 2)) ** 0.5
            theta12 = np.mean(Ah12)
            Ah13 = ((expVzz_x_cal ** 2) + (expVzz_y_cal ** 2)) ** 0.5
            theta13 = np.mean(Ah13)
            Ah = np.array([theta11, theta12, theta13])
            PXY7[j][i] = PXY7[j][i] + Ah[0]
            PXY8[j][i] = PXY8[j][i] + Ah[1]
            PXY9[j][i] = PXY9[j][i] + Ah[2]
    PXY7 = PXY7.reshape((-1, 1), order="F")
    PXY8 = PXY8.reshape((-1, 1), order="F")
    PXY9 = PXY9.reshape((-1, 1), order="F")
    PXY = np.hstack((x1, y1, outx1, outy1, outz1, outn1, PXY7, PXY8, PXY9))
#滤波1
    m = 0
    n = len_x * len_y
    while m < n:
        if PXY[m][6] < theta1 * kt1 or PXY[m][7] < theta2 * kt2 or PXY[m][8] < theta3 * kt3:
            PXY = np.delete(PXY, m, axis=0)
            n -= 1
        else:
            m += 1
#滤波2
    size1 = len(PXY)
    S = np.zeros((size1, 1), dtype=float)
    for cc in range(0, size1):
        S[cc][0] = S[cc][0] + ((PXY[cc][0] - PXY[cc][2])**2 + (PXY[cc][1] - PXY[cc][3])**2)**0.5
    ss = xx * (x_spacing**2 + y_spacing**2)**0.5
    m1 = 0
    while m1 < size1:
        if S[m1][0] > ss:
            PXY = np.delete(PXY, m1, axis=0)
            S = np.delete(S, m1, axis=0)
            size1 -= 1
        else:
            m1 += 1
#滤波3
    m2 = 0
    size2 = PXY.shape[0]
    while m2 < size2:
        if PXY[m2][2] > x_e or PXY[m2][2] < x_s or PXY[m2][3] > y_e or PXY[m2][3] < y_s or PXY[m2][4] < 0:
            PXY = np.delete(PXY, m2, axis=0)
            size2 -= 1
        else:
            m2 += 1

#滤波4
    size3 = len(PXY)
    NK = np.zeros((1, size3), dtype=float)

    for i2 in range(0, size3):
        kk = np.zeros((1, size3), dtype=float)
        for j2 in range(0, size3):
            s2 = ((PXY[i2][2] - PXY[j2][2])**2 + (PXY[i2][3] - PXY[j2][3])**2 + (PXY[i2][4] - PXY[j2][4])**2)**0.5
            if s2 < DS * x_spacing:
                kk[0][j2] = kk[0][j2] + 1
        NK[0][i2] = NK[0][i2] + np.sum(kk)

    N1 = np.ones((1, size3), dtype=float)
    NK2 = NK - N1
    NK3 = NK2.T
    m3 = 0
    while m3 < size3:
        if NK3[m3][0] < NN:
            PXY = np.delete(PXY, m3, axis=0)
            NK3 = np.delete(NK3, m3, axis=0)
            size3 -= 1
        else:
            m3 += 1
#滤波5
    size4 = len(PXY)
    range1 = np.loadtxt('./record/range.txt')
    range1 = range1.astype(float)
    range2 = range1.reshape(-1, 4)
    p = len(range2)
    NK4 = np.zeros((1, size4), dtype=float)
    for q in range(0, p):#各个框的坐标
        l1 = range2[q][0]
        l2 = range2[q][1]
        l3 = range2[q][2]
        l4 = range2[q][3]
        for i3 in range(0, size4):
            if PXY[i3][2] >= l1 and PXY[i3][2] <= l2 and PXY[i3][3] >= l3 and PXY[i3][3] <= l4:#如果点在框内
                NK4[0][i3] = NK4[0][i3] + 1#计数+1
    m4 = 0
    while m4 < size4:
        if NK4[0][m4] < 1:#点坐标一次都没落在框内
            PXY = np.delete(PXY, m4, axis=0)#删除
            NK4 = np.delete(NK4, m4, axis=1)
            size4 -= 1
        else:
            m4 += 1


    outputx = PXY[:, 2]
    outputy = PXY[:, 3]
    outputz = PXY[:, 4]
    return outputx, outputy, outputz
