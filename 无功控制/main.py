# Import modules
import sys
import pandas as pd

# Import PySwarms
import pyswarms as ps


def cost_function(x):  # 损失函数，输入x是一个数组
    ldf = app.GetFromStudyCase("ComLdf")  # 获取研究案例里的潮流计算赋予ldf
    comSh = app.GetFromStudyCase("ComSh")  # 结果输出
    outputWindow = app.GetOutputWindow()  # 结果窗口

    def get_Ul():
        ldf.Execute()  # 执行潮流计算
        outputWindow.Clear()  # 清空输出窗口
        comSh.iopt_cmd = 3  # complete system report
        comSh.iopt_vpr = 1  # voltage profiles
        comSh.Execute()  # 结果输出
        outputWindow.Save('ldf.txt')  # 保存结果窗口
        df = pd.read_fwf('ldf.txt')  # pandas读取txt文件
        str = df.iloc[336, 0]  # 定位到第338行|minghai21, 第1列
        s = str.split()  # 切分字符串
        Ul = float(s[4])  # 字符串列表第5个元素为Ul，转化为浮点数
        return Ul

    def action(rate):  # 调整风电同时率
        for para in DFIG_02:
            para.ngnum = int(100 * rate)
        for para in PMSG_02:
            para.ngnum = int(100 * rate)
        for para in PMSG_03:
            para.ngnum = int(100 * rate)
        for para in PMSG_06:
            para.ngnum = int(100 * rate)
        # for para in DFIG_02:  # 风电同时率为0%
        #     para.outserv = 1
        # for para in PMSG_02:
        #     para.outserv = 1
        # for para in PMSG_03:
        #     para.outserv = 1
        # for para in PMSG_06:
        #     para.outserv = 1

    def reset():   # 复位函数
        for para in DFIG_02:
            para.ngnum = 100  # 山台站发电机额定功率为3*100=300MW
        for para in PMSG_02:
            para.ngnum = 100  # 卧龙站发电机有功最大值为3*100=300MW
        for para in PMSG_03:
            para.ngnum = 100  # 蒋家站发电机有功最大值为3.5*100=350MW
        for para in PMSG_06:
            para.ngnum = 100  # 台子山站发电机有功最大值为1*100=100MW
        # for para in DFIG_02:  # 风电同时率为0%
        #     para.outserv = 0
        # for para in PMSG_02:
        #     para.outserv = 0
        # for para in PMSG_03:
        #     para.outserv = 0
        # for para in PMSG_06:
        #     para.outserv = 0
        for para in wolong9SVG_4:        # 初始状态，并补全部投入运行
            para.ncapa = 4
        for para in wolong11FC_1:
            para.ncapa = 1
        for para in wolong12FC_2:
            para.ncapa = 2
        for para in wolong14SVG_1:
            para.ncapa = 1
        for para in jaingjia10FC_4:
            para.ncapa = 4
        for para in jaingjia12SVG_4:
            para.ncapa = 4
        for para in jaingjia13SVG_1:
            para.ncapa = 1
        for para in taizishan25SVG_1:
            para.ncapa = 1

    DFIG_02 = app.GetCalcRelevantObjects("DFIG 02.ElmAsm")      # 山台站DFIG 02
    PMSG_02 = app.GetCalcRelevantObjects("PMSG 02.ElmGenstat")  # 卧龙站PMSG 02
    PMSG_03 = app.GetCalcRelevantObjects("PMSG 03.ElmGenstat")  # 蒋家站PMSG 03
    PMSG_06 = app.GetCalcRelevantObjects("PMSG 06.ElmGenstat")  # 台子山站PMSG 06

    wolong9SVG_4 = app.GetCalcRelevantObjects("wolong_9SVG#4.ElmShnt")          # 卧龙站4*9MVar额定容量等值电容器
    wolong11FC_1 = app.GetCalcRelevantObjects("wolong_11FC#1.ElmShnt")          # 卧龙站1*11MVar额定容量等值电容器
    wolong12FC_2 = app.GetCalcRelevantObjects("wolong_12FC#2.ElmShnt")          # 卧龙站2*12MVar额定容量等值电容器
    wolong14SVG_1 = app.GetCalcRelevantObjects("wolong_14SVG#1.ElmShnt")        # 卧龙站1*14MVar额定容量等值电容器
    jaingjia10FC_4 = app.GetCalcRelevantObjects("jiangjia_10FC#4.ElmShnt")      # 蒋家站4*10MVar额定容量等值电容器
    jaingjia12SVG_4 = app.GetCalcRelevantObjects("jiangjia_12.5SVG#4.ElmShnt")  # 蒋家站4*12.5MVar额定容量等值电容器
    jaingjia13SVG_1 = app.GetCalcRelevantObjects("jiangjia_13SVG#1.ElmShnt")    # 蒋家站1*13MVar额定容量等值电容器
    taizishan25SVG_1 = app.GetCalcRelevantObjects("taizishan_25SVG#1.ElmShnt")  # 台子山站1*25MVar额定容量等值电容器

    U = []
    for i in range(n_particles):  # 每个粒子循环一次
        reset()
        U_1 = get_Ul()
        action(0.5)  # 调整风电同时率,0.5表示50%
        '''并补投切'''
        for para in wolong9SVG_4:
            para.ncapa = int(x[:, 0][i])
        for para in wolong11FC_1:
            para.ncapa = int(x[:, 1][i])
        for para in wolong12FC_2:
            para.ncapa = int(x[:, 2][i])
        for para in wolong14SVG_1:
            para.ncapa = int(x[:, 3][i])
        for para in jaingjia10FC_4:
            para.ncapa = int(x[:, 4][i])
        for para in jaingjia12SVG_4:
            para.ncapa = int(x[:, 5][i])
        for para in jaingjia13SVG_1:
            para.ncapa = int(x[:, 6][i])
        for para in taizishan25SVG_1:
            para.ncapa = int(x[:, 7][i])
        U_2 = get_Ul()
        delta_U = abs(U_1 - U_2)  # 母线线电压变化量
        U.append(delta_U)
        reset()  # 复位

    return U


def pso():
    # Set-up hyperparameters
    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}

    # Create bounds
    max_bound = [5, 2, 3, 2, 5, 5, 2, 2]
    min_bound = [0, 0, 0, 0, 0, 0, 0, 0]
    bounds = (min_bound, max_bound)

    # Call instance of PSO
    global n_particles  # 全局变量
    n_particles = 15
    optimizer = ps.single.GlobalBestPSO(n_particles=n_particles, dimensions=8, options=options, bounds=bounds)

    # Perform optimization
    cost, pos = optimizer.optimize(cost_function, iters=10)
    return cost, pos


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

    pso()
