import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def gaussian_weighted_moving_average(signal, window_size, sigma):
    """高斯加权移动平均滤波函数"""
    # 生成高斯权重
    t = np.linspace(-window_size // 2, window_size // 2, window_size)
    weight = np.exp(-t**2 / (2 * sigma**2))
    weight /= np.sum(weight)  # 归一化权重
    # 应用卷积计算加权平均
    return np.convolve(signal, weight, mode='same')

# 读取CSV文件
# 请将文件名替换为你的CSV文件路径
file_path = 'C:\\Users\\zhangyu\\Desktop\\re29.csv'  # 例如: 'sensor_data.csv'
df = pd.read_csv(file_path)

# 请根据你的数据修改以下参数
time_column = 'time'  # 时间列的名称，如果没有时间列可以使用索引
data_column = 'CH1V'  # 需要滤波的数据列名称
window_size = 15       # 窗口大小，可根据数据特点调整
sigma = 3              # 高斯分布的标准差，可根据数据特点调整

# 提取数据
if time_column in df.columns:
    t = df[time_column].values
else:
    t = np.arange(len(df))  # 如果没有时间列，使用索引作为时间轴

original_signal = df[data_column].values

# 进行滤波
filtered_signal = gaussian_weighted_moving_average(original_signal, window_size, sigma)

# 可视化结果
plt.figure(figsize=(12, 6))
plt.plot(t, original_signal, label='原始数据', alpha=0.5)
plt.plot(t, filtered_signal, label='滤波后数据', linewidth=2)
plt.xlabel('时间')
plt.ylabel('数值')
plt.title('高斯加权移动平均滤波结果')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# 保存滤波后的数据到新的CSV文件
df['filtered_' + data_column] = filtered_signal
output_file = 'C:\\Users\\zhangyu\\Desktop\\out\\29_.csv'
df.to_csv(output_file, index=False)
print(f"滤波后的数据已保存到: {output_file}")