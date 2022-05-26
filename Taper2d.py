import numpy as np

def taper2d(dataset, x, y, xsize, ysize, x_spacing, y_spacing):
#前期准备
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

    xsize = float(xsize)
    ysize = float(ysize)
    xx1 = (xsize - 1) / 2
    yy1 = (ysize - 1) / 2
    xx = int(xx1)
    yy = int(yy1)
    dataset = dataset.reshape(len_x, len_y)
    xnumber = int(len_x + 2 * xx)
    ynumber = int(len_y + 2 * yy)
#扩边
    new_data = np.zeros((xnumber, ynumber), dtype=float)
    gp1 = dataset[:, 0: 3]
    gp2 = dataset[:, len_x - 3: len_x]
    [junk1, gpx1] = np.gradient(gp1)
    [junk2, gpx2] = np.gradient(gp2)
    x1 = 0
    x2 = 2 * xx + 1
    x_cal = np.array([[1, 1, 0, 0], [x1, x2, 1, 1], [x1**2, x2**2, 2*x1, 2*x2], [x1**3, x2**3, 3*x1**2, 3*x2**2]])
    for i in range(0, len_x):
        for j in range(0, len_y):
            new_data[j + yy][i + xx] = new_data[j + yy][i + xx] + dataset[j][i]
#sides
    for i in range(0, len_y):
        y_cal = np.array([dataset[i][len_y - 1], dataset[i][0], gpx2[i][2], gpx1[i][0]])
        x_cal_1 = np.linalg.inv(x_cal)
        c_cal = np.dot(y_cal, x_cal_1)
        for j in range(0, xx):
            add1 = c_cal[0] + (j + 1 + xx) * c_cal[1] + c_cal[2] * ((j + 1 + xx)**2) + c_cal[3] * ((j + 1 + xx)**3)
            new_data[i + xx][j] = new_data[i + xx][j] + add1
            add2 = c_cal[0] + (j + 1) * c_cal[1] + c_cal[2] * ((j + 1)**2) + c_cal[3] * ((j + 1)**3)
            new_data[i + xx][j + len_y + yy] = new_data[i + xx][j + len_y + yy] + add2
#top and bottom
    gp1 = dataset[0: 3, :]
    gp2 = dataset[len_y - 3: len_x, :]
    [gpx1, junk1] = np.gradient(gp1)
    [gpx2, junk2] = np.gradient(gp2)
    x2 = 2 * yy + 1
    x_cal = np.array([[1, 1, 0, 0], [x1, x2, 1, 1], [x1**2, x2**2, 2*x1, 2*x2], [x1**3, x2**3, 3*x1**2, 3*x2**2]])
    for j in range(0, len_x):
        y_cal = np.array([dataset[len_y - 1][j], dataset[0][j], gpx2[2][j], gpx1[0][j]])
        x_cal_1 = np.linalg.inv(x_cal)
        c_cal = np.dot(y_cal, x_cal_1)
        for i in range(0, yy):
            add1 = c_cal[0] + (i + 1 + yy) * c_cal[1] + c_cal[2] * ((i + 1 + yy)**2) + c_cal[3] * ((i + 1 + yy)**3)
            new_data[i][j + yy] = new_data[i][j + yy] + add1
            add2 = c_cal[0] + (i + 1) * c_cal[1] + c_cal[2] * ((i + 1) ** 2) + c_cal[3] * ((i + 1) ** 3)
            new_data[i + len_x + xx][j + yy] = new_data[i + len_x + xx][j + yy]+ add2
#corners
    for i in range(xx + len_x, xnumber):
        for j in range(yy + len_y, ynumber):
            if i - len_x - xx > j - len_y - yy:
                add = new_data[i][yy + len_y - 1]
                new_data[i][j] = new_data[i][j] + add
            else:
                add = new_data[xx + len_x - 1][j]
                new_data[i][j] = new_data[i][j] + add

    for i in range(0, xx):
        for j in range(0, yy):
            if i > j:
                add = new_data[xx][j]
                new_data[i][j] = new_data[i][j] + add
            else:
                add = new_data[i][yy]
                new_data[i][j] = new_data[i][j] + add

    for i in range(0, xx):
        for j in range(yy + len_y, ynumber):
            if i > ynumber - j:
                add = new_data[xx][j]
                new_data[i][j] = new_data[i][j] + add
            else:
                add = new_data[i][yy + len_y - 1]
                new_data[i][j] = new_data[i][j] + add

    for i in range(xx + len_x, xnumber):
        for j in range(0, yy):
            if xnumber - i > j:
                add = new_data[xx + len_x - 1][j]
                new_data[i][j] = new_data[i][j] + add
            else:
                add = new_data[i][yy - 1]
                new_data[i][j] = new_data[i - 1][yy - 1] + add

    return new_data
