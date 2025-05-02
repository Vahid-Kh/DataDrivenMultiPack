# coding=utf8
import pandas as pd                 # Dataframe library
import numpy as np                  # Scientific computing with nD object support
from datetime import datetime
#from TDN import TDN, PSI
#from functions import mov_ave
#import seaborn as sns

"""________________________________________________________________________________"""


"""Before Ejector installation"""
W01_LP0_HP0_LE0 = "10_01_2019_to_17_01_2019_converted.csv"
W02_LP0_HP0_LE0 = "17_01_2019_to_24_01_2019_converted.csv"
W03_LP0_HP0_LE0 = "24_01_2019_to_31_01_2019_converted.csv"
W04_LP0_HP0_LE0 = "07_02_2019_to_14_02_2019_converted.csv"
W05_LP0_HP0_LE0 = "14_02_2019_to_21_02_2019_converted.csv"
W06_LP0_HP0_LE0 = "21_02_2019_to_28_02_2019_converted.csv"
W07_LP0_HP0_LE0 = "31_01_2019_to_07_02_2019_converted.csv"

"""After Ejector installation"""
W08_LP1_HP1_LE1 = "28_02_2019_to_07_03_2019_converted.csv"
W09_LP1_HP1_LE1 = "07_03_2019_to_14_03_2019_converted.csv"
W10_LP1_HP1_LE1 = "14_03_2019_to_21_03_2019_converted.csv"
W11_LP1_HP1_LE1 = "21_03_2019_to_28_03_2019_converted.csv"
W12_LP1_HP1_LE1 = "28_03_2019_to_04_04_2019_converted.csv"
W13_LP1_HP1_LE1 = "04_04_2019_to_11_04_2019_converted.csv"
W14_LP1_HP1_LE1 = "11_04_2019_to_18_04_2019_converted.csv"
W15_LP1_HP1_LE1 = "18_04_2019_to_25_04_2019_converted.csv"
W16_LP1_HP1_LE1 = "25_04_2019_to_02_05_2019_converted.csv"
W17_LP1_HP1_LE1 = "02_05_2019_to_09_05_2019_converted.csv"
W18_LP1_HP1_LE1 = "09_05_2019_to_16_05_2019_converted.csv"
W19_LP1_HP1_LE1 = "16_05_2019_to_23_05_2019_converted.csv"
W20_LP1_HP1_LE1 = "23_05_2019_to_30_05_2019_converted.csv"
W21_LP1_HP1_LE1 = "21_03_2019_to_28_03_2019_converted.csv"
W22_LP1_HP1_LE1 = "28_03_2019_to_04_04_2019_converted.csv"
W23_LP1_HP1_LE1 = "30_05_2019_to_06_06_2019_converted.csv"
W24_LP1_HP1_LE1 = "06_06_2019_to_13_06_2019_converted.csv"
W25_LP1_HP1_LE1 = "13_06_2019_to_20_06_2019_converted.csv"
W26_LP1_HP1_LE1 = "20_06_2019_to_27_06_2019_converted.csv"
W27_LP1_HP1_LE1 = "27_06_2019_to_04_07_2019_converted.csv"

"""Summer Weeks"""
W28_LP1_HP1_LE1 = "11_07_2019_to_18_07_2019_converted.csv"
W29_LP1_HP0_LE1 = "18_07_2019_to_25_07_2019_converted.csv"
W30_LP1_HP0_LE0 = "25_07_2019_to_01_08_2019_converted.csv"
W31_LP1_HP1_LE0 = "01_08_2019_to_08_08_2019_converted.csv"
W32_LP0_HP0_LE1 = "08_08_2019_to_15_08_2019_converted.csv"
W33_LP0_HP0_LE0 = "15_08_2019_to_22_08_2019_converted.csv"
W34_LP0_HP1_LE0 = "22_08_2019_to_29_08_2019_converted.csv"
W35_LP0_HP1_LE1 = "29_08_2019_to_05_09_2019_converted.csv"

"""Name of file to LIST """
PDM_C = [

        W01_LP0_HP0_LE0,
        W02_LP0_HP0_LE0,
        W03_LP0_HP0_LE0,
        W04_LP0_HP0_LE0,
        W05_LP0_HP0_LE0,
        W06_LP0_HP0_LE0,
        W07_LP0_HP0_LE0,

        W08_LP1_HP1_LE1,
        W09_LP1_HP1_LE1,
        W10_LP1_HP1_LE1,
        W11_LP1_HP1_LE1,
        W12_LP1_HP1_LE1,
        W13_LP1_HP1_LE1,
        W14_LP1_HP1_LE1,
        W15_LP1_HP1_LE1,
        W16_LP1_HP1_LE1,
        W17_LP1_HP1_LE1,
        W18_LP1_HP1_LE1,
        W19_LP1_HP1_LE1,
        W20_LP1_HP1_LE1,
        W21_LP1_HP1_LE1,
        W22_LP1_HP1_LE1,
        W23_LP1_HP1_LE1,
        W24_LP1_HP1_LE1,
        W25_LP1_HP1_LE1,
        W26_LP1_HP1_LE1,
        W27_LP1_HP1_LE1,

        W28_LP1_HP1_LE1,
        W29_LP1_HP0_LE1,
        W30_LP1_HP0_LE0,
        W31_LP1_HP1_LE0,
        W32_LP0_HP0_LE1,
        W33_LP0_HP0_LE0,
        W34_LP0_HP1_LE0,
        W35_LP0_HP1_LE1,

]

PDM_C_l_n = [

        'W01_LP0_HP0_LE0',
        'W02_LP0_HP0_LE0',
        'W03_LP0_HP0_LE0',
        'W04_LP0_HP0_LE0',
        'W05_LP0_HP0_LE0',
        'W06_LP0_HP0_LE0',
        'W07_LP0_HP0_LE0',

        'W08_LP1_HP1_LE1',
        'W09_LP1_HP1_LE1',
        'W10_LP1_HP1_LE1',
        'W11_LP1_HP1_LE1',
        'W12_LP1_HP1_LE1',
        'W13_LP1_HP1_LE1',
        'W14_LP1_HP1_LE1',
        'W15_LP1_HP1_LE1',
        'W16_LP1_HP1_LE1',
        'W17_LP1_HP1_LE1',
        'W18_LP1_HP1_LE1',
        'W19_LP1_HP1_LE1',
        'W20_LP1_HP1_LE1',
        'W21_LP1_HP1_LE1',
        'W22_LP1_HP1_LE1',
        'W23_LP1_HP1_LE1',
        'W24_LP1_HP1_LE1',
        'W25_LP1_HP1_LE1',
        'W26_LP1_HP1_LE1',
        'W27_LP1_HP1_LE1',

        'W28_LP1_HP1_LE1',
        'W29_LP1_HP0_LE1',
        'W30_LP1_HP0_LE0',
        'W31_LP1_HP1_LE0',
        'W32_LP0_HP0_LE1',
        'W33_LP0_HP0_LE0',
        'W34_LP0_HP1_LE0',
        'W35_LP0_HP1_LE1',

]


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

"""Label list set up"""
label = [0]*8
label[0] = 'Time [s]'
"""----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """
"""Steps for reading data, takes one data out of #Step """

step_c = 1
length = 500
n = 180    # Moving averaging sample size


for week in range(len(PDM_C)):

    """----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """

    print(week+1)
    print(str(PDM_C[week]))

    def logic(index):

        if index % step_c == 0:
            return False
        return True

    weekdata = 'Data/' + PDM_C[week]
    print(weekdata)
    """ DataFrame read from CSV file, na_filter=False, skip_blank_lines=False """
    dfc = pd.read_csv(weekdata, sep=';', skiprows=lambda x: logic(x), na_filter=True, skip_blank_lines=True, low_memory=False)
    print(dfc.shape)
    dfc.drop(dfc.columns[0], axis=1, inplace=True)
    dfc.drop('Calculated values ==>', axis=1, inplace=True)

    """Change date format from 2019 - 08 - 01 17: 05:45.119  "%Y-%m-%d %H:%M:%S.%f "  to Seconds"""
    # t0 = datetime.strptime(df.loc[0][0], "%Y-%m-%d %H:%M:%S.%f")  # Time refrence for date conversion
    t0 = datetime.strptime(" 17:00:00  11/07/2019", " %H:%M:%S %d/%m/%Y")  # Time refrence for date conversion
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

    for j in range(10):
        for i in range(1, len(dfc.columns) - 1):
            if i >= len(dfc.columns):
                break
            if dfc.isnull().iloc[6][i]:
                dfc.drop(dfc.columns[i], axis=1, inplace=True)
    print(dfc.shape)


    """________________________________________________________________________________"""


    dfc.to_csv("Data_cleaned/"+ str(PDM_C_l_n[week]))





