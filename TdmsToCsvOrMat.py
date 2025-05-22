from nptdms import TdmsFile
import numpy as np
from scipy import io
import matplotlib.pyplot as plt
from scipy.io import savemat
from scipy.signal import argrelextrema
#输入一个TDMS文件的路径
# 读取TDMS文件
with TdmsFile.open('E:\\DAQ\\DB\\STEPANDSPIKE_.tdms') as tdms_file:
    # 获取到第一个group
    last_grp = tdms_file.groups()[-1]

    # 获取到第一个 channel
    data = last_grp.channels()[0]
    print(len(data), data[0])
    # print(len(data))
    # print(type(data))
    
    state = 2136
    state_1 = state*6*10000

    data0 = np.array(data[state_1:state_1+10000])
    #寻找最小值,利用scipy库里的函数
    minima_indices = argrelextrema(data0, np.less, order=1000)[0]
    
    minima_y = data0[minima_indices]

    
    #画图并标注坐标
    plt.plot(data0)
    plt.scatter(minima_indices, minima_y, color='red', zorder=5, label='Local Minima')

# 标注坐标，方便知道dip的中心波长
for x_point, y_point in zip(minima_indices, minima_y):
    plt.annotate(
        f'({x_point:.2f}, {y_point:.2f})',
        (x_point, y_point),
        xytext=(0, 15),
        textcoords='offset points',
        ha='center',
        color='red',
        arrowprops=dict(arrowstyle="->", color='black', lw=0.5)
    )
    
    # print(data)保存的是光谱数据，保存为mat格式方便用matlab处理
    data_dict1 = {'d': data0}
     filename = 'E:\\DAQDATA\\DATA_2.mat'
     savemat(filename, data_dict1, long_field_names=True)
    res = []
    pos = 4702

    for i in range(1522):
        k = pos + i*10000
#distance 代表着光谱上那个dip大概的宽度/可以看着光谱改不要离太远了；
        distance = 600
        aim_range = data[k-distance:k+distance]
        min_val = min(aim_range)
        for j in range(k-distance, k+distance):
            if data[j]==min_val:
            res.append(j-i*10000)
            pos = j-i*10000
    res = np.array(res)
# 输出目录修改为自己要保存的目录，这里保存的是中心波长的坐标数据
    np.savetxt('E:\\data.csv', res, delimiter=',')