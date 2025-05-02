# coding=utf8
import pandas as pd                 # Dataframe library
import numpy as np                  # Scientific computing with nD object support
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from TDN import TDN
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
W28_ACLP1_HP1_ALC1 = "11_07_2019_to_18_07_2019_converted.csv"
W29_ACLP1_HP0_ALC1 = "18_07_2019_to_25_07_2019_converted.csv"
W30_ACLP1_HP0_ALC0 = "25_07_2019_to_01_08_2019_converted.csv"
W31_ACLP1_HP1_ALC0 = "01_08_2019_to_08_08_2019_converted.csv"
W32_ACDX1_HP0_ALC1 = "08_08_2019_to_15_08_2019_converted.csv"
W33_ACDX1_HP0_ALC0 = "15_08_2019_to_22_08_2019_converted.csv"
W34_ACDX1_HP1_ALC0 = "22_08_2019_to_29_08_2019_converted.csv"
W35_ACDX1_HP1_ALC1 = "29_08_2019_to_05_09_2019_converted.csv"

PDM_C = [W28_ACLP1_HP1_ALC1, W29_ACLP1_HP0_ALC1, W30_ACLP1_HP0_ALC0, W31_ACLP1_HP1_ALC0,
         W32_ACDX1_HP0_ALC1, W33_ACDX1_HP0_ALC0, W34_ACDX1_HP1_ALC0, W35_ACDX1_HP1_ALC1]
pdm = [

    'W28_CD_LP1_HP1_LE1',
    'W29_CD_LP1_HP0_LE1',
    'W30_CD_LP1_HP0_LE0',
    'W31_CD_LP1_HP1_LE0',
    'W32_CD_LP0_HP0_LE1',
    'W33_CD_LP0_HP0_LE0',
    'W34_CD_LP0_HP1_LE0',
    'W35_CD_LP0_HP1_LE1',

]
"""Label list set up"""
label = [0]*8
label[0] = 'Time [s]'
"""----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """
"""Steps for reading data, takes one data out of #Step """
step = 1
step_c = step*2
length = 500
weeknum = [28, 29, 30, 31, 32, 33, 34, 35]
weeknum = [32,33]
n = 1    # Moving averaging sample size
"""----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """
""" Time differences for week 28 to 35 
 time_C = [x + (time_D[0]-time_C[0])-td[week-28] for x in time_C]  """

td = [2700,
      -152400,
      -11000,
      -13300,
      -11100,
      -7700,
      -10900,
      -11100,
      ]
# td = [0]*8

"""----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """
for week in weeknum:
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


    weekdata = 'Data/' + PDM_C[week - 28]
    """ DataFrame read from CSV file, na_filter=False, skip_blank_lines=False """
    dfc = pd.read_csv(weekdata, sep=';', skiprows=lambda x: logic(x), na_filter=True, skip_blank_lines=True, low_memory=False)

    """ PRINT DATA HEADER"""
    # for i in range(len(dfc.columns)):
    #     try:
    #         print(i, '   ', dfc.columns[i], '     ', round(dfc.loc[1][i], 3))
    #     except:
    #         print(i, '   ', dfc.columns[i])
    # df = pd.read_csv(weekdata, sep=';')  # takes all rows
    dfh = pd.read_csv(weekdata, nrows=1, sep=';')
    dfc.drop(dfc.columns[0], axis=1, inplace=True)
    dfc.drop('Calculated values ==>', axis=1, inplace=True)

    """Change date format from 2019 - 08 - 01 17: 05:45.119  "%Y-%m-%d %H:%M:%S.%f "  to Seconds"""
    # t0 = datetime.strptime(df.loc[0][0], "%Y-%m-%d %H:%M:%S.%f")  # Time refrence for date conversion

    for i in range(dfc.shape[0]):
        DT = datetime.strptime(dfc.loc[i][0], "%Y-%m-%d %H:%M:%S.%f")
        dfc.at[i, 'time'] = (DT - t0).total_seconds()

    dfc = dfc.apply(pd.to_numeric, errors='coerce')
    """DROP NAN acting only on the COLUMNS with more than 1000 nan values"""
    dfc = dfc.dropna(axis='columns', how='all', thresh=1000 / step_c, subset=None, inplace=False)
    """DROP NAN acting only on the ROWS with any nan values"""
    dfc = dfc.dropna(axis='rows', how='any', thresh=None, subset=None, inplace=False)
    dfc = dfc.round({"time": 0})

    time_C = dfc['time'].tolist()

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

    """----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """
    """DATA SENSOR TAG TO PLOT"""
    """ CNR , DANFOSS     CNR sensor tag  ,  DANFOSS sensor tag  """
    # label[1], label[2] = 'T1 MT discharge', 'AK-PC 782A:   Sd-MT'
    # label[1], label[2] = 'T2 After AHU', 'AK-PC 782A:   Stw2'
    # label[1], label[2] = 'T3 GC Outlet', 'AK-PC 782A:   Sgc ctrl.'
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
    label[1], label[2] = 'P6 MT suction', 'AK-PC 782A:   Po-MT'

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

    """Energy balance"""
    time = time_C
    var1 = dfc[label[1]].tolist()
    var2 = dfd[label[2]].tolist()

    """----------------- %%%%%%%%%%%-- DegC to Kelvin --%%%%%%%%%%%%%------------- """
    if 150 > var2[0] > -50 and var1[0] < 10e5:
        var2 = [x + 273.15 for x in var2]
    elif var1[0] > 5e5:
        var1 = [x/1e5 for x in var1]

    plot_2(time, var1, var2, ["Time [s]", label[1], label[2]], week)

    dfc.reset_index(inplace=True)
    dfd.reset_index(inplace=True)
    #
    # plot_2(time, var1, var2, ["Time [s]", label[1], label[2]], week)
    print(dfc.index, dfd.index)
    dfc = pd.concat([dfc, dfd.reindex(dfc.index)], axis=1)
    print(dfc.shape)
    dfc.to_csv(str(pdm[week-28]))
    # dfd.to_csv("Data_cleaned/" + str(pdm[week-28]))

plt.show()
