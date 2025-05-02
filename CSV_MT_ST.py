
import pandas as pd                 # Dataframe library
import numpy as np                  # Scientific computing with nD object support
from datetime import datetime
from TDN import TDN, PSI
from functions import mov_ave

"""________________________________________________________________________________"""

"""------CNR DATA-----"""
W28_ACLP1_HP1_ALC1 = "11_07_2019_to_18_07_2019_converted.csv"
W29_ACLP1_HP0_ALC1 = "18_07_2019_to_25_07_2019_converted.csv"
W30_ACLP1_HP0_ALC0 = "25_07_2019_to_01_08_2019_converted.csv"
W31_ACLP1_HP1_ALC0 = "01_08_2019_to_08_08_2019_converted.csv"
W32_ACDX1_HP0_ALC1 = "08_08_2019_to_15_08_2019_converted.csv"
W33_ACDX1_HP0_ALC0 = "15_08_2019_to_22_08_2019_converted.csv"
W34_ACDX1_HP1_ALC0 = "22_08_2019_to_29_08_2019_converted.csv"
W35_ACDX1_HP1_ALC1 = "29_08_2019_to_05_09_2019_converted.csv"

"""Before Ejector installation"""
W2_ACDX1_HP0_ALC0 = "10_01_2019_to_17_01_2019_converted.csv"
W3_ACDX1_HP0_ALC0 = "17_01_2019_to_24_01_2019_converted.csv"
W4_ACDX1_HP0_ALC0 = "24_01_2019_to_31_01_2019_converted.csv"
W5_ACDX1_HP0_ALC0 = "07_02_2019_to_14_02_2019_converted.csv"
W6_ACDX1_HP0_ALC0 = "14_02_2019_to_21_02_2019_converted.csv"
W7_ACDX1_HP0_ALC0 = "21_02_2019_to_28_02_2019_converted.csv"
W8_ACDX1_HP0_ALC0 = "31_01_2019_to_07_02_2019_converted.csv"

"""No ejector"""
PDM = [

        W2_ACDX1_HP0_ALC0, W3_ACDX1_HP0_ALC0, W4_ACDX1_HP0_ALC0, W5_ACDX1_HP0_ALC0,
        W6_ACDX1_HP0_ALC0, W7_ACDX1_HP0_ALC0, W8_ACDX1_HP0_ALC0,
        W28_ACLP1_HP1_ALC1, W29_ACLP1_HP0_ALC1, W30_ACLP1_HP0_ALC0, W31_ACLP1_HP1_ALC0,
        W32_ACDX1_HP0_ALC1, W33_ACDX1_HP0_ALC0, W34_ACDX1_HP1_ALC0, W35_ACDX1_HP1_ALC1
    ]

"""Label list set up"""
label = [0]*8
label[0] = 'Time [s]'
"""----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """
"""Steps for reading data, takes one data out of #Step """

step_c = 1
length = 500
n = 180    # Moving averaging sample size

"""----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """
""" Time differences for week 28 to 35 
 time_C = [x + (time_D[0]-time_C[0])-td[week-28] for x in time_C]  """

""" :::::::::  """

"""----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """
"""----------------- %%%%%%%--- Bitzer polynomial ---%%%%%%%%------------- """
"""----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """

bitlis = [
r'\4FTC30KSC',
r'\4FTC30KTC',
r'\4HTC20KSC',
r'\4HTC20KTC',
r'\4MTC10KSC',
r'\4MTC10KTC',
r'\6FTE50KSC',
r'\6FTE50KTC'
]

colname = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10 ','nn']
dfbit = pd.read_csv(r'C:\Users\U375297\Documents\PycharmProjects\Danfoss\BitzerPoly' + bitlis[0] + '.csv', names=colname,
                    sep=';', na_filter=True, skiprows=28, nrows=2, decimal=",")
for i in bitlis:
    dfb = pd.read_csv(r'C:\Users\U375297\Documents\PycharmProjects\Danfoss\BitzerPoly' + i + '.csv',names=colname,
                             sep=';', na_filter=True, skiprows=28, nrows=2,decimal=",")
    """ , float_precision='round_trip'   add this to get all digits """
    namechange = i[1:]
    dfb.rename(index={'P [W]': 'P' + namechange}, inplace=True)  # can also use
    dfb.rename(index={'m [kg/h]': 'M' + namechange}, inplace=True)  # can also use
    dfbit = dfbit.append(dfb)

del dfbit['nn']
dfbit = dfbit.transpose()
del dfbit['P [W]']
del dfbit['m [kg/h]']
# with pd.option_context('display.max_rows', 10, 'display.max_columns', None):  # more options can be specified also
#     print(dfbit)

"""----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """
"""----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """
"""----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """

for iiii in [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]:


# for iiii in [21]:
    """----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """
    week = iiii
    print(iiii)


    """--------------------------------"""
    """--------------CNR---------------"""
    """--------------------------------"""

    """ Skip rows every (step)th line  """


    def logic(index):

        if index % step_c == 0:
            return False
        return True


    weekdata = 'Data/' + PDM[week - 21]
    """ DataFrame read from CSV file, na_filter=False, skip_blank_lines=False """
    dfc = pd.read_csv(weekdata, sep=';', skiprows=lambda x: logic(x), na_filter=True, skip_blank_lines=True, low_memory=False)
    dfh = pd.read_csv(weekdata, nrows=1, sep=';')
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

    """___________________________________________________________________________"""

    """----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """
    """----------------- %%%%%%%%%%%--- CALCULATIONS ---%%%%%%%%%------------- """
    """----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """


    """________________________________________________________________________________"""
    """      MT COMPRESSOR GROUP
             -------->         N°2 4FTC – 30K   Displacement (1450 RPM 50Hz)	17,8 m3/h
                                                Displacement (1750 RPM 60Hz)	21,5 m3/h
    Polynomial:
    y = c1 + c2*to + c3*p_HP + c4*to^2 + c5*to*p_HP + c6*p_HP^2 + c7*to^3 + c8*p_HP*to^2 + c9*to*p_HP^2 + c10*p_HP^3
    Coefficients:
    ;c1;c2;c3;c4;c5;c6;c7;c8;c9;c10
    Q [W];0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;
    P [W];-13643,28386766220000000000;-666,71084263225200000000;614,32617126939600000000;-8,53075194384595000000;8,94204364536806000000;-3,13325231781035000000;-0,03290496561987360000;0,02071123587534440000;-0,01403220393964770000;0,00720092009729605000;
    m [kg/h];1713,48733596902000000000;54,08089603726060000000;-5,29454016123850000000;0,84083583901891500000;-0,08071099253171230000;0,00500979706160115000;0,01051434993889650000;-0,00056487233694372300;-0,00001517351860330420;0,00001151066500037660;
    I [A];-5,21031130106921000000;-0,82002430699295500000;0,66199948251390000000;-0,01022777819204650000;0,00976212410081571000;-0,00238589490518005000;-0,00004669608309241090;0,00000689607492902588;-0,00000272237737647322;0,00000411361511514571;
             -------->         N°1 4HTC - 20K   Displacement (1450 RPM 50Hz)	12,0 m3/h
                                                Displacement (1750 RPM 60Hz)	14,5 m3/h
    Polynomial:
    y = c1 + c2*to + c3*p_HP + c4*to^2 + c5*to*p_HP + c6*p_HP^2 + c7*to^3 + c8*p_HP*to^2 + c9*to*p_HP^2 + c10*p_HP^3
    y = c1 + c2*to + c3*p_HP + c4*to^2 + c5*to*p_HP + c6*p_HP^2 + c7*to^3 + c8*p_HP*to^2 + c9*to*p_HP^2 + c10*p_HP^3

    Coefficients:
    ;c1;c2;c3;c4;c5;c6;c7;c8;c9;c10
    Q [W];0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;
    P [W];-9996,06025068975000000000;-453,45246059705600000000;438,53389154674100000000;-4,99962053197480000000;5,91410556930166000000;-2,37086669178297000000;-0,01763906479621670000;0,00320446960309784000;-0,00806664218192681000;0,00574396956895894000;
    m [kg/h];1179,68651817137000000000;36,66723659370270000000;-4,34809546580149000000;0,53933091884398500000;-0,05742948904262850000;0,00667013717377170000;0,00627099810974875000;-0,00035049446629169200;0,00000069362544050556;0,00000222402238978224;
    I [A];-3,71763520443249000000;-0,51023620017299300000;0,42910164729199000000;-0,00509706710487099000;0,00534206831605793000;-0,00150129019520248000;-0,00002582415961714170;-0,00001889511714063800;0,00000620562349152785;0,00000274143760000279;
    """

    """Displacement & Eta"""


    eta_vol_mt = 0.9
    """________________________________________________________________________________"""

    """Energy balance"""
    h14 = dfc['h14 Enthalpy'].tolist()
    h1 = dfc['h1 Enthalpy'].tolist()
    pwrmt = dfc['Power Meter MT'].tolist()

    """Volumetric based on displacement"""
    t14 = dfc['T14 MT suction'].tolist()
    p14 = dfc['P6 MT suction'].tolist()
    p1 = dfc['P1 discharge'].tolist()

    sm1 = dfc['stato_mt1'].tolist()
    sm2 = dfc['stato_mt2'].tolist()
    sm3 = dfc['stato_mt3'].tolist()

    imt1 = dfc['inverter_mt_1'].tolist()

    stm = list((14.4 * np.array(sm1) * (np.array(imt1) / 100 * 30 + 30) / 60 + np.array(sm2) * 17.8 + np.array(sm3) * 17.8) / (17.8 * 2 + 14.4) * 100)
    rc = stm.copy()

    """Displaced volume"""
    vcr = list((14.4 * np.array(sm1) * (np.array(imt1) / 100 * 30 + 30) / 60 + np.array(sm2) * 17.8 + np.array(sm3) * 17.8) / 3600)

    v14 = []
    for i in range(len(h14)):
        v14.append(1 / TDN(p14[i], 0, t14[i], 0, 0, 'CO2').d)

    """_____________________________________ MT ___________________________________________"""

    """  WARNING :::::  CONFIDENTIAL INFORMATION """
    mval = - 0.0967
    pr_0 = 2
    eta_vol_0 = 0.86  #  Initial value suggested by Danfoss
    eta_vol_mt = []
    for i in range(len(p14)):
        fpr = mval*(p1[i]/p14[i] - pr_0) + eta_vol_0
        if fpr <= 0.4:
            eta_vol_mt.append(0.4)
        elif 0.4 < fpr < 0.9:
            eta_vol_mt.append(mval*(fpr) + eta_vol_0)
        else:
            eta_vol_mt.append(0.9)
    """________________________________________________________________________________"""

    """Volumetric based on displacement"""
    if type(eta_vol_mt)== list:
        mmt_cal_vd = list(np.array(vcr)/np.array(v14)*np.array(eta_vol_mt)*0.81) #  [m3/kg]
    else:
        mmt_cal_vd = list(np.array(vcr)/np.array(v14)*eta_vol_mt) #  [m3/kg]

    """Energy balance"""
    mmt_cal_eb = list((np.array(pwrmt)) / (np.array(h1) - np.array(h14)))

    """Direct measurement"""
    mmt = list((np.array(dfc['M4 LT liquid'].tolist()) + np.array(dfc['M3 MT liquid'].tolist())))

    """Bitzer polynomial"""

    to = np.array(dfc['MT evaporation temp'].tolist())-273.15
    p_HP = np.array(dfc['P1 discharge'].tolist())/1e5

    for ii in range(len(p_HP)):
        c = dfbit['M4FTC30KTC'].tolist() if p_HP[ii] > 73.8 else dfbit['M4FTC30KSC'].tolist()

        mdot_4ftc = (c[0] + c[1] * to[ii] + c[2] * p_HP[ii] + c[3] * to[ii] ** 2 + c[4] * to[ii] * p_HP[ii] + c[5] * p_HP[ii] ** 2 + c[6] * to[ii] ** 3 + c[7] * p_HP[ii] * to[ii] ** 2 + c[8] * to[ii] * p_HP[ii] ** 2 + c[9] * p_HP[ii] ** 3)/3600

        c = dfbit['M4HTC20KTC'].tolist() if p_HP[ii] > 73.8 else dfbit['M4HTC20KSC'].tolist()
        mdot_4htc = (c[0] + c[1] * to[ii] + c[2] * p_HP[ii] + c[3] * to[ii] ** 2 + c[4] * to[ii] * p_HP[ii] + c[5] *
                     p_HP[ii] ** 2 + c[6] * to[ii] ** 3 + c[7] * p_HP[ii] * to[ii] ** 2 + c[8] * to[ii] * p_HP[
                         ii] ** 2 + c[9] * p_HP[ii] ** 3) / 3600

    mmt_bitzer = list((np.array(sm1) * (np.array(imt1) / 100 * 30 + 30) / 60 * mdot_4htc + np.array(
        sm2) * mdot_4ftc + np.array(sm3) * mdot_4ftc))


    """________________________________________________________________________________"""

    """ Variables to plot against each other"""
    time = time_C

    """________________________________________________________________________________"""


    """____________________________________________________________"""
    """___________________________ MT _____________________________"""
    """____________________________________________________________"""

    """Mass flow rate"""
    group = "MT"
    var1 = mov_ave(mmt_cal_vd, n)[n:]
    var2 = mov_ave(mmt_cal_eb, n)[n:]
    var3 = mov_ave(mmt_bitzer, n)[n:]
    var4 = mov_ave(mmt, n)[n:]
    from functions import plot_4
    import matplotlib.pyplot as plt

    """ X """
    pwr = mov_ave(pwrmt, n)[n:]
    mvd = mov_ave(mmt_cal_vd, n)[n:]
    meb = mov_ave(mmt_cal_eb, n)[n:]
    mbt = mov_ave(mmt_bitzer, n)[n:]
    stt = mov_ave(stm, n)[n:]

    """ X for n-1 measurement"""
    old = mov_ave(mmt, n)[n - 1:-1]
    old_10 = mov_ave(mmt, n)[n - 10:-10]

    """Initiallize for n-1 data """
    inn = mov_ave(mmt_bitzer, n * 2)[n + 1]

    """ Y """
    mdot = mov_ave(mmt, n)[n:]


    """____________________________________________________________"""
    """________________________ Extra Var _________________________"""
    """____________________________________________________________"""
    time = time[n:]
    mmt = mov_ave(mmt, n)[n:]
    """____________________________________________________________"""

    """ X Extra var """
    cd = [[0] * (len(time) - n)] * 100
    dd = [[0] * (len(time) - n)] * 100
    for ii in range(len(cd)):
        cd[ii] = [0] * len(time)
        dd[ii] = [0] * len(time)

    """_____TRAIN DATA LABELS____"""
    lcd = [

        'T1 MT discharge',
        'T2 After AHU',
        'T3 GC Outlet',
        'T4 Inlet IHX 1',
        'T5 Inlet IHX 2',
        'T6 Receiver',
        'T6 Receiver sat',
        'T7 Ejector inlet',
        'T8 Liquid out IHX',
        'T9 MT section outlet',
        'T10 LT suction',
        'T11 LT discharge',
        'T12 Intercooler outlet',
        'T13 out intercooler and MT section',
        'T14 MT suction',
        'T15 Aux_HP suction',
        'T16 Aux suction',
        'T18 Outlet AHU (heating)',
        'T19 Outlet AHU (cooling)',
        'T20 Outlet AHU (cooling)',
        'T23 LT section outlet',
        'LT evaporation temp',
        'MT evaporation temp',
        'AHU saturation temp',
        'Tair external air',
        'P1 discharge',
        'P2 receiver',
        'P3 AHU evaporation',
        'P4 LT suction',
        'P5 Aux HP suction',
        'P6 MT suction',
        'P7 ejector inlet',
        'M2 AHU vapour (heating)',
        'M3 MT liquid',
        'M4 LT liquid',
        'Mtotal AHU',
        'Power Meter MT',
        'Power Meter AUX',
        'Power Meter LT',
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
        'Cooling duty rooftop AC',

        ]

    """ PREPARE DATA TO CSV """

    for i in range(len(lcd)):
        cd[i] = mov_ave(dfc[lcd[i]].tolist(), n)[n:]

    if iiii < 32:
        mac = list(mov_ave(dfc['M1 AHU liquid (cooling)'].tolist(), n))[n:]
    else:
        mac = list(np.array(mov_ave(dfc['M5 AHU (no ejectors)'].tolist(), n))*10)[n:]

    """___________________________________________________________________________________"""
    dict_df = {

        'time': time,
        'mvd': mvd,
        'meb': meb,
        'mbt': mbt,
        'pwr': pwr,
        'stt': stt,
        'mmt': mmt,
        'mac': mac

        }

    for i in range(len(lcd)):
        dict_df.update({lcd[i]: cd[i]})

    dict_df.update({'mdot_old': old})
    dict_df.update({'mdot_old_10': old_10})

    y = mdot.copy()
    data_ml = pd.DataFrame(dict_df)
    data_ml = data_ml.assign(y=y)
    data_ml = data_ml.assign(p14p1=mov_ave(list(np.array(p1)/np.array(p14)), n)[n:])
    import matplotlib.pyplot as plt
    # plt.plot(data_ml['Power Meter MT'], pmt_bitzer[n:])


    data_ml.to_csv("Data_Calc/Data_"+str(group)+"_Week_" + str(week))


















