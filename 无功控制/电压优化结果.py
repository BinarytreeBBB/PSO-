import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('result\\数据输出\\result_1.xlsx')

x = np.linspace(1, 9, 9)
col = 8
y1, y2 = [], []
for i in range(9):
    if i < 5:
        ori = df.iloc[col, i * 2 + 5]/220
        opt = df.iloc[col, i * 2 + 6]/220
    else:
        ori = df.iloc[col, i * 2 + 5]/500
        opt = df.iloc[col, i * 2 + 6]/500
    y1.append(ori)
    y2.append(opt)
fig, ax = plt.subplots()
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体”黑体“
plt.plot(x, y1, 'o-', label='初始电压偏差')
plt.plot(x, y2, 'o-', label='优化电压偏差')
ax.set(xlabel='母线编号', ylabel='电压偏差(p.u.)')
plt.legend()
fig.savefig("result\\电压优化结果\\电压优化结果8.png")
plt.show()
