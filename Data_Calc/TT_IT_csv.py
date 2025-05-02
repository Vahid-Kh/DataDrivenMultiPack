import pandas as pd  # Dataframe library
import numpy as np  # Scientific computing with nD object support
import matplotlib.pyplot as plt
from datetime import datetime
from TDN import TDN
from functions import mov_ave, plot_corr, plot_5,plot_2,plot_3, print_weekly_ave, print_lengly_ave, is_nan
from sklearn.metrics import r2_score as r2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from statsmodels.tsa.vector_ar.var_model import VAR

""" LT  """
""" Load data as CSV """


W2_ACDX1_HP0_ALC0  = "Data__Week_21"
W3_ACDX1_HP0_ALC0  = "Data__Week_22"
W4_ACDX1_HP0_ALC0  = "Data__Week_23"
W5_ACDX1_HP0_ALC0  = "Data__Week_24"
W6_ACDX1_HP0_ALC0  = "Data__Week_25"
W7_ACDX1_HP0_ALC0  = "Data__Week_26"
W8_ACDX1_HP0_ALC0  = "Data__Week_27"
W28_ACLP1_HP1_ALC1 = "Data__Week_28"
W29_ACLP1_HP0_ALC1 = "Data__Week_29"
W30_ACLP1_HP0_ALC0 = "Data__Week_30"
W31_ACLP1_HP1_ALC0 = "Data__Week_31"
W32_ACDX1_HP0_ALC1 = "Data__Week_32"
W33_ACDX1_HP0_ALC0 = "Data__Week_33"
W34_ACDX1_HP1_ALC0 = "Data__Week_34"
W35_ACDX1_HP1_ALC1 = "Data__Week_35"

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

week = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]



step = 1
n = 180
"""________________________________________________________________________________"""
"""___________________________ LIST OF DROP ITEMS FOR TRAINING ____________________"""

"""                    

                    'mebm'
                    'mbtm'
                    'P6 MT suction'
                    'T14 MT suction'
                    'pwrm'
                    'mebi'
                    'mbti'
                    'P5 Aux HP suction'
                    'P3 AHU evaporation'
                    'T16 Aux suction':

                    'pwri'

"""


dl = [
    'mebl',
    'mbtl',
    'pwrl',
    'sttl',
    'mac',
    'yl',
    # 'mebm',
    # 'mbtm',
    # 'mebi',
    # 'mbti',

    # 'ym'

]

"""________________________________________________________________________________"""

"""Testing weeks"""
week_ts = [28, 29, 30, 31, 32, 33, 34, 35]
week_ts.sort()

"""________________________________________________________________________________"""
data_tr = pd.read_csv(PDM[week_tr[0] - 21], na_filter=True, skip_blank_lines=True, low_memory=False)
for i in week_tr[1:]:
    df = pd.read_csv(PDM[i - 21], na_filter=True, skip_blank_lines=True, low_memory=False)
    data_tr = data_tr.append(df)

cd = [[0]] * 30
dd = [[0]] * 30
for ii in range(len(cd)):
    cd[ii] = []
    dd[ii] = []

data_tr.drop('time', axis=1, inplace=True)
data_tr.drop('Unnamed: 0', axis=1, inplace=True)

y = data_tr['ym'].tolist()

"""  ______________ %%%%%%%%%%%%%%%%%%% ____________  """
"""___________________________________________________________________________________"""
""" DROP FROM LIST """
data_tr.drop([
                'mebl',
                'mbtl',
                'pwrl',
                'sttl',
                'mac',
                'yl',
                'ym',
                'pwrm',
                'mbtm',
                'mbti',
                'pwri',

                'mebi',
                'P5 Aux HP suction',
                'P3 AHU evaporation',
                'T16 Aux suction',
              ], axis=1, inplace=True)



"""                    


mebm,
P3 AHU evaporation,
P6 MT suction,
T14 MT suction,

mebi,
P5 Aux HP suction,
P3 AHU evaporation,
T16 Aux suction,


"""
print(data_tr.columns)

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
    mebi = data_ts['mebi'].tolist()
    ym = data_ts['ym'].tolist()
    mbti = data_ts['mbti'].tolist()
    mac = data_ts['mac'].tolist()
    data_ts.drop([
        'mebl',
        'mbtl',
        'pwrl',
        'sttl',
        'mac',
        'yl',
        'ym',
        'pwrm',
        'mbtm',
        'mbti',
        'pwri',

        'mebm',
        'P3 AHU evaporation',
        'P6 MT suction',
        'T14 MT suction',
    ], axis=1, inplace=True)



    """  ______________ %%%%%%%%%%%%%%%%%%% ____________  """

    """___________________________________________________________________________________"""
    """ One by one drop """


    """___________________________________________________________________________________"""
    data_ts.drop('time', axis=1, inplace=True)
    data_ts.drop('Unnamed: 0', axis=1, inplace=True)

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


    """___________________________________________________________________________________"""
    """___________________________________________________________________________________"""
    label = ['not named']*10
    label[0] = 'Time [s]'
    label[1] = 'mmt'
    label[2] = 'mac'
    label[3] = 'mit_data_driven'


    var1 = mebi.copy()
    var2 = mbti.copy()
    """  PLOT   """
    plot_3(time, ym, mac, var5, label, iiiiii)

    label[0] = 'Time [s]'
    label[1] = 'mit_cal_energy_bal'
    label[2] = 'mit_bitzer_poly'
    label[3] = 'mmt'
    label[4] = 'mac'
    label[5] = 'mit_data_driven'
    # plot_5(time, var1, var2,ym, mac, var5, label, iiiiii)

    """ Interpreting the Coefficient and the Intercept """
    # print(regressor.coef_)
    # print(regressor.intercept_)
    # """ Predict the Score (% Accuracy) """
    # print('Train Score :', regressor.score(X_train, y_train))
    # print('Test Score:', regressor.score(X_test, y_test))
    # print('MSE :', metrics.mean_squared_error(y_test, y_pred))
    # print('RMSE :', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

    """  PRINT   """
    print_weekly_ave(var1, var2, ym, mac, var5)
    # print_lengly_ave(var1, var2, var1, var2, var5, step, 720)

    """--------Plot Show-----------"""
    dict_df = {

        'time': time,
        'mit': var5
    }

    data_ml = pd.DataFrame(dict_df)

    data_ml.to_csv("Data_mit_" + "Week_" + str(iiiiii))



plt.show()
