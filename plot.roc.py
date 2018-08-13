#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

path = "E:\\data.txt" # 文件路径
f = open(path) #打开文件
content = f.read().splitlines() # 读取并分割行，splitlines()默认按照'\n'分割
head = content[0] # 每列的head，如果没有head，此行可忽略
data_str = content[1:] # 此时数据以字符串的形式存入一个列表
data_num = [[]]*len(data_str) # 创建一个空列表，用以装入转后后的数据

# for循环用以将字符串形式的数据转换成数字，这一步结束就已经完成了转换了
# 转换后的数据存储在data_num中
for i in range(len(data_str)):
    data_num[i] = [float(x) for x in data_str[i].split(',')]
 
# 下面是利用numpy和matplotlib.pyplot进行数组转换和画图 
data_array = np.array(data_num) # 将数据转换成二维数组

# 下面将二维数组中的每一列存储到一个列向量中，以备画图
lamda = data_array[:, 0] 
s_lamda = data_array[:, 1]
n_bulk = data_array[:, 2]
k_bulk = data_array[:, 3]
n_1L = data_array[:, 4]
k_1L = data_array[:, 5]
n_si = data_array[:, 6]
k_si = data_array[:, 7]

# 下面是创建图形，并作图；利用上面的lamda作为x坐标轴，其余数据作为y，进行画图。
plt.figure()
plt.plot(lamda, s_lamda)
plt.figure()
plt.plot(lamda, n_bulk, lamda, k_bulk, lamda, n_1L, lamda, k_1L)
plt.figure()
plt.plot(lamda, n_si, lamda, k_si)
plt.show()