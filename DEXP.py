import numpy as np
from Upward import upward_continuation
import math
def calW(M, N, ZZ, dz, z_max, z_min, dzz, a, r):
    z = np.ones([M, 1])
    W = np.ones([M, 1])
    z[0] = ZZ[0]
    i = 1
    for s in range(1, M):
        z[s] = z[0] + dz * (i - 1)
        if s % N == 0:
            i = i + 1
    z1 = z_min
    z2 = z_max
    for i in range(0, M):
        W[i] = (a + math.exp((r / dzz) * (z[i] - z1))) * (1 + a * math.exp((r / dzz) * (z[i] - z2))) / (
                (1 + math.exp((r / dzz) * (z[i] - z1))) * (1 + math.exp((r / dzz) * (z[i] - z2))))
    return W

def calculation2(Vxx2, deepgroup, znum):
    ly = znum + 1
    lx = Vxx2.shape[0]
    Vxx3 = np.zeros((lx, ly), dtype=float)
    for i in range(0, ly):
        deepz = deepgroup[i]
        for j in range(0, lx):
            vxx = Vxx2[j][i] * (deepz)**1.5
            Vxx3[j][i] = Vxx3[j][i] + vxx
    return Vxx3

def Dexp1(dataset, xcount, ycount, expdeep, znum, poumian, x, y, flag, zzmax, zzmin, aa, rr, deepmax):
    Vxx = dataset[:, 0]
    Vxx = Vxx.astype(float)
    Vyy = dataset[:, 3]
    Vyy = Vyy.astype(float)
    Vzz = dataset[:, 5]
    Vzz = Vzz.astype(float)
    znum = int(znum)
    poumian = int(poumian)
    expdeep = int(expdeep)
    ace = int(poumian - 1)
    updataVxx = upward_continuation(Vxx, expdeep, znum, xcount, ycount, x, y)
    updataVyy = upward_continuation(Vyy, expdeep, znum, xcount, ycount, x, y)
    updataVzz = upward_continuation(Vzz, expdeep, znum, xcount, ycount, x, y)

    Vxx2 = updataVxx[ace, :, :]
    Vyy2 = updataVyy[ace, :, :]
    Vzz2 = updataVzz[ace, :, :]

    deepgroup = np.linspace(0, expdeep, num=znum+1, endpoint=True)
    deepgroup[0] = 1
    Vxx3 = calculation2(Vxx2, deepgroup, znum)
    Vyy3 = calculation2(Vyy2, deepgroup, znum)
    Vzz3 = calculation2(Vzz2, deepgroup, znum)
    dz = deepgroup[2] - deepgroup[1]

    Wxyz1 = (Vxx3) ** 2
    Wxyz2 = (Vyy3) ** 2
    Wxyz3 = (Vzz3) ** 2
    Wxyz = (Wxyz1 + Wxyz2 + Wxyz3)**0.5
    if flag:
        WWW = calW(xcount * ycount * (znum + 1), xcount * ycount, deepgroup, dz, zzmax, zzmin, deepmax, aa, rr)
        WWW = WWW.reshape((xcount, ycount, znum + 1), order='F')
        www = WWW[ace, :, :]
        Wxyz = np.multiply(Wxyz, www)

    R5 = np.unique(Wxyz)
    R1 = max(R5)
    R2 = min(R5)
    R3 = 0.75*(R1 - R2)
    R4 = R2 + R3
    for k in range(0, znum+1):
        for l in range(0, xcount):
            if Wxyz[l][k] < R4:
                Wxyz[l][k] = R2

    return Wxyz

def Dexp2(dataset, xcount, ycount, expdeep, znum, poumian, x, y, flag, zzmax, zzmin, aa, rr, deepmax):

    Vxx = dataset[:, 0]
    Vxx = Vxx.astype(float)
    Vyy = dataset[:, 3]
    Vyy = Vyy.astype(float)
    Vzz = dataset[:, 5]
    Vzz = Vzz.astype(float)
    znum = int(znum)
    poumian = int(poumian)
    expdeep = int(expdeep)
    ace = int(poumian - 1)
    updataVxx = upward_continuation(Vxx, expdeep, znum, xcount, ycount, x, y)
    updataVyy = upward_continuation(Vyy, expdeep, znum, xcount, ycount, x, y)
    updataVzz = upward_continuation(Vzz, expdeep, znum, xcount, ycount, x, y)

    Vxx2 = updataVxx[:, ace, :]
    Vyy2 = updataVyy[:, ace, :]
    Vzz2 = updataVzz[:, ace, :]

    deepgroup = np.linspace(0, expdeep, num=znum+1, endpoint=True)
    deepgroup[0] = 1
    Vxx3 = calculation2(Vxx2, deepgroup, znum)
    Vyy3 = calculation2(Vyy2, deepgroup, znum)
    Vzz3 = calculation2(Vzz2, deepgroup, znum)

    Wxyz1 = (Vxx3) ** 2
    Wxyz2 = (Vyy3) ** 2
    Wxyz3 = (Vzz3) ** 2
    Wxyz = (Wxyz1 + Wxyz2 + Wxyz3)**0.5
    dz = deepgroup[2] - deepgroup[1]
    if flag:
        WWW = calW(xcount * ycount * (znum + 1), xcount * ycount, deepgroup, dz, zzmax, zzmin, deepmax, aa, rr)
        WWW = WWW.reshape((xcount, ycount, znum + 1), order='F')
        www = WWW[ace, :, :]
        Wxyz = np.multiply(Wxyz, www)

    R5 = np.unique(Wxyz)
    R1 = max(R5)
    R2 = min(R5)
    R3 = 0.75*(R1 - R2)
    R4 = R2 + R3
    for k in range(0, znum+1):
        for l in range(0, xcount):
            if Wxyz[l][k] < R4:
                Wxyz[l][k] = R2

    return Wxyz