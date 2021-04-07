import pandas as pd
import numpy as np


def read_excel(num):
    df = pd.read_excel('data\\qs_excel\\shanxi_20191120_{number}.xlsx'.format(number=num))
    P_1 = df.iloc[47439 - 2, 10] + df.iloc[47440 - 2, 10]  # 昱光有功
    Q_1 = df.iloc[47439 - 2, 11] + df.iloc[47440 - 2, 11]  # 昱光无功
    P_2 = df.iloc[47287 - 2, 10] + df.iloc[47288 - 2, 10] + df.iloc[47289 - 2, 10] + df.iloc[47290 - 2, 10]  # 河曲有功
    Q_2 = df.iloc[47487 - 2, 11] + df.iloc[47488 - 2, 11] + df.iloc[47289 - 2, 11] + df.iloc[47290 - 2, 11]  # 河曲无功
    P_3 = df.iloc[47317 - 2, 10] + df.iloc[47318 - 2, 10] + df.iloc[47319 - 2, 10] + df.iloc[47320 - 2, 10]  # 神头2有功
    Q_3 = df.iloc[47317 - 2, 11] + df.iloc[47318 - 2, 11] + df.iloc[47319 - 2, 11] + df.iloc[47320 - 2, 11]  # 神头2无功
    P_4 = df.iloc[47339 - 2, 10] + df.iloc[47340 - 2, 10] + df.iloc[47341 - 2, 10] + df.iloc[47342 - 2, 10] + \
          df.iloc[47343 - 2, 10] + df.iloc[47344 - 2, 10]  # 万家寨有功
    Q_4 = df.iloc[47339 - 2, 11] + df.iloc[47340 - 2, 11] + df.iloc[47341 - 2, 11] + df.iloc[47342 - 2, 11] + \
          df.iloc[47343 - 2, 11] + df.iloc[47344 - 2, 11]  # 万家寨无功
    P_5 = df.iloc[47447 - 2, 10] + df.iloc[47448 - 2, 10]  # 神泉有功
    Q_5 = df.iloc[47447 - 2, 11] + df.iloc[47448 - 2, 11]  # 神泉无功
    P_6 = df.iloc[47497 - 2, 10] + df.iloc[47498 - 2, 10]  # 锦华有功
    Q_6 = df.iloc[47497 - 2, 11] + df.iloc[47498 - 2, 11]  # 锦华无功
    P_7 = df.iloc[47415 - 2, 10] + df.iloc[47416 - 2, 10]  # 京玉有功
    Q_7 = df.iloc[47415 - 2, 11] + df.iloc[47416 - 2, 11]  # 京玉无功
    P_8 = df.iloc[47322 - 2, 10] + df.iloc[47323 - 2, 10] + df.iloc[47324 - 2, 10] + df.iloc[47325 - 2, 10]  # 塔山有功
    Q_8 = df.iloc[47322 - 2, 11] + df.iloc[47323 - 2, 11] + df.iloc[47324 - 2, 11] + df.iloc[47325 - 2, 11]  # 塔山无功
    return P_1, Q_1, P_2, Q_2, P_3, Q_3, P_4, Q_4, P_5, Q_5, P_6, Q_6, P_7, Q_7, P_8, Q_8


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
for i in range(24):
    p_1, q_1, p_2, q_2, p_3, q_3, p_4, q_4, p_5, q_5, p_6, q_6, p_7, q_7, p_8, q_8 = read_excel(i)
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
max_P = [max(listP_1), max(listP_2), max(listP_3), max(listP_4), max(listP_5), max(listP_6), max(listP_7), max(listP_8)]
min_P = [min(listP_1), min(listP_2), min(listP_3), min(listP_4), min(listP_5), min(listP_6), min(listP_7), min(listP_8)]
max_Q = [max(listQ_1), max(listQ_2), max(listQ_3), max(listQ_4), max(listQ_5), max(listQ_6), max(listQ_7), max(listQ_8)]
min_Q = [min(listQ_1), min(listQ_2), min(listQ_3), min(listQ_4), min(listQ_5), min(listQ_6), min(listQ_7), min(listQ_8)]
values = [max_P, min_P, max_Q, min_Q]
values = np.array(values).T

print(values)
result = pd.DataFrame(values,
                      index=['昱光', '河曲', '神二', '万家寨', '神泉', '锦华', '京玉', '塔山'],
                      columns=['max_P', 'min_P', 'max_Q', 'min_Q'])
result.to_csv('result\\发电机.csv')
