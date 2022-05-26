from geoist.pfm import pftrans
import numpy as np

def upward_continuation(dataset, expdeep, znum, xcount, ycount, x, y):

    newdata = np.zeros((xcount, ycount, znum+1))
    dataset = dataset.reshape(xcount, ycount)

    for i in range(0, xcount):
        for j in range(0, ycount):
            newdata[i][j][0] = newdata[i][j][0] + dataset[i][j]

    deepgroup = np.linspace(0, expdeep, num=znum+1, endpoint=True)
    ix = len(deepgroup)
    shape = (xcount, ycount)
    for i in range(1, ix):
        height = deepgroup[i]
        bgas_contf = pftrans.upcontinue(x, y, dataset, shape, height)
        bgas_contf = bgas_contf.reshape(xcount, ycount)
        for m in range(0, xcount):
            for n in range(0, ycount):
                newdata[m][n][i] = newdata[m][n][i] + bgas_contf[m][n]
    return newdata