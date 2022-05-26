import numpy as np
np.seterr(divide='ignore', invalid='ignore')
#欧拉反褶积

def calculateEuler(Vxz, Vyz, Vzz, Vxz_x, Vyz_y, Vzz_x, Vzz_y, Vxyz, xsize, ysize, expx, expy, len_x, len_y):

    len_x = int(len_x)
    len_y = int(len_y)

    xsize = float(xsize)
    ysize = float(ysize)
    xx1 = (xsize - 1)/2
    yy1 = (ysize - 1)/2
    xx = int(xx1)
    yy = int(yy1)

    xnumber = int(len_x + 2*xx)
    ynumber = int(len_y + 2*yy)

    resultx = np.zeros((xnumber, ynumber), dtype=float)
    resulty = np.zeros((xnumber, ynumber), dtype=float)
    resultz = np.zeros((xnumber, ynumber), dtype=float)
    resultn = np.zeros((xnumber, ynumber), dtype=float)
    expz = np.ones((xnumber, ynumber), dtype=float)
    for j in range(yy, ynumber - yy):
        for i in range(xx, xnumber - xx):
            Vxz_x_temp = Vxz_x[i - xx: i + xx + 1, j - yy: j + yy + 1]
            Vxz_x_cal = Vxz_x_temp.reshape((-1, 1), order="F")
            Vxyz_temp = Vxyz[i - xx: i + xx + 1, j - yy: j + yy + 1]
            Vxyz_cal = Vxyz_temp.reshape((-1, 1), order="F")
            Vyz_y_temp = Vyz_y[i - xx: i + xx + 1, j - yy: j + yy + 1]
            Vyz_y_cal = Vyz_y_temp.reshape((-1, 1), order="F")
            Vzz_x_temp = Vzz_x[i - xx: i + xx + 1, j - yy: j + yy + 1]
            Vzz_x_cal = Vzz_x_temp.reshape((-1, 1), order="F")
            Vzz_y_temp = Vzz_y[i - xx: i + xx + 1, j - yy: j + yy + 1]
            Vzz_y_cal = Vzz_y_temp.reshape((-1, 1), order="F")

            Vxz_temp = Vxz[i - xx: i + xx + 1, j - yy: j + yy + 1]
            Vxz_cal = Vxz_temp.reshape((-1, 1), order="F")
            Vyz_temp = Vyz[i - xx: i + xx + 1, j - yy: j + yy + 1]
            Vyz_cal = Vyz_temp.reshape((-1, 1), order="F")
            Vzz_temp = Vzz[i - xx: i + xx + 1, j - yy: j + yy + 1]
            Vzz_cal = Vzz_temp.reshape((-1, 1), order="F")

            expx_temp = expx[i - xx: i + xx + 1, j - yy: j + yy + 1]
            expx_cal = expx_temp.reshape((-1, 1), order="F")
            expy_temp = expy[i - xx: i + xx + 1, j - yy: j + yy + 1]
            expy_cal = expy_temp.reshape((-1, 1), order="F")
            expz_temp = expz[i - xx: i + xx + 1, j - yy: j + yy + 1]
            expz_cal = expz_temp.reshape((-1, 1), order="F")

            A_1 = np.hstack((Vxz_x_cal, Vxyz_cal, Vzz_x_cal, Vxz_cal))
            A_2 = np.hstack((Vxyz_cal, Vyz_y_cal, Vzz_y_cal, Vyz_cal))
            A_3 = np.hstack((Vzz_x_cal, Vzz_y_cal, 0-(Vxz_x_cal + Vyz_y_cal), Vzz_cal))
            A = np.vstack((A_1, A_2, A_3))

            B_1 = expx_cal*Vxz_x_cal + expy_cal*Vxyz_cal + expz_cal*Vzz_x_cal + Vxz_cal
            B_2 = expx_cal*Vxyz_cal + expy_cal*Vyz_y_cal + expz_cal*Vzz_y_cal + Vyz_cal
            B_3 = expx_cal*Vzz_x_cal + expy_cal*Vzz_y_cal - expz_cal*(Vxz_x_cal + Vyz_y_cal) + Vzz_cal
            B = np.vstack((B_1, B_2, B_3))

            [U, S, V] = np.linalg.svd(A)
            linecount = int(U.shape[0])
            SS = np.zeros((4, linecount), dtype=float)
            if linecount > 4:
                for k in range(0, 4):
                    SS[k][k] = 1/S[k] + SS[k][k]
            else:
                for k in range(0, linecount):
                    SS[k][k] = 1/S[k] + SS[k][k]
            V2 = V.T
            xyz1 = np.dot(V2, SS)
            U2 = U.T
            xyz2 = np.dot(xyz1, U2)
            xyz = np.dot(xyz2, B)

            resultx[j][i] = xyz[0] + resultx[j][i]
            resulty[j][i] = xyz[1] + resulty[j][i]
            resultz[j][i] = resultz[j][i] + xyz[2]
            resultn[j][i] = resultn[j][i] - xyz[3]

    outx = np.zeros((len_x, len_y), dtype=float)
    outy = np.zeros((len_x, len_y), dtype=float)
    outz = np.zeros((len_x, len_y), dtype=float)
    outn = np.zeros((len_x, len_y), dtype=float)

    for i in range(0, len_x):
        for j in range(0, len_y):
            outx[j][i] = resultx[j+yy][i+xx]
            outy[j][i] = resulty[j + yy][i + xx]
            outz[j][i] = resultz[j + yy][i + xx]
            outn[j][i] = resultn[j + yy][i + xx]

    return outx, outy, outz, outn
