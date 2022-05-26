import numpy as np

def regional(dataset, x, y, xsize, ysize, x_spacing, y_spacing):

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
    xx1 = (xsize - 1)/2
    yy1 = (ysize - 1)/2
    xx = int(xx1)
    yy = int(yy1)

    xnumber = int(len_x + 2*xx)
    ynumber = int(len_y + 2*yy)

    expdataset = np.zeros((ynumber, xnumber), dtype=float)
    dataset = np.array(dataset)
    dataset = dataset.astype('float64')
    dataset = dataset.reshape(len_x, len_y)
    dataleft = np.zeros(len_y)
    dataright = np.zeros(len_y)
    datatop = np.zeros(xnumber)
    databottom = np.zeros(xnumber)
#左右两侧

    for i in range(xx, len_x+xx):
        for j in range(yy, len_y+yy):
            expdataset[j][i] = expdataset[j][i] + dataset[j-yy][i-xx]
    #left
    for i in range(0, xx):
        for j in range(0, len_y):
            gl = dataset[j][i] - dataset[j][i+1]
            gl = gl/xx
            dataleft[j] = dataleft[j] + gl

    for i in range(0, xx):
        for j in range(0, len_y):
            addleft = dataset[j][0] + dataleft[j] * (xx - i)
            expdataset[j + yy][i] = expdataset[j + yy][i] + addleft
    #right
    for i in range(len_x-xx, len_x):
        for j in range(0, len_y):
            gr = dataset[j][i-1] - dataset[j][i]
            gr = gr/xx
            dataright[j] = dataright[j] - gr

    for i in range(len_x+xx, len_x+xx+xx):
        for j in range(0, len_y):
            addright = dataset[j][len_x - 1] + dataright[j] * (i - len_x - xx + 1)
            expdataset[j + yy][i] = expdataset[j + yy][i] + addright

    #top
    for i in range(0, xnumber):
        for j in range(yy, yy+yy):
            gt = expdataset[j+1][i] - expdataset[j][i]
            gt = gt/yy
            datatop[i] = datatop[i] - gt

    for i in range(0, xnumber):
        for j in range(0, yy):
            addtop = expdataset[yy][i] + datatop[i] * (yy - j)
            expdataset[j][i] = expdataset[j][i] + addtop

    #bottom
    for i in range(0, xnumber):
        for j in range(len_y, len_y+yy):
            gb = expdataset[j-1][i] - expdataset[j][i]
            gb = gb/yy
            databottom[i] = databottom[i] - gb

    for i in range(0, xnumber):
        for j in range(len_y+yy, len_y+yy+yy):
            addbottom = expdataset[len_y+yy-1][i] + databottom[i] * (j - len_y - yy + 1)
            expdataset[j][i] = expdataset[j][i] + addbottom

    return expdataset
