import numpy as np

def read_txt(txt_path):
    f = open(txt_path)
    data_lists = f.readlines()  # 读出的是str类型
    global dataset
    dataset = []
    # 对每一行作循环
    for data in data_lists:
        data1 = data.strip('\n')  # 去掉开头和结尾的换行符
        data2 = data1.split(',')  # 把,作为间隔符
        dataset.append(data2)  # 把这一行的结果作为元素加入列表dataset

    dataset = np.array(dataset)
    f.close()

    return dataset
