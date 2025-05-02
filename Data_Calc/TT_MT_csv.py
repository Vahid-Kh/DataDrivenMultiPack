import pandas as pd  # Dataframe library
import numpy as np  # Scientific computing with nD object support
import matplotlib.pyplot as plt
from datetime import datetime
from TDN import TDN
from functions import mov_ave, plot_corr, plot_5,plot_2, print_weekly_ave, print_lengly_ave, is_nan
from sklearn.metrics import r2_score as r2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
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
"""Training weeks"""
week_tr = [21, 22, 23, 24, 25, 26, 27, 30, 33]
# week_tr = [30]

"""________________________________________________________________________________"""
"""________________________________________________________________________________"""

# week = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
week = [21, 22, 23, 24, 25, 26, 27, 30, 32, 33]


step = 1
n = 180
"""________________________________________________________________________________"""
"""___________________________ LIST OF DROP ITEMS FOR TRAINING ____________________"""



dl = [
    # 'meb',
    # 'P6 MT suction',
    'P3 AHU evaporation',
    # 'T14 MT suction',

    'p14p1',
    'T11 LT discharge',
    'Power Meter LT',
    'Power Meter MT',
    'P2 receiver',
    'M3 MT liquid',
    'T15 Aux_HP suction',
    'mvd',
    'mbt',
    'T3 GC Outlet',

    'T16 Aux suction',

    'T7 Ejector inlet',

    'MT evaporation temp',

    'mac',


    'P1 discharge',

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



    'P4 LT suction',


    'P7 ejector inlet',
    'M2 AHU vapour (heating)',

    'M4 LT liquid',                        #  0.391
    'Mtotal AHU',                          #  0.244

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



"""________________________________________________________________________________"""

"""Testing weeks"""
week_ts = list(set(week) - set(week_tr))
week_ts.append(30)
week_ts.append(33)
week_ts.sort()

"""________________________________________________________________________________"""
data_tr = pd.read_csv(PDM[week_tr[0]-21], na_filter=True, skip_blank_lines=True, low_memory=False)
for i in week_tr[1:]:
    df = pd.read_csv(PDM[i-21], na_filter=True, skip_blank_lines=True, low_memory=False)
    data_tr = data_tr.append(df)

cd = [[0]] * 30
dd = [[0]] * 30
for ii in range(len(cd)):
    cd[ii] = []
    dd[ii] = []

data_tr.drop('time', axis=1, inplace=True)
data_tr.drop('Unnamed: 0', axis=1, inplace=True)


y = data_tr['y'].tolist()

"""  ______________ %%%%%%%%%%%%%%%%%%% ____________  """
"""___________________________________________________________________________________"""
""" DROP FROM LIST """
data_tr.drop(dl, axis=1, inplace=True)
"""___________________________________________________________________________________"""

data_tr.drop('y', axis=1, inplace=True)

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
regressor = LinearRegression()
regressor.fit(X_train, y_train)

""" Interpreting the Coefficient and the Intercept """
y_pred = regressor.predict(X_test)

"""___________________________________________________________________________________"""
print(' # of columns used for train and test : ', len(data_tr.columns))
print(data_tr.columns)

for iiiiii in week_ts:
    print('______________  Week :', iiiiii, '______________')

    data_ts = pd.read_csv(PDM[iiiiii - 21], na_filter=True, skip_blank_lines=True, low_memory=False)

    time = data_ts['time'].tolist()

    mvd = data_ts['mvd'].tolist()
    meb = data_ts['meb'].tolist()
    mbt = data_ts['mbt'].tolist()

    old = data_ts['mdot_old'].tolist()
    y = data_ts['y'].tolist()

    """  ______________ %%%%%%%%%%%%%%%%%%% ____________  """

    """___________________________________________________________________________________"""
    """ One by one drop """
    data_ts.drop(dl, axis=1, inplace=True)

    """___________________________________________________________________________________"""
    data_ts.drop('time', axis=1, inplace=True)
    data_ts.drop('Unnamed: 0', axis=1, inplace=True)
    data_ts.drop('y', axis=1, inplace=True)
    """___________________________________________________________________________________"""
    """___________________________________________________________________________________"""
    """___________________________________________________________________________________"""


    var5 = []
    ld = []
    old = []
    print(data_ts.columns)
    for i in range((data_ts.shape[0])):
        """     ------    NO OLD DATA USED FOR MEMORY OF TRAINING     ------    """
        ld = list(data_ts.iloc[i][:])
        var5.append(regressor.predict([ld])[0])
        """     ------    OLD -1 DATA USED FOR MEMORY OF TRAINING     ------    """
        # if i == 0:
        #     ld = list(data_ts.iloc[i][:])
        #     ld.pop()
        #     ld.append(meb[0])
        #     reg_est = regressor.predict([ld])[0]

            # for i in range(6):
            #     ld.pop()
            #     ld.append(reg_est)
            #     reg_est = regressor.predict([ld])[0]

        #     ld.pop()
        #     ld.append(reg_est)
        #     var5.append(regressor.predict([ld])[0])
        # else:
        #     ld = list(data_ts.iloc[i][:])
        #     ld.pop()
        #     ld.append(var5[i - 1])
        #     reg_est = regressor.predict([ld])[0]
        #     for i in range(6):
        #         ld.pop()
        #         ld.append(reg_est)
        #         reg_est = regressor.predict([ld])[0]
        #     ld.pop()
        #     ld.append(reg_est)
        #     var5.append(regressor.predict([ld])[0])

    """___________________________________________________________________________________"""
    """___________________________________________________________________________________"""
    label = ['not named']*10
    label[0] = 'Time [s]'
    label[1] = 'mmt_cal_volumetric'
    label[2] = 'mmt_cal_energy_bal'
    label[3] = 'mmt_bitzer_poly'
    label[4] = 'mmt+ej_measurement'
    label[5] = 'mmt_data_driven'

    var1 = mvd.copy()
    var2 = meb.copy()
    var3 = mbt.copy()
    var4 = y.copy()

    """  PLOT   """
    plot_5(time, var1, var2, var3, var4, var5, label, iiiiii)

    """ Interpreting the Coefficient and the Intercept """
    # print(regressor.coef_)
    # print(regressor.intercept_)
    # """ Predict the Score (% Accuracy) """
    # print('Train Score :', regressor.score(X_train, y_train))
    # print('Test Score:', regressor.score(X_test, y_test))
    # print('MSE :', metrics.mean_squared_error(y_test, y_pred))
    # print('RMSE :', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

    """  PRINT   """
    print_weekly_ave(var1, var2, var3, var4, var5)
    # print_lengly_ave(var1, var2, var3, var4, var5, step, 720)
    mej = mov_ave(list(np.array(var4)-np.array(var5)),n)
    plot_2(time, mej, mej,['time','mej','mej'],iiiiii)

    print('VD  Calc vs exact Sqr is : ', r2(var1, var4))
    print('EB  Calc vs exact Sqr is : ', r2(var2, var4))
    print('BT  Calc vs exact Sqr is : ', r2(var3, var4))
    print('DD  Calc vs exact Sqr is : ', r2(var5, var4))

    """--------Plot Show-----------"""
    if iiiiii == 30 or iiiiii == 33:

        dict_df = {
            'time': time,
            'mmt': var4
        }
        print('weeks is 30 or 30' ,'###########################3')
    else:
        dict_df = {
            'time': time,
            'mmt': var5
        }

    data_ml = pd.DataFrame(dict_df)

    data_ml.to_csv("Data_mmt" + "Week_" + str(iiiiii))

plt.show()
