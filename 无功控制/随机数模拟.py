import sys
import pandas as pd
import numpy as np
import pyswarms as ps


def cost_function(x):  # 损失函数，输入x是一个数组
    ldf = app.GetFromStudyCase("ComLdf")  # 获取研究案例里的潮流计算赋予ldf
    comSh = app.GetFromStudyCase("ComSh")  # 结果输出
    outputWindow = app.GetOutputWindow()  # 结果窗口

    def get_dev(df):
        str1 = df.iloc[545, 0]  # 水头
        str2 = df.iloc[593, 0]  # 右玉
        str3 = df.iloc[523, 0]  # 明海21
        str4 = df.iloc[551, 0]  # 朔州21
        str5 = df.iloc[576, 0]  # 向阳堡
        str6 = df.iloc[119, 0]  # 朔州51
        str7 = df.iloc[99, 0]  # 明海51
        str8 = df.iloc[116, 0]  # 神泉
        str9 = df.iloc[286, 0]  # 晋晋换

        s1 = str1.split()  # 切分字符串
        s2 = str2.split()
        s3 = str3.split()
        s4 = str4.split()
        s5 = str5.split()
        s6 = str6.split()
        s7 = str7.split()
        s8 = str8.split()
        s9 = str9.split()

        Ul1 = float(s1[4])  # 字符串列表第5个元素为Ul，转化为浮点数
        Ul2 = float(s2[4])
        Ul3 = float(s3[4])
        Ul4 = float(s4[4])
        Ul5 = float(s5[4])
        Ul6 = float(s6[4])
        Ul7 = float(s7[4])
        Ul8 = float(s8[4])
        Ul9 = float(s9[3])

        dev = abs(Ul1-220)/220+abs(Ul2-220)/220+abs(Ul3-220)/220+abs(Ul4-220)/220+abs(Ul5-220)/220+\
               abs(Ul6-500)/500+abs(Ul7-500)/500+abs(Ul8-500)/500+abs(Ul9-500)/500
        return dev  # 电压偏差

    def get_loss(df):
        def lineploss(loc):
            str_1 = df.iloc[loc - 2, 0]
            str_2 = df.iloc[loc - 1, 0]
            s_1 = str_1.split()
            s_2 = str_2.split()
            P_1 = float(s_1[5])
            P_2 = float(s_2[2])
            ploss = abs(P_1 + P_2)
            return ploss
        p_loss = lineploss(778) + lineploss(710) + lineploss(225) + lineploss(688) + \
                 lineploss(748)  # 右玉-明海；水头-明海；明海-晋换；京玉-右玉；水头-朔州
        return p_loss

    def action(rate):  # 调整风电同时率
        for para in D_01:
            para.ngnum = int(100 * rate)
        for para in D_02:
            para.ngnum = int(100 * rate)
        for para in D_03:
            para.ngnum = int(100 * rate)
        for para in D_04:
            para.ngnum = int(100 * rate)
        for para in P_02:
            para.ngnum = int(100 * rate)
        for para in P_03:
            para.ngnum = int(100 * rate)
        for para in P_04:
            para.ngnum = int(100 * rate)
        for para in P_05:
            para.ngnum = int(100 * rate)
        for para in P_06:
            para.ngnum = int(100 * rate)
        for para in P_07:
            para.ngnum = int(100 * rate)
        for para in P_08:
            para.ngnum = int(100 * rate)
        for para in P_09:
            para.ngnum = int(100 * rate)
        for para in P_10:
            para.ngnum = int(100 * rate)
        for para in P_11:
            para.ngnum = int(100 * rate)

    def reset():   # 复位函数
        for para in C_1:
            para.ncapa = 0
        for para in L_1:
            para.ncapa = 0
        for para in C_2:
            para.ncapa = 0
        for para in L_2:
            para.ncapa = 0

    C_1 = app.GetCalcRelevantObjects("右玉C.ElmShnt")
    L_1 = app.GetCalcRelevantObjects("右玉L.ElmShnt")
    C_2 = app.GetCalcRelevantObjects("水头C.ElmShnt")
    L_2 = app.GetCalcRelevantObjects("水头L.ElmShnt")

    D_01 = app.GetCalcRelevantObjects("DFIG 01.ElmAsm")
    D_02 = app.GetCalcRelevantObjects("DFIG 02.ElmAsm")
    D_03 = app.GetCalcRelevantObjects("DFIG 03.ElmAsm")
    D_04 = app.GetCalcRelevantObjects("DFIG 04.ElmAsm")
    P_02 = app.GetCalcRelevantObjects("PMSG 02.ElmGenstat")
    P_03 = app.GetCalcRelevantObjects("PMSG 03.ElmGenstat")
    P_04 = app.GetCalcRelevantObjects("PMSG 04.ElmGenstat")
    P_05 = app.GetCalcRelevantObjects("PMSG 05.ElmGenstat")
    P_06 = app.GetCalcRelevantObjects("PMSG 06.ElmGenstat")
    P_07 = app.GetCalcRelevantObjects("PMSG 07.ElmGenstat")
    P_08 = app.GetCalcRelevantObjects("PMSG 08.ElmGenstat")
    P_09 = app.GetCalcRelevantObjects("PMSG 09.ElmGenstat")
    P_10 = app.GetCalcRelevantObjects("PMSG 10.ElmGenstat")
    P_11 = app.GetCalcRelevantObjects("PMSG 11.ElmGenstat")

    C = []
    for i in range(n_particles):  # 每个粒子循环一次
        reset()

        action(0.5)  # 调整风电同时率,0.5表示50%
        '''并补投切'''
        for para in C_1:
            para.ncapa = int(x[:, 0][i])
        for para in L_1:
            para.ncapa = int(x[:, 1][i])
        for para in C_2:
            para.ncapa = int(x[:, 2][i])
        for para in L_2:
            para.ncapa = int(x[:, 3][i])

        ldf.Execute()  # 执行潮流计算
        outputWindow.Clear()  # 清空输出窗口
        comSh.iopt_cmd = 3  # complete system report
        comSh.iopt_vpr = 1  # voltage profiles
        comSh.Execute()  # 结果输出
        outputWindow.Save('dataflow\\ldf.txt')  # 保存结果窗口
        dataframe1 = pd.read_fwf('dataflow\\ldf.txt')  # pandas读取txt文件

        outputWindow.Clear()  # 清空输出窗口
        comSh.iopt_cmd = 4  # Edge element
        comSh.Execute()  # 结果输出
        outputWindow.Save('dataflow\\edge.txt')  # 保存结果窗口
        dataframe2 = pd.read_fwf('dataflow\\edge.txt')  # pandas读取txt文件

        delta_U = get_dev(dataframe1)
        loss = get_loss(dataframe2)
        f1 = delta_U
        f2 = loss/200

        C.append(f1 + f2)

        reset()  # 复位
    return C


def pso():
    # Set-up hyperparameters
    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.8}

    # Create bounds
    max_bound = [60, 60, 60, 60]
    min_bound = [0, 0, 0, 0]
    bounds = (min_bound, max_bound)

    # Call instance of PSO
    global n_particles  # 全局变量
    n_particles = 10
    optimizer = ps.single.GlobalBestPSO(n_particles=n_particles, dimensions=4, options=options, bounds=bounds)

    # Perform optimization
    cost, pos = optimizer.optimize(cost_function, iters=20)
    return cost, pos


def ldf():
    ldf = app.GetFromStudyCase("ComLdf")  # 获取研究案例里的潮流计算赋予ldf
    comSh = app.GetFromStudyCase("ComSh")  # 结果输出
    outputWindow = app.GetOutputWindow()  # 结果窗口
    ldf.Execute()  # 执行潮流计算
    outputWindow.Clear()  # 清空输出窗口
    comSh.iopt_cmd = 3  # complete system report
    comSh.iopt_vpr = 1  # voltage profiles
    comSh.Execute()  # 结果输出
    outputWindow.Save('ldf.txt')  # 保存结果窗口
    df = pd.read_fwf('ldf.txt')  # pandas读取txt文件

    str1 = df.iloc[545, 0]  # 水头
    str2 = df.iloc[593, 0]  # 右玉
    str3 = df.iloc[523, 0]  # 明海21
    str4 = df.iloc[551, 0]  # 朔州21
    str5 = df.iloc[576, 0]  # 向阳堡
    str6 = df.iloc[119, 0]  # 朔州51
    str7 = df.iloc[99, 0]  # 明海51
    str8 = df.iloc[116, 0]  # 神泉
    str9 = df.iloc[286, 0]  # 晋晋换

    s1 = str1.split()  # 切分字符串
    s2 = str2.split()
    s3 = str3.split()
    s4 = str4.split()
    s5 = str5.split()
    s6 = str6.split()
    s7 = str7.split()
    s8 = str8.split()
    s9 = str9.split()

    Ul1 = float(s1[4])  # 字符串列表第5个元素为Ul，转化为浮点数
    Ul2 = float(s2[4])
    Ul3 = float(s3[4])
    Ul4 = float(s4[4])
    Ul5 = float(s5[4])
    Ul6 = float(s6[4])
    Ul7 = float(s7[4])
    Ul8 = float(s8[4])
    Ul9 = float(s9[3])

    cost = abs(Ul1 - 220) + abs(Ul2 - 220) + abs(Ul3 - 220) + abs(Ul4 - 220) + abs(Ul5 - 220) + \
           abs(Ul6 - 500) + abs(Ul7 - 500) + abs(Ul8 - 500) + abs(Ul9 - 500)
    return cost, abs(Ul1 - 220), abs(Ul2 - 220), abs(Ul3 - 220), abs(Ul4 - 220), abs(Ul5 - 220), \
           abs(Ul6 - 500), abs(Ul7 - 500), abs(Ul8 - 500), abs(Ul9 - 500)  # 电压偏差


def Loss():
    ldf = app.GetFromStudyCase("ComLdf")  # 获取研究案例里的潮流计算赋予ldf
    comSh = app.GetFromStudyCase("ComSh")  # 结果输出
    outputWindow = app.GetOutputWindow()  # 结果窗口
    ldf.Execute()  # 执行潮流计算
    outputWindow.Clear()  # 清空输出窗口
    comSh.iopt_cmd = 4  # Edge element
    comSh.Execute()  # 结果输出
    outputWindow.Save('dataflow\\edge.txt')  # 保存结果窗口
    df = pd.read_fwf('dataflow\\edge.txt')  # pandas读取txt文件

    def lineploss(loc):
        str_1 = df.iloc[loc - 2, 0]
        str_2 = df.iloc[loc - 1, 0]
        s_1 = str_1.split()
        s_2 = str_2.split()
        P_1 = float(s_1[5])
        P_2 = float(s_2[2])
        ploss = abs(P_1 + P_2)
        return ploss
    p_loss = lineploss(778) + lineploss(710) + lineploss(225) + lineploss(688) + \
                lineploss(748)  # 右玉-明海；水头-明海；明海-晋换；京玉-右玉；水头-朔州
    return p_loss


def set_variable(df1, df2):
    def gen1():
        P = np.random.uniform(df1.loc[0, 'min_P'] * 0.8, 300)  # 昱光满发300MW
        Q = np.random.uniform(df1.loc[0, 'min_Q'], df1.loc[0, 'max_Q'] * 1.2)
        gen = app.GetCalcRelevantObjects("昱光.ElmSym")
        for para in gen:
            para.pgini = P / para.ngnum
            para.qgini = Q / para.ngnum
        return P, Q

    def gen2():
        P = np.random.uniform(df1.loc[1, 'min_P'] * 0.8, 2400)  # 河曲满发2400MW
        Q = np.random.uniform(df1.loc[1, 'min_Q'], df1.loc[1, 'max_Q'] * 1.2)
        gen = app.GetCalcRelevantObjects("hequ2.ElmSym")
        for para in gen:
            para.pgini = P / para.ngnum
            para.qgini = Q / para.ngnum
        return P, Q

    def gen3():
        P = np.random.uniform(df1.loc[2, 'min_P'] * 0.8, 1500)  # 神头2满发1500MW
        Q = np.random.uniform(df1.loc[2, 'min_Q'], df1.loc[2, 'max_Q'] * 1.2)
        gen = app.GetCalcRelevantObjects("shener3.ElmSym")
        for para in gen:
            para.pgini = P / para.ngnum
            para.qgini = Q / para.ngnum
        return P, Q

    def gen4():
        P = np.random.uniform(df1.loc[3, 'min_P'] * 0.8, df1.loc[3, 'max_P'] * 1.2)
        Q = np.random.uniform(df1.loc[3, 'min_Q'], df1.loc[3, 'max_Q'] * 1.2)
        gen = app.GetCalcRelevantObjects("万家寨.Genstat")
        for para in gen:
            para.pgini = P / para.ngnum
            para.qgini = Q / para.ngnum
        return P, Q

    def gen5():
        P = np.random.uniform(df1.loc[4, 'min_P'] * 0.8, 1200)  # 神泉满发1200MW
        Q = np.random.uniform(df1.loc[4, 'min_Q'], df1.loc[4, 'max_Q'] * 1.2)
        gen = app.GetCalcRelevantObjects("shenquan1.ElmSym")
        for para in gen:
            para.pgini = P / para.ngnum
            para.qgini = Q / para.ngnum
        return P, Q

    def gen6():
        P = np.random.uniform(df1.loc[5, 'min_P'] * 0.8, 700)  # 锦华满发700MW
        Q = np.random.uniform(df1.loc[5, 'min_Q'], df1.loc[5, 'max_Q'] * 1.2)
        gen = app.GetCalcRelevantObjects("锦华.ElmSym")
        for para in gen:
            para.pgini = P / para.ngnum
            para.qgini = Q / para.ngnum
        return P, Q

    def gen7():
        P = np.random.uniform(df1.loc[6, 'min_P'] * 0.8, 660)  # 京玉满发660MW
        Q = np.random.uniform(df1.loc[6, 'min_Q'], df1.loc[6, 'max_Q'] * 1.2)
        gen = app.GetCalcRelevantObjects("京玉.ElmSym")
        for para in gen:
            para.pgini = P / para.ngnum
            para.qgini = Q / para.ngnum
        return P, Q

    def gen8():
        P = np.random.uniform(df1.loc[7, 'min_P'] * 0.8, 2520)  # 塔山满发2520MW
        Q = np.random.uniform(df1.loc[7, 'min_Q'], df1.loc[7, 'max_Q'] * 1.2)
        gen = app.GetCalcRelevantObjects("tashan1.ElmSym")
        for para in gen:
            para.pgini = P / para.ngnum
            para.qgini = Q / para.ngnum
        return P, Q

    def load1():
        P = np.random.uniform(df2.loc[0, 'min_P'] * 1.2, df2.loc[0, 'max_P'] * 1.2)
        Q = np.random.uniform(df2.loc[0, 'min_Q'] * 1.2, df2.loc[0, 'max_Q'] * 1.2)
        lod = app.GetCalcRelevantObjects("右玉.ElmLod")
        for para in lod:
            para.plini = P
            para.qlini = Q
        return P, Q

    def load2():
        P = np.random.uniform(df2.loc[1, 'min_P'] * 0.8, df2.loc[1, 'max_P'] * 1.2)
        Q = np.random.uniform(df2.loc[1, 'min_Q'] * 0.8, df2.loc[1, 'max_Q'] * 1.2)
        lod = app.GetCalcRelevantObjects("向阳堡.ElmLod")
        for para in lod:
            para.plini = P
            para.qlini = Q
        return P, Q

    def load3():
        P = np.random.uniform(df2.loc[2, 'min_P'] * 1.2, df2.loc[2, 'max_P'] * 1.2)
        Q = np.random.uniform(df2.loc[2, 'min_Q'] * 0.8, df2.loc[2, 'max_Q'] * 1.2)
        lod = app.GetCalcRelevantObjects("翠微.ElmLod")
        for para in lod:
            para.plini = P
            para.qlini = Q
        return P, Q

    def load4():
        P = np.random.uniform(df2.loc[3, 'min_P'] * 0.8, df2.loc[3, 'max_P'] * 1.2)
        Q = np.random.uniform(df2.loc[3, 'min_Q'] * 0.8, df2.loc[3, 'max_Q'] * 1.2)
        lod = app.GetCalcRelevantObjects("七里沟.ElmLod")
        for para in lod:
            para.plini = P
            para.qlini = Q
        return P, Q

    def load5():
        P = np.random.uniform(df2.loc[4, 'min_P'] * 0.8, df2.loc[4, 'max_P'] * 1.2)
        Q = np.random.uniform(df2.loc[4, 'min_Q'] * 1.2, df2.loc[4, 'max_Q'] * 1.2)
        lod = app.GetCalcRelevantObjects("水头.ElmLod")
        for para in lod:
            para.plini = P
            para.qlini = Q
        return P, Q

    def load6():
        P = np.random.uniform(df2.loc[5, 'min_P'] * 0.8, df2.loc[5, 'max_P'] * 1.2)
        Q = np.random.uniform(df2.loc[5, 'min_Q'] * 1.2, df2.loc[5, 'max_Q'] * 1.2)
        lod = app.GetCalcRelevantObjects("方城.ElmLod")
        for para in lod:
            para.plini = P
            para.qlini = Q
        return P, Q

    def load7():
        P = np.random.uniform(df2.loc[6, 'min_P'] * 0.8, df2.loc[6, 'max_P'] * 1.2)
        Q = np.random.uniform(df2.loc[6, 'min_Q'] * 0.8, df2.loc[6, 'max_Q'] * 1.2)
        lod = app.GetCalcRelevantObjects("古渡.ElmLod")
        for para in lod:
            para.plini = P
            para.qlini = Q
        return P, Q

    def load8():
        P = np.random.uniform(df2.loc[7, 'min_P'] * 0.8, df2.loc[7, 'max_P'] * 1.2)
        Q = np.random.uniform(df2.loc[7, 'min_Q'] * 0.8, df2.loc[7, 'max_Q'] * 1.2)
        lod = app.GetCalcRelevantObjects("铺上.ElmLod")
        for para in lod:
            para.plini = P
            para.qlini = Q
        return P, Q

    def load9():
        P = np.random.uniform(df2.loc[8, 'min_P'] * 0.8, df2.loc[8, 'max_P'] * 1.2)
        Q = np.random.uniform(df2.loc[8, 'min_Q'] * 0.8, df2.loc[8, 'max_Q'] * 1.2)
        lod = app.GetCalcRelevantObjects("安荣.ElmLod")
        for para in lod:
            para.plini = P
            para.qlini = Q
        return P, Q

    def load10():
        P = np.random.uniform(df2.loc[9, 'min_P'] * 1.2, df2.loc[9, 'max_P'] * 1.2)
        Q = np.random.uniform(df2.loc[9, 'min_Q'] * 0.8, df2.loc[9, 'max_Q'] * 1.2)
        lod = app.GetCalcRelevantObjects("吉庄.ElmLod")
        for para in lod:
            para.plini = P
            para.qlini = Q
        return P, Q

    def load11():
        P = np.random.uniform(df2.loc[10, 'min_P'] * 0.8, df2.loc[10, 'max_P'] * 1.2)
        Q = np.random.uniform(df2.loc[10, 'min_Q'] * 0.8, df2.loc[10, 'max_Q'] * 1.2)
        lod = app.GetCalcRelevantObjects("繁峙.ElmLod")
        for para in lod:
            para.plini = P
            para.qlini = Q
        return P, Q

    PG1, QG1 = gen1()
    PG2, QG2 = gen2()
    PG3, QG3 = gen3()
    PG4, QG4 = gen4()
    PG5, QG5 = gen5()
    PG6, QG6 = gen6()
    PG7, QG7 = gen7()
    PG8, QG8 = gen8()

    PL1, QL1 = load1()
    PL2, QL2 = load2()
    PL3, QL3 = load3()
    PL4, QL4 = load4()
    PL5, QL5 = load5()
    PL6, QL6 = load6()
    PL7, QL7 = load7()
    PL8, QL8 = load8()
    PL9, QL9 = load9()
    PL10, QL10 = load10()
    PL11, QL11 = load11()
    return PG1, QG1, PG2, QG2, PG3, QG3, PG4, QG4, PG5, QG5, PG6, QG6, PG7, QG7, PG8, QG8, \
           PL1, QL1, PL2, QL2, PL3, QL3, PL4, QL4, PL5, QL5, PL6, QL6, PL7, QL7, PL8, QL8, PL9, QL9, \
           PL10, QL10, PL11, QL11


if __name__ == "__main__":
    sys.path.append(r"E:\\DIgSILENT\\DIgSILENT 2018\\Python\\3.6")  # 自定义路径中寻找sys模块
    import powerfactory as pf  # 引入PowerFactory模块，与DIgSILENT对接

    app = pf.GetApplication()
    app.Show()  # 显示digsilent界面
    user = app.GetCurrentUser()  # 获取对应的用户
    projects = user.GetContents('*.IntPrj')[0]  # 从用户中获取所有项目
    project = projects.GetContents()[0]  # 从所有项目中找到指定的项目
    case = project.GetContents()[0]  # 找到项目下的算例
    case.Activate()  # 激活算例

    data1 = pd.read_csv('result/发电机.csv')
    data2 = pd.read_csv('result/负荷.csv')

    Ori_bias = []
    Best_bias = []
    Ori_loss = []
    Best_loss = []
    Pos_1 = []
    Pos_2 = []
    U1, U2, U3, U4, U5, U6, U7, U8, U9 = [], [], [], [], [], [], [], [], []
    U_1, U_2, U_3, U_4, U_5, U_6, U_7, U_8, U_9 = [], [], [], [], [], [], [], [], []
    P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19 = \
        [], [], [], [], [], [], [] ,[], [], [], [], [], [], [], [], [], [], [], []
    Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19 = \
        [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

    for i in range(8):
        print(i)
        pg1, qg1, pg2, qg2, pg3, qg3, pg4, qg4, pg5, qg5, pg6, qg6, pg7, qg7, pg8, qg8, \
        pl1, ql1, pl2, ql2, pl3, ql3, pl4, ql4, pl5, ql5, pl6, ql6, pl7, ql7, pl8, ql8, pl9, ql9, \
        pl10, ql10, pl11, ql11 = set_variable(data1, data2)

        P1.append(pg1)  # 保存随机产生的发电站数据
        Q1.append(qg1)
        P2.append(pg2)
        Q2.append(qg2)
        P3.append(pg3)
        Q3.append(qg3)
        P4.append(pg4)
        Q4.append(qg4)
        P5.append(pg5)
        Q5.append(qg5)
        P6.append(pg6)
        Q6.append(qg6)
        P7.append(pg7)
        Q7.append(qg7)
        P8.append(pg8)
        Q8.append(qg8)

        P9.append(pl1)  # 保存随机产生的负荷数据
        Q9.append(ql1)
        P10.append(pl2)
        Q10.append(ql2)
        P11.append(pl3)
        Q11.append(ql3)
        P12.append(pl4)
        Q12.append(ql4)
        P13.append(pl5)
        Q13.append(ql5)
        P14.append(pl6)
        Q14.append(ql6)
        P15.append(pl7)
        Q15.append(ql7)
        P16.append(pl8)
        Q16.append(ql8)
        P17.append(pl9)
        Q17.append(ql9)
        P18.append(pl10)
        Q18.append(ql10)
        P19.append(pl11)
        Q19.append(ql11)

        r, u1, u2, u3, u4, u5, u6, u7, u8, u9 = ldf()
        r1 = Loss()
        Ori_bias.append(r)
        Ori_loss.append(r1)
        U1.append(u1)
        U2.append(u2)
        U3.append(u3)
        U4.append(u4)
        U5.append(u5)
        U6.append(u6)
        U7.append(u7)
        U8.append(u8)
        U9.append(u9)

        bias, position = pso()
        Best_bias.append(bias)
        Pos_1.append(5 * (int(position[0]) - int(position[1])))
        Pos_2.append(5 * (int(position[2]) - int(position[3])))

        C_1 = app.GetCalcRelevantObjects("右玉C.ElmShnt")
        L_1 = app.GetCalcRelevantObjects("右玉L.ElmShnt")
        C_2 = app.GetCalcRelevantObjects("水头C.ElmShnt")
        L_2 = app.GetCalcRelevantObjects("水头L.ElmShnt")

        for para in C_1:
            para.ncapa = int(position[0])
        for para in L_1:
            para.ncapa = int(position[1])
        for para in C_2:
            para.ncapa = int(position[2])
        for para in L_2:
            para.ncapa = int(position[3])

        r, u_1, u_2, u_3, u_4, u_5, u_6, u_7, u_8, u_9 = ldf()
        r2 = Loss()
        Best_loss.append(r2)
        U_1.append(u_1)
        U_2.append(u_2)
        U_3.append(u_3)
        U_4.append(u_4)
        U_5.append(u_5)
        U_6.append(u_6)
        U_7.append(u_7)
        U_8.append(u_8)
        U_9.append(u_9)

        for para in C_1:  # 复位
            para.ncapa = 0
        for para in L_1:
            para.ncapa = 0
        for para in C_2:
            para.ncapa = 0
        for para in L_2:
            para.ncapa = 0

    result = pd.DataFrame({'总初始电压偏差': Ori_bias, '总优化电压偏差': Best_bias, '初始网损':Ori_loss, '优化网损':Best_loss,
                           '右玉无功补偿': Pos_1, '水头无功补偿': Pos_2, '水头初始电压偏差': U1, '水头优化电压偏差': U_1,
                           '右玉初始电压偏差': U2, '右玉优化电压偏差':U_2, '明海21初始电压偏差': U3, '明海21优化电压偏差': U_3,
                           '朔州21初始电压偏差': U4, '朔州21优化电压偏差': U_4, '向阳堡初始电压偏差': U5, '向阳堡优化电压偏差': U_5,
                           '朔州51初始电压偏差': U6, '朔州51优化电压偏差': U_6, '明海51初始电压偏差': U7, '明海51优化电压偏差': U_7,
                           '神泉初始电压偏差': U8, '神泉优化电压偏差': U_8, '晋换初始电压偏差': U9, '晋换优化电压偏差': U_9,
                           '昱光发电站有功': P1, '昱光发电站无功': Q1, '河曲发电站有功': P2, '河曲发电站无功': Q2,
                           '神二发电站有功': P3, '神二发电站无功': Q3, '万家寨发电站有功': P4,
                           '万家寨发电站无功': Q4, '神泉发电站有功': P5, '神泉发电站无功': Q5,
                           '锦华发电站有功': P6, '锦华发电站无功': Q6, '京玉发电站有功': P7,
                           '京玉发电站无功': Q7, '塔山发电站有功': P8, '塔山发电站无功': Q8,
                           '右玉负荷有功': P9, '右玉负荷无功': Q9, '向阳堡负荷有功': P10,
                           '向阳堡负荷无功': Q10, '翠微负荷有功': P11, '翠微负荷无功': Q11,
                           '七里沟负荷有功': P12, '七里沟负荷无功': Q12, '水头负荷有功': P13,
                           '水头负荷无功': Q13, '方城负荷有功': P14, '方城负荷无功': Q14,
                           '古渡负荷有功': P15, '古渡负荷无功': Q15, '铺上负荷有功': P16,
                           '铺上负荷无功': Q16, '安荣负荷有功': P17, '安荣负荷无功': Q17,
                           '吉庄负荷有功': P18, '吉庄负荷无功': Q18, '繁峙负荷有功': P19,
                           '繁峙负荷无功': Q19})
    result.to_excel('result\\result_2.xlsx')
