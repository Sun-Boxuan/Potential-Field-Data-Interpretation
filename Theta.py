import numpy as np

np.seterr(divide='ignore', invalid='ignore')
#Theta图法
def calculateTheta(dataset, x_spacing,y_spacing):

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

    len_x = ((x_e - x_s) / x_spacing) + 1
    len_y = ((y_e - y_s) / y_spacing) + 1
    len_x = int(len_x)
    len_y = int(len_y)
    len = len_y*len_x

    Theta = np.zeros((len), dtype=float)

    for i in range(0, len):
        theta_1 = (((Vxz[i])**2 + (Vyz[i])**2)**0.5)/(((Vxz[i])**2 + (Vyz[i])**2 + (Vzz[i])**2)**0.5)
        Theta[i] = theta_1 + Theta[i]

    Theta = Theta.reshape(-1, 1)

    return Theta
