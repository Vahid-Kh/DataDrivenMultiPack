# coding=utf8
import pandas as pd                 # Dataframe library
import numpy as np                  # Scientific computing with nD object support
import matplotlib.pyplot as plt
from datetime import datetime
from TDN import TDN, PSI
from functions import mov_ave, plot_corr, plot_4, print_weekly_ave, print_lengly_ave, is_nan, plot_2
from sklearn.metrics import r2_score as r2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

from statsmodels.tsa.vector_ar.var_model import VAR

"""________________________________________________________________________________"""

""" Load data as CSV """

"""------DANFOSS DATA-----"""
W28_ACLP1_HP1_ALC1 = "CNT-Porto Mós CNT-Porto Mós 07181621.csv"
W29_ACLP1_HP0_ALC1 = "CNT-Porto Mós CNT-Porto Mós 07251740.csv"
W30_ACLP1_HP0_ALC0 = "CNT-Porto Mós CNT-Porto Mós 08011828.csv"
W31_ACLP1_HP1_ALC0 = "CNT-Porto Mós CNT-Porto Mós 08081807.csv"
W32_ACDX1_HP0_ALC1 = "CNT-Porto Mós CNT-Porto Mós 08141822.csv"
W33_ACDX1_HP0_ALC0 = "CNT-Porto Mós CNT-Porto Mós 08221642.csv"
W34_ACDX1_HP1_ALC0 = "CNT-Porto Mós CNT-Porto Mós 08291846.csv"
W35_ACDX1_HP1_ALC1 = "CNT-Porto Mós CNT-Porto Mós 10161239.csv"

PDM_D = [W28_ACLP1_HP1_ALC1, W29_ACLP1_HP0_ALC1, W30_ACLP1_HP0_ALC0, W31_ACLP1_HP1_ALC0,
         W32_ACDX1_HP0_ALC1, W33_ACDX1_HP0_ALC0, W34_ACDX1_HP1_ALC0, W35_ACDX1_HP1_ALC1]

"""------CNR DATA-----"""
W28_ACLP1_HP1_ALC1 = "Data_Mdot/Data_28"
W29_ACLP1_HP0_ALC1 = "Data_Mdot/Data_29"
W30_ACLP1_HP0_ALC0 = "Data_Mdot/Data_30"
W31_ACLP1_HP1_ALC0 = "Data_Mdot/Data_31"
W32_ACDX1_HP0_ALC1 = "Data_Mdot/Data_32"
W33_ACDX1_HP0_ALC0 = "Data_Mdot/Data_33"
W34_ACDX1_HP1_ALC0 = "Data_Mdot/Data_34"
W35_ACDX1_HP1_ALC1 = "Data_Mdot/Data_35"

PDM_C = [W28_ACLP1_HP1_ALC1, W29_ACLP1_HP0_ALC1, W30_ACLP1_HP0_ALC0, W31_ACLP1_HP1_ALC0,
         W32_ACDX1_HP0_ALC1, W33_ACDX1_HP0_ALC0, W34_ACDX1_HP1_ALC0, W35_ACDX1_HP1_ALC1]

"""Label list set up"""
label = [0]*8
label[0] = 'Time [s]'
"""----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """
"""Steps for reading data, takes one data out of #Step """
step = 1
step_c = step*2
length = 500
week = 30
n = 180    # Moving averaging sample size
"""----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """
""" Time differences for week 28 to 35 
 time_C = [x + (time_D[0]-time_C[0])-td[week-28] for x in time_C]  """

td = [-11300, -164013, -15860, -18160, -15960, -8866, -12061, -12226]


idk = [0, 0, -100, -100, -100, -100, -100, -100]

print(td)

# for week in[28, 29, 30, 31, 32, 33, 34, 35]:
for week in [34]:
    """----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """

    """--------------------------------"""
    """------------Danfoss-------------"""
    """--------------------------------"""


    def logic(index):

        if index % step == 0 and index >= 5:
            return False
        elif index % 5 - 1 == 0 and index < 5:
            return False
        return True


    weekdata = 'Data/' + PDM_D[week - 28]

    """ DataFrame read from CSV file, na_filter=False, skip_blank_lines=False """
    dfd = pd.read_csv(weekdata, skiprows=lambda x: logic(x), na_filter=True, skip_blank_lines=True, low_memory=False)
    """ PRINT DATA HEADER"""
    # for i in range(len(dfd.columns)):
    #     print(i, '   ', dfd.columns[i], '         ', dfd.loc[1][i])
    # df = pd.read_csv(weekdata, nrows=100, skiprows=[0, 2, 3, 4, 5]) # takes 100 rows only
    """Change date format from  " %H:%M:%S %d/%m/%Y"  to Seconds"""
    t0 = datetime.strptime(" 17:00:00  11/07/2019", " %H:%M:%S %d/%m/%Y")  # Time refrence for date conversion
    # t0 = datetime.strptime(df.loc[0][0], " %H:%M:%S %d/%m/%Y")  # Time refrence for date conversion
    tb = (t0-datetime.strptime(" 01:00:00  01/01/1970", " %H:%M:%S %d/%m/%Y")).total_seconds()
    for i in range(dfd.shape[0]):
        DT = datetime.strptime(dfd.loc[i][0], " %H:%M:%S %d/%m/%Y")
        dfd.at[i, 'Name'] = (DT - t0).total_seconds()

    """ Makes all to numeric so str changes to NaN and droped by dropna"""
    dfd = dfd.apply(pd.to_numeric, errors='coerce')
    # """DROP NAN acting only on the COLUMNS with nan values"""
    dfd = dfd.dropna(axis='columns', how='all', thresh=1000 / step, subset=None, inplace=False)
    """DROP NAN acting only on the ROWS with nan values"""
    dfd = dfd.dropna(axis='rows', how='any', thresh=None, subset=None, inplace=False)
    """Round time measurements to seconds only"""
    dfd = dfd.round({'Name': 0})
    time_D = dfd['Name'].tolist()

    """ %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
    """ WARNING : THIS DROPS ALL ZEROS """
    dfd = dfd.loc[(dfd != 0).any(axis=1)]
    dfd = dfd.loc[~(dfd == 0).all(axis=1)]
    dfd = dfd.loc[(dfd != 0).any(1)]

    """________________________________________________________________________________"""
    """________________________________________________________________________________"""

    # """Read only certain number of data"""
    # num = 910
    # df = pd.read_csv("CNT-Porto Mós CNT-Porto Mós 09111019.csv", skiprows=lambda x: logic(x), nrows=num,
    #                  na_filter=False, skip_blank_lines=False)
    """________________________________________________________________________________"""

    """To get 2 digits after decimal only, error in measurement of temperature(rounded to ~0.02%) and 
    pressure(rounded to ~0.01%) is for sure more than 1% """
    dfd = dfd.round(2)
    dfd = dfd.astype(float).round(2)

    for j in range(10):
        for i in range(1, len(dfd.columns) - 1):
            if i >= len(dfd.columns):
                break
            if dfd.isnull().iloc[6][i]:
                dfd.drop(dfd.columns[i], axis=1, inplace=True)

    """----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """

    """--------------------------------"""
    """--------------CNR---------------"""
    """--------------------------------"""

    """ Skip rows every (step)th line  """


    def logic(index):

        if index % step_c == 0:
            return False
        return True


    weekdata = PDM_C[week - 28]
    """ DataFrame read from CSV file, na_filter=False, skip_blank_lines=False """
    dfc = pd.read_csv(weekdata, sep=',', skiprows=lambda x: logic(x), na_filter=True, skip_blank_lines=True, low_memory=False)


    time_C = dfc['time'].tolist()

    """----------------- %%%%%%%%%%%-- DegC to Kelvin --%%%%%%%%%%%%%------------- """


    """________________________________________________________________________________"""
    """________________________________________________________________________________"""

    for j in range(10):
        for i in range(1, len(dfc.columns) - 1):
            if i >= len(dfc.columns):
                break
            if dfc.isnull().iloc[6][i]:
                dfc.drop(dfc.columns[i], axis=1, inplace=True)

    """___________________________________________________________________________"""

    """----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """
    """----------------- %%%%%%%%%%%--- CALCULATIONS ---%%%%%%%%%------------- """
    """----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """

    """Test for enthalpy calculation"""    # DON'T REMOVE
    # lpl = dfc['P4 LT suction'].tolist()
    # ltl = dfc['T10 LT suction'].tolist()
    # lhl = dfc['h10 Enthalpy'].tolist()
    # lh10 = []
    # for i in range(dfc.shape[0]):
    #     lh10.append(TDN(lpl[i], 0, ltl[i], 0, 0, 'CO2').h)

    time_lag = round(td[week-28]/120)
    print(time_lag)

    """________________Ensure same legth of data from two datasets________________"""

    if time_lag > 0:
        for i in range(abs(time_lag)):
            dfc.drop(dfc.head(1).index, inplace=True)  # drop first n rows
            del time_C[0]

    if time_lag < 0:
        for i in range(abs(time_lag)):
            dfd.drop(dfd.head(1).index, inplace=True)   # drop first n rows

    if dfc.shape[0] < dfd.shape[0]:
        for i in range(dfc.shape[0], dfd.shape[0]):
            dfd.drop(dfd.tail(1).index, inplace=True)   # drop last n rows

    elif dfc.shape[0] > dfd.shape[0]:
        for i in range(dfd.shape[0], dfc.shape[0]):
            dfc.drop(dfc.tail(1).index, inplace=True)   # drop last n rows
            del time_C[-1]

    """________________________________________________________________________________"""


    """ CNR , DANFOSS     CNR sensor tag  ,  DANFOSS sensor tag  """
    # label[1], label[2] = 'T1 MT discharge', 'AK-PC 782A:   Sd-MT'
    # label[1], label[2] = 'T2 After AHU', 'AK-PC 782A:   Stw2'
    label[1], label[2] = 'T3 GC Outlet', 'AK-PC 782A:   Sgc ctrl.'
    # label[1], label[2] = 'T6 Receiver sat', 'AK-PC 782A:   Trec'
    # label[1], label[2] = 'T10 LT suction', 'AK-PC 782A:   Ss-LT'
    # label[1], label[2] = 'T11 LT discharge', 'AK-PC 782A:   Sd-LT'
    # label[1], label[2] = 'T16 Aux suction', 'AK-PC 782A:   Ss-IT'
    # label[1], label[2] = 'T21 Water in DHW', 'AK-PC 782A:   Stw3'
    # label[1], label[2] = 'T22 Water out DHW', 'AK-PC 782A:   Stw4'
    #
    # label[1], label[2] = 'LT evaporation temp', 'AK-PC 782A:   Suction temp. To-LT'
    # label[1], label[2] = 'MT evaporation temp', 'AK-PC 782A:   Suction temp. To-MT'
    # label[1], label[2] = 'Tair external air', 'AK-PC 782A:   Cond. temp.'
    # label[1], label[2] = 'Tair external air', 'AK-PC 782A:   Sc3'
    #
    # label[1], label[2] = 'P1 discharge', 'AK-PC 782A:   Pgc'
    # label[1], label[2] = 'P2 receiver', 'AK-PC 781A:   Po Pressure' #  Not exactly the same
    # label[1], label[2] = 'P4 LT suction', 'AK-PC 782A:   Po-LT'
    # label[1], label[2] = 'P6 MT suction', 'AK-PC 782A:   Po-MT'

    # label[1], label[2] = 'T6 Receiver sat', 'AK-PC 782A:   Vapor ejector capaci'
    # label[1], label[2] = 'T6 Receiver sat', 'AK-PC 782A:   Ejector OD'
    # label[1], label[2] = 'T6 Receiver sat', 'AK-PC 782A:   Suction accumulator'
    # label[1], label[2] = '', ''

    # label[1], label[2] = 'T1 MT discharge', 'AK-PC 782A:   Running capacity MT'
    # label[1], label[2] = 'Power Meter MT', 'AK-PC 782A:   Running capacity MT'
    # label[1], label[2] = 'DHW water', 'AK-PC 782A:   Running capacity IT'
    # label[1], label[2] = 'M4 LT liquid', 'AK-PC 782A:   Tw enable'
    # label[1], label[2] = 'M1 AHU liquid (cooling)', 'AK-PC 782A:   Running capacity IT'
    # label[1], label[2] = 'stato_mt1', 'AK-PC 782A:   Running capacity MT'
    # label[1], label[2] = 'M1 AHU liquid (cooling)', 'AK-PC 782A:   Running capacity IT'
    # label[1], label[2] = 'P6 MT suction', 'AK-PC 782A:   Tc-LT'

    time_lag =idk[week-28]
    if time_lag > 0:
        for i in range(abs(time_lag)):
            dfc.drop(dfc.head(1).index, inplace=True)  # drop first n rows
            del time_C[0]

    if time_lag < 0:
        for i in range(abs(time_lag)):
            dfd.drop(dfd.head(1).index, inplace=True)   # drop first n rows

    if dfc.shape[0] < dfd.shape[0]:
        for i in range(dfc.shape[0], dfd.shape[0]):
            dfd.drop(dfd.tail(1).index, inplace=True)   # drop last n rows

    elif dfc.shape[0] > dfd.shape[0]:
        for i in range(dfd.shape[0], dfc.shape[0]):
            dfc.drop(dfc.tail(1).index, inplace=True)   # drop last n rows
            del time_C[-1]
    var1 = dfc[label[1]].tolist()   # Color "c-"

    var2 = dfd[label[2]].tolist()  # Color "r-"
    plot_2(time_C,var1,var2,label,week)
    """________________________________________________________________________________"""
    label[2] = "AK-PC 782A:   Vhp OD"
    label[3] = "AK-PC 782A:   Vrec OD"
    label[4] = "AK-PC 782A:   Vapor ejector capaci"
    label[5] = "AK-PC 782A:   V3gc valve"
    """________________________________________________________________________________"""

    """________________________________________________________________________________"""

    var1 = dfc[label[1]].tolist()   # Color "c-"
    var2 = dfd[label[2]].tolist()  # Color "r-"
    var3 = dfd[label[3]].tolist()  # Color "r-"
    var4 = dfd[label[4]].tolist()  # Color "r-"
    var5 = dfd[label[5]].tolist()  # Color "r-"

    time = time_C[n:]
    var1 = var1[n:]
    var2 = mov_ave(var2, n)[n:]
    var3 = mov_ave(var3, n)[n:]
    var4 = mov_ave(var4, n)[n:]
    var5 = mov_ave(var5, n)[n:]

    print(r2(var1, var2))

    # """Polynomial regression of 3rd order for Bitzer estimation to measured data"""
    # ds = 720  # One day data
    # cp1 = np.polyfit(var1[n:n + ds], var4[n:n + ds], 1)  # VD
    # print('Calc vs exact Sqr is : ', r2(var1, var4))
    # var1 = [cp1[0] * x + cp1[1] for x in var1]
    # print('Regression R vs exact R Sqr is : ', r2(var1, var4))

    plot_2(time, var3, var2, label, week)

    print(dfc.shape[0], len(var2))
    HPV_OD = var2
    VR_OD = var3
    V3gc = var5
    od = np.array(HPV_OD)/100

    """ Mass flow for CCMT 16 """
    k = 75.84*(od*0.05935 + 0.94150*od**2 - 0.00120*od**3)
    p_i = mov_ave(dfc['P7 ejector inlet'].tolist(), n)[n:]
    p_o = mov_ave(dfc['P2 receiver'].tolist(), n)[n:]
    t_5 = mov_ave(dfc['T5 Inlet IHX 2'].tolist(), n)[n:]

    rho_i = []
    for i in range(len(p_i)):
        # rho_i.append(TDN(p_i[i], h_8[i], 0, 0, 0, 'CO2').d)
        rho_i.append(PSI('D', 'P', p_i[i], 'T', t_5[i], 'CO2'))

    var6 = list((k * 2 / 3 * np.sqrt(((np.array(p_i) - np.array(p_o)) / 1e5 * np.array(rho_i))))  / 3600)

    print(dfc.head)

    dfc.drop(dfc.head(n).index, inplace=True)  # drop last n rows



    dfc = dfc.assign(HPV_OD = HPV_OD)
    dfc = dfc.assign(VR_OD = var3)
    dfc = dfc.assign(V3gc = var5)
    dfc = dfc.assign(mhv=var6)
    print(dfc.head)

    dfc.to_csv("PDM_W_" + str(week))

plt.show()

