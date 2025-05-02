import pandas as pd  # Dataframe library
import numpy as np  # Scientific computing with nD object support
import matplotlib.pyplot as plt
from datetime import datetime
from TDN import TDN, PSI
from functions import mov_ave, plot_corr, plot_5,plot_2, print_weekly_ave, print_lengly_ave, is_nan
from sklearn.metrics import r2_score as r2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from statsmodels.tsa.vector_ar.var_model import VAR

"""________________________________________________________________________________"""
""" LT  """
""" Load data as CSV """
W28_ACLP1_HP1_ALC1 = "Data_LT_Week_28"
W29_ACLP1_HP0_ALC1 = "Data_LT_Week_29"
W30_ACLP1_HP0_ALC0 = "Data_LT_Week_30"
W31_ACLP1_HP1_ALC0 = "Data_LT_Week_31"
W32_ACDX1_HP0_ALC1 = "Data_LT_Week_32"
W33_ACDX1_HP0_ALC0 = "Data_LT_Week_33"
W34_ACDX1_HP1_ALC0 = "Data_LT_Week_34"
W35_ACDX1_HP1_ALC1 = "Data_LT_Week_35"
#
PDM = [W28_ACLP1_HP1_ALC1, W29_ACLP1_HP0_ALC1, W30_ACLP1_HP0_ALC0, W31_ACLP1_HP1_ALC0,
       W32_ACDX1_HP0_ALC1, W33_ACDX1_HP0_ALC0, W34_ACDX1_HP1_ALC0, W35_ACDX1_HP1_ALC1]
#
"""Training weeks"""
week_tr = [29, 31]

"""________________________________________________________________________________"""

# """ MT  """
# """ Load data as CSV """
# W28_ACLP1_HP1_ALC1 = "Data_MT_Week_28"
# W29_ACLP1_HP0_ALC1 = "Data_MT_Week_29"
# W30_ACLP1_HP0_ALC0 = "Data_MT_Week_30"
# W31_ACLP1_HP1_ALC0 = "Data_MT_Week_31"
# W32_ACDX1_HP0_ALC1 = "Data_MT_Week_32"
# W33_ACDX1_HP0_ALC0 = "Data_MT_Week_33"
# W34_ACDX1_HP1_ALC0 = "Data_MT_Week_34"
# W35_ACDX1_HP1_ALC1 = "Data_MT_Week_35"

# PDM = [W28_ACLP1_HP1_ALC1, W29_ACLP1_HP0_ALC1, W30_ACLP1_HP0_ALC0, W31_ACLP1_HP1_ALC0,
#        W32_ACDX1_HP0_ALC1, W33_ACDX1_HP0_ALC0, W34_ACDX1_HP1_ALC0, W35_ACDX1_HP1_ALC1]


"""________________________________________________________________________________"""

"""Training weeks"""
week_tr = [28, 29, 30, 31, 32, 33, 34, 35]

"""________________________________________________________________________________"""
"""___________________________ LIST OF DROP ITEMS FOR TRAINING ____________________"""

dl = [
        'mvd',
        'meb',
        'mbt',
        'mlt_old',

        'h10',
        'h11',
        'p10',
        'p11',
        'pwrlt',
        'invlt',

        'T1 MT discharge',                    #  0.328
        'T2 After AHU',                       #  0.239
        'T3 GC Outlet',                       #  0.296
        'T4 Inlet IHX 1',                     #  0.298
        'T5 Inlet IHX 2',                     #  0.307
        'T6 Receiver',                        #  0.191
        'T6 Receiver sat',                    #  0.278
        'T7 Ejector inlet',                   #  -0.072
        'T8 Liquid out IHX',                  #  0.074
        'T9 MT section outlet',               #  -0.15
        'T10 LT suction',                     #  -0.027
        'T11 LT discharge',                   #  0.12
        'T12 Intercooler outlet',             #  0.335
        'T13 out intercooler and MT section', #  -0.157
        'T14 MT suction',                     #  -0.157
        'T15 Aux_HP suction',                 #  -0.3
        'T16 Aux suction',                    #  -0.111
        'T18 Outlet AHU (heating)',           #  0.275
        'T19 Outlet AHU (cooling)',           #  -0.24
        'T20 Outlet AHU (cooling)',           #  -0.072
        'T21 Water in DHW',                   #  0.097
        'T22 Water out DHW',                  #  -0.007
        'T23 LT section outlet',              #  -0.138
        'LT evaporation temp',                #  0.103
        'MT evaporation temp',                #  0.098
        'AHU saturation temp',                #  0.278
        'Tair external air',                  #  0.325
        'P1 discharge',                       #  0.397
        'P2 receiver',                        #  0.28
        'P3 AHU evaporation',                 #  0.332
        'P4 LT suction',                      #  0.103
        'P5 Aux HP suction',                  #  0.276
        'P6 MT suction',                      #  0.098
        'P7 ejector inlet',                   #  0.4
        'M1 AHU liquid (cooling)',
        'M2 AHU vapour (heating)',
        'M3 MT liquid',
        'M4 LT liquid',
        'M5 AHU (no ejectors)',
        'Mtotal AHU',                         #  0.244
        'Power Meter MT',                     #  0.312
        'Power Meter AUX',                    #  0.138
        'Power Meter LT',                     #  0.166
        'Total Power',                        #  0.235
        'h1 Enthalpy',                        #  0.073
        'h2 Enthalpy',                        #  -0.016
        'h3 Enthalpy',                        #  0.068
        'h4 Enthalpy',                        #  0.074
        'h5 Enthalpy',                        #  0.221
        'h6 Enthalpy sat',                    #  -0.284
        'h7 Enthalpy',                        #  -0.203
        'h9 Enthalpy',                        #  -0.217
        'h10 Enthalpy',                       #  -0.07
        'h11 Enthalpy',                       #  0.074
        'h12 Enthalpy',                       #  0.244
        'h13 Enthalpy',                       #  -0.235
        'h14 Enthalpy',                       #  -0.239
        'h15 Enthalpy',                       #  -0.38
        'h16 Enthalpy',                       #  -0.307
        'h17 Enthalpy',                       #  -0.394
        'h18 Enthalpy',                       #  0.062
        'h19 Enthalpy',                       #  -0.363
        'h20 Enthalpy',                       #  -0.204
        'h21 Enthalpy',                       #  0.097
        'h22 Enthalpy',                       #  -0.007
        'h23 Enthalpy',                       #  -0.15
        'h8 Enthalpy calc',                   #  0.145
        'hmix Enthalpy',                      #  0.009
        'T8 calculated',                      #  0.272
        'Accumulated Etot',                   #  0.091
        'Accumulated E_MT',                   #  0.094
        'Accumulated E_LT',                   #  0.085
        'Accumulated E_AUX',                  #  0.088
        'Number of Cycles MT2',               #  0.1
        'Number of Cycles AUX2',              #  0.086
        'Number of Cycles AUX4',              #  0.086
        'Accumulated Pevap P3',               #  0.092
        'Accumulated Pevap P4',               #  0.092
        'Accumulated Pevap P6',               #  0.092
        'Cooling duty LT evap',               #  0.385
        'Cooling duty rooftop AC',            #  0.239
        'Accumulated cooling MT evap',        #  0.093
        'Accumulated cooling LT evap',        #  0.085
        'Accumulated cooling rooftop',        #  0.09

        'AK-PC 782A:   Pgc',
        'AK-PC 782A:   Running capacity LT',
        'AK-PC 782A:   Vrec OD',
        'AK-PC 782A:   Requested cap. MT',
        'AK-PC 782A:   Sd-MT',
        'AK-PC 782A:   Ss-MT',
        'Controlo Inj. UTA1:   Actual OD',
        'Controlo Inj. UTA2:   Actual OD',
        'AK-PC 782A:   Liq. inj. status MT',
        'AK-PC 782A:   Requested cap. MT',
        'AK-PC 782A:   Suction reference MT',
        'AK-PC 782A:   Suction temp. To-MT',
        'AK-PC 782A:   Requested cap. LT',
        'AK-PC 782A:   Superheat LT'

        ]

for iii in week_tr:
    """________________________________________________________________________________"""
    data_tr = pd.read_csv(PDM[iii-28], na_filter=True, skip_blank_lines=True, low_memory=False)

    """___________________________________________________________________________________"""
    label = ['not named'] * 10
    label[0] = 'time [s] (120 sec sampling)'
    label[1] = 'Mtotal AHU'
    label[2] = 'Average AHU Actual OD'
    label[3] = 'mlt_bitzer_poly'
    label[4] = 'mlt_measurement'
    label[5] = 'mlt_data_driven'


    time = data_tr['time'].tolist()
    var1 = mov_ave(data_tr['M1 AHU liquid (cooling)'].tolist())
    var2 = mov_ave(data_tr['M5 AHU (no ejectors)'].tolist())
    var3 = mov_ave(data_tr['Controlo Inj. UTA1:   Actual OD'].tolist())
    var4 = mov_ave(data_tr['Controlo Inj. UTA2:   Actual OD'].tolist())

    var3 = list(((np.array(var3) + np.array(var4)))/200)

    od = list(((np.array(var3) + np.array(var4))) / 200)

    """ Mass flow for CCMT 16 """
    k = 50.56 *(0.477*np.array(od)+0.234*np.array(od)**2-0.197*np.array(od)**3+1.954*np.array(od)**4-1.468*np.array(od)**5)
    p_i = mov_ave(data_tr['P2 receiver'].tolist())
    p_o = mov_ave(data_tr['P3 AHU evaporation'].tolist())
    h_8 = mov_ave(data_tr['T8 calculated'].tolist())
    rho_i = []
    for i in range(len(p_i)):
        # rho_i.append(TDN(p_i[i], h_8[i], 0, 0, 0, 'CO2').d)
        rho_i.append(PSI('D', 'P', p_i[i], 'Q', 0, 'CO2'))

    var5 =list((k*2/3*np.sqrt(((np.array(p_i)-np.array(p_o))/1e5*np.array(rho_i))))*2/3600)
    print((np.array(p_i)-np.array(p_o))/1e5)
    if iii < 32:
        var1= var1.copy()
        # var1 = list((np.array(var1) + np.array(var2)*10))
    else:
        var1=list((np.array(var2)*10))
    # n=20
    # ds = 720  # One day data
    # cp1 = np.polyfit(var3[n:n + ds], var1[n:n + ds], 3)  # VD
    # var3 = [cp1[0]*x*x*x + cp1[1]*x*x + cp1[2]*x + cp1[3] for x in var3]
    # var3 = [cp1[0] * x + cp1[1] for x in var3]

    plot_2(time, var1, var5, label, iii)
    # print('Calc vs exact Sqr is : ', r2(var1, var3))
    print('Calc vs exact Sqr is : ', r2(var5, var3))
plt.show()