import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

sns.set_theme(style="darkgrid")
df = pd.read_excel('result\\result.xlsx')
# histogram
# scaler = StandardScaler()
# data = scaler.fit_transform(df)
fig, ax = plt.subplots(figsize=(8, 5))
sns.distplot(df.水头无功投入, kde=False)
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体”黑体“
ax.set(xlabel="Reactive power input in Shuitou substation/MVA", ylabel='/%')
plt.show()
fig.savefig("result\\Shuitou.png")