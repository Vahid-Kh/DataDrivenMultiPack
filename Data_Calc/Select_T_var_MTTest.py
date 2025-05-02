import pandas as pd  # Dataframe library
import numpy as np  # Scientific computing with nD object support
import matplotlib.pyplot as plt
from datetime import datetime
from TDN import TDN
from functions import mov_ave, plot_corr, plot_5,plot_2, print_weekly_ave, print_lengly_ave, is_nan
from sklearn.metrics import r2_score as r2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn import metrics
from statsmodels.tsa.vector_ar.var_model import VAR

""" LT  """
""" Load data as CSV """
W28_ACLP1_HP1_ALC1 = "Data_MT_Week_28"
W29_ACLP1_HP0_ALC1 = "Data_MT_Week_29"
W30_ACLP1_HP0_ALC0 = "Data_MT_Week_30"
W31_ACLP1_HP1_ALC0 = "Data_MT_Week_31"
W32_ACDX1_HP0_ALC1 = "Data_MT_Week_32"
W33_ACDX1_HP0_ALC0 = "Data_MT_Week_33"
W34_ACDX1_HP1_ALC0 = "Data_MT_Week_34"
W35_ACDX1_HP1_ALC1 = "Data_MT_Week_35"
"""Before Ejector installation"""
W2_ACDX1_HP0_ALC0 = "Data_MT_Week_21"
W3_ACDX1_HP0_ALC0 = "Data_MT_Week_22"
W4_ACDX1_HP0_ALC0 = "Data_MT_Week_23"
W5_ACDX1_HP0_ALC0 = "Data_MT_Week_24"
W6_ACDX1_HP0_ALC0 = "Data_MT_Week_25"
W7_ACDX1_HP0_ALC0 = "Data_MT_Week_26"
W8_ACDX1_HP0_ALC0 = "Data_MT_Week_27"


PDM = [

        W2_ACDX1_HP0_ALC0, W3_ACDX1_HP0_ALC0, W4_ACDX1_HP0_ALC0, W5_ACDX1_HP0_ALC0,
        W6_ACDX1_HP0_ALC0, W7_ACDX1_HP0_ALC0, W8_ACDX1_HP0_ALC0,
        W28_ACLP1_HP1_ALC1, W29_ACLP1_HP0_ALC1, W30_ACLP1_HP0_ALC0, W31_ACLP1_HP1_ALC0,
        W32_ACDX1_HP0_ALC1, W33_ACDX1_HP0_ALC0, W34_ACDX1_HP1_ALC0, W35_ACDX1_HP1_ALC1
    ]

step = 1

"""___________________________ LIST OF DROP ITEMS FOR TRAINING ____________________"""
r2g = 0.2
train = [ 25, 26, 27, 30]
test = [30, 33]

dl = [
    # 'meb',
    # 'P6 MT suction',
    'T14 MT suction',
    'P3 AHU evaporation',
    'P4 LT suction',

    'T3 GC Outlet',

    'P1 discharge',
    'Power Meter MT',



    'Power Meter LT',
    'p14p1',

    'T11 LT discharge',

    'P2 receiver',
    'M3 MT liquid',
    'T15 Aux_HP suction',
    'mvd',
    'mbt',

    'T16 Aux suction',

    'T7 Ejector inlet',
    'MT evaporation temp',
    'mac',

    'P5 Aux HP suction',
    'T9 MT section outlet',
    'T4 Inlet IHX 1',
    'T5 Inlet IHX 2',
    'pwr',
    'mmt',
    'stt',
    'mdot_old',
    'mdot_old_10',

    'T1 MT discharge',
    'T2 After AHU',
    'T6 Receiver',
    'T6 Receiver sat',
    'T8 Liquid out IHX',
    'T10 LT suction',
    'T12 Intercooler outlet',
    'T13 out intercooler and MT section',
    'T18 Outlet AHU (heating)',
    'T19 Outlet AHU (cooling)',
    'T20 Outlet AHU (cooling)',
    'T23 LT section outlet',
    'LT evaporation temp',

    'AHU saturation temp',
    'Tair external air',

    'P7 ejector inlet',

    'M2 AHU vapour (heating)',
    'M4 LT liquid',  # 0.391
    'Mtotal AHU',  # 0.244
    'Power Meter AUX',
    'Total Power',
    'h1 Enthalpy',
    'h2 Enthalpy',
    'h3 Enthalpy',
    'h4 Enthalpy',
    'h5 Enthalpy',
    'h6 Enthalpy sat',
    'h7 Enthalpy',
    'h9 Enthalpy',
    'h10 Enthalpy',
    'h11 Enthalpy',
    'h12 Enthalpy',
    'h13 Enthalpy',
    'h14 Enthalpy',
    'h15 Enthalpy',
    'h16 Enthalpy',
    'h17 Enthalpy',
    'h18 Enthalpy',
    'h19 Enthalpy',
    'h20 Enthalpy',
    'h23 Enthalpy',
    'h8 Enthalpy calc',
    'hmix Enthalpy',
    'T8 calculated',
    'Cooling duty LT evap',
    'Cooling duty rooftop AC'
]
"""Training weeks"""
dll = dl.copy()

for iii in train:
    for jjj in test:
        print(iii,jjj)
        week_tr, week_ts = iii, jjj
        """________________________________________________________________________________"""
        """Testing weeks"""
        """________________________________________________________________________________"""
        data_tr = pd.read_csv(PDM[week_tr-21], na_filter=True, skip_blank_lines=True, low_memory=False)

        cd = [[0]] * 30
        dd = [[0]] * 30
        for ii in range(len(cd)):
            cd[ii] = []
            dd[ii] = []

        data_tr.drop('time', axis=1, inplace=True)
        data_tr.drop('Unnamed: 0', axis=1, inplace=True)


        data_trr = data_tr.copy()

        # for iiiii in dl:
        # for iiiii in dl[:-24]:
        dl = dll.copy()
        for iiiii in dl[0:1]:
            if iiiii not in ['mmt' , 'mdot_old' , 'mdot_old_10', 'M3 MT liquid']:
                # print(iiiii)

                data_tr = data_trr.copy()
                y = data_tr['y'].tolist()
                data_tr.drop('y', axis=1, inplace=True)
                dl.remove(iiiii)
                """ DROP FROM LIST """
                data_tr.drop(dl, axis=1, inplace=True)
                # print(data_tr.columns)
                """___________________________________________________________________________________"""

                """  ______________Multivariate Linear Regression____________  """

                """Making train and validation set"""
                train_ratio = 0.9999
                X_train = data_tr[:int(train_ratio * (len(data_tr)))]
                X_test = data_tr[int(train_ratio * (len(data_tr))):]
                y_train = y[:int(train_ratio * (len(y)))]
                y_test = y[int(train_ratio * (len(y))):]

                """___________________________________________________________________________________"""

                """_________-  Multivariate Linear Regression -_______________ """

                """ Create the Linear Model (LinearRegression) """
                # regressor = LinearRegression()
                regressor = BayesianRidge()
                regressor.fit(X_train, y_train)

                """ Interpreting the Coefficient and the Intercept """
                y_pred = regressor.predict(X_test)

                """___________________________________________________________________________________"""
                # print(' # of columns used for train and test : ', len(data_tr.columns))
                # print(data_tr.columns)
                # print(PDM[week_ts[0]-21])
                data_ts = pd.read_csv(PDM[week_ts-21], na_filter=True, skip_blank_lines=True, low_memory=False)
                time = data_ts['time'].tolist()

                mvd = data_ts['mvd'].tolist()
                meb = data_ts['meb'].tolist()
                mbt = data_ts['mbt'].tolist()

                old = data_ts['mdot_old'].tolist()
                y = data_ts['y'].tolist()
                """___________________________________________________________________________________"""
                """ One by one drop """
                data_ts.drop(dl, axis=1, inplace=True)
                """___________________________________________________________________________________"""
                data_ts.drop('time', axis=1, inplace=True)
                data_ts.drop('Unnamed: 0', axis=1, inplace=True)
                data_ts.drop('y', axis=1, inplace=True)
                var5 = []
                ld = []

                for i in range((data_ts.shape[0])):

                    """     ------    NO OLD DATA USED FOR MEMORY OF TRAINING     ------    """
                    ld = list(data_ts.iloc[i][:])
                    var5.append(regressor.predict([ld])[0])

                """___________________________________________________________________________________"""
                """___________________________________________________________________________________"""
                label = ['not named']*10
                label[0] = 'Time [s]'
                label[1] = 'mlt_cal_volumetric'
                label[2] = 'mlt_cal_energy_bal'
                label[3] = 'mlt_bitzer_poly'
                label[4] = 'mlt_measurement'
                label[5] = 'mlt_data_driven'

                var1 = mvd.copy()
                var2 = meb.copy()
                var3 = mbt.copy()
                var4 = y.copy()

                if r2(var5, var4) > r2g:
                    print(  round(r2(var5, var4),4),' Var: ', iiiii, ' Tr ', week_tr, ' Ts ', week_ts)



