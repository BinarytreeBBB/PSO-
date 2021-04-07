import pandas as pd
import numpy as np


def read_excel(num):
    df = pd.read_excel('data\\qs_excel\\shanxi_20191120_{number}.xlsx'.format(number=num))
    df.columns = np.arange(62)
    P_1 = df.loc[49000 - 2:49017 - 2, 8].sum()  # 右玉有功
    Q_1 = df.loc[49000 - 2:49017 - 2, 9].sum()  # 右玉无功
    P_2 = df.loc[48966 - 2:48988 - 2, 8].sum()  # 向阳堡有功
    Q_2 = df.loc[48966 - 2:48988 - 2, 9].sum()  # 向阳堡无功
    P_3 = df.loc[48919 - 2:48934 - 2, 8].sum()  # 翠微有功
    Q_3 = df.loc[48919 - 2:48934 - 2, 9].sum()  # 翠微无功
    P_4 = df.loc[48951 - 2:48986 - 2, 8].sum()  # 七里沟有功
    Q_4 = df.loc[48951 - 2:48986 - 2, 9].sum()  # 七里沟无功
    P_5 = df.loc[49063 - 2:49073 - 2, 8].sum()  # 水头有功
    Q_5 = df.loc[49063 - 2:49073 - 2, 9].sum()  # 水头无功
    P_6 = df.loc[49639 - 2:49652 - 2, 8].sum()  # 方城有功
    Q_6 = df.loc[49639 - 2:49652 - 2, 9].sum()  # 方城无功
    P_7 = df.loc[49653 - 2:49663 - 2, 8].sum()  # 古渡有功
    Q_7 = df.loc[49653 - 2:49663 - 2, 9].sum()  # 古渡无功
    P_8 = df.loc[48935 - 2:48950 - 2, 8].sum()  # 铺上有功
    Q_8 = df.loc[48935 - 2:48950 - 2, 9].sum()  # 铺上无功
    P_9 = df.loc[48909 - 2:48918 - 2, 8].sum()  # 安荣有功
    Q_9 = df.loc[48909 - 2:48918 - 2, 9].sum()  # 安荣无功
    P_10 = df.loc[49036 - 2:49048 - 2, 8].sum()  # 吉庄有功
    Q_10 = df.loc[49036 - 2:49048 - 2, 9].sum()  # 吉庄无功
    P_11 = df.loc[49621 - 2:49638 - 2, 8].sum()  # 繁峙有功
    Q_11 = df.loc[49621 - 2:49638 - 2, 9].sum()  # 繁峙无功

    return P_1, Q_1, P_2, Q_2, P_3, Q_3, P_4, Q_4, P_5, Q_5, P_6, Q_6, P_7, Q_7, P_8, Q_8, P_9, Q_9\
        , P_10, Q_10, P_11, Q_11


listP_1 = []
listQ_1 = []
listP_2 = []
listQ_2 = []
listP_3 = []
listQ_3 = []
listP_4 = []
listQ_4 = []
listP_5 = []
listQ_5 = []
listP_6 = []
listQ_6 = []
listP_7 = []
listQ_7 = []
listP_8 = []
listQ_8 = []
listP_9 = []
listQ_9 = []
listP_10 = []
listQ_10 = []
listP_11 = []
listQ_11 = []
for i in range(24):
    p_1, q_1, p_2, q_2, p_3, q_3, p_4, q_4, p_5, q_5, p_6, q_6, p_7, q_7, p_8, q_8, p_9, q_9, p_10, q_10\
        , p_11, q_11 = read_excel(i)
    listP_1.append(p_1)
    listQ_1.append(q_1)
    listP_2.append(p_2)
    listQ_2.append(q_2)
    listP_3.append(p_3)
    listQ_3.append(q_3)
    listP_4.append(p_4)
    listQ_4.append(q_4)
    listP_5.append(p_5)
    listQ_5.append(q_5)
    listP_6.append(p_6)
    listQ_6.append(q_6)
    listP_7.append(p_7)
    listQ_7.append(q_7)
    listP_8.append(p_8)
    listQ_8.append(q_8)
    listP_9.append(p_9)
    listQ_9.append(q_9)
    listP_10.append(p_10)
    listQ_10.append(q_10)
    listP_11.append(p_11)
    listQ_11.append(q_11)
max_P = [max(listP_1), max(listP_2), max(listP_3), max(listP_4), max(listP_5), max(listP_6), max(listP_7),
         max(listP_8), max(listP_9), max(listP_10), max(listP_11)]
min_P = [min(listP_1), min(listP_2), min(listP_3), min(listP_4), min(listP_5), min(listP_6), min(listP_7),
         min(listP_8), min(listP_9), min(listP_10), min(listP_11)]
max_Q = [max(listQ_1), max(listQ_2), max(listQ_3), max(listQ_4), max(listQ_5), max(listQ_6), max(listQ_7),
         max(listQ_8), max(listQ_9), max(listQ_10), max(listQ_11)]
min_Q = [min(listQ_1), min(listQ_2), min(listQ_3), min(listQ_4), min(listQ_5), min(listQ_6), min(listQ_7),
         min(listQ_8), min(listQ_9), min(listQ_10), min(listQ_11)]
values = [max_P, min_P, max_Q, min_Q]
values = np.array(values).T

print(values)
result = pd.DataFrame(values,
                      index=['右玉', '向阳堡', '翠微', '七里沟', '水头', '方城', '古渡', '铺上', '安荣', '吉庄', '繁峙'],
                      columns=['max_P', 'min_P', 'max_Q', 'min_Q'])
result.to_csv('result\\负荷.csv')
