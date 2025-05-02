
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


for iiii in [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]:



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
    """      LT COMPRESSOR GROUP      
             -------->    N°2 2JSL – 2K    Displacement (1450 RPM 50Hz)	3,48 m3/h
                                           Displacement (1750 RPM 60Hz)	4,19 m3/h
    Polynomial:
    y = c1 + c2*to + c3*tc + c4*to^2 + c5*to*tc + c6*tc^2 + c7*to^3 + c8*tc*to^2 + c9*to*tc^2 + c10*tc^3
    Coefficients:
    ;c1;c2;c3;c4;c5;c6;c7;c8;c9;c10
    Q [W];20510,94049617030000000000;647,81256904386500000000;-296,93864713199200000000;6,52774298263469000000;-6,60884504606558000000;-0,63273612725138000000;0,01817982556410840000;-0,03126473611652510000;-0,02520160720816570000;0,00459257740214673000;
    P [W];166,13703104020200000000;-115,73319947892600000000;115,60055653982600000000;-2,51301687322319000000;3,12780752312994000000;-0,44582034965388400000;-0,01433680094693460000;0,02331698847080350000;-0,01009677754482320000;0,00034107617277647700;
    m [kg/h];296,59201587773500000000;9,42182985900289000000;-1,44621832461110000000;0,09768881336021270000;-0,01079987535353640000;-0,01562349801007640000;0,00029924094397134200;0,00022803894511386300;-0,00043900058770621500;0,00008925289341499110;
    I [A];2,08027975962107000000;-0,11616979918383000000;0,10267114363108200000;-0,00246722498288618000;0,00200720036067185000;0,00062967029085192700;-0,00001326624573745780;0,00000458786659162303;0,00001466893346029640;-0,00000431654102380788;
      
             -------->    N°1 2KSL – 1K    Displacement (1450 RPM 50Hz)	2,71 m3/h
                                           Displacement (1750 RPM 60Hz)	3,27 m3/h
    Polynomial:
    y = c1 + c2*to + c3*tc + c4*to^2 + c5*to*tc + c6*tc^2 + c7*to^3 + c8*tc*to^2 + c9*to*tc^2 + c10*tc^3
    
    Coefficients:
    ;c1;c2;c3;c4;c5;c6;c7;c8;c9;c10
    Q [W];15896,68665954770000000000;499,70136822972100000000;-278,44039579102400000000;5,07255843301259000000;-7,80635767559493000000;1,46474177324694000000;0,01687273801309690000;-0,06596979233938960000;0,03344351816202920000;-0,01159329197541470000;
    P [W];-92,73977285674720000000;-114,32967400843200000000;96,93031634431390000000;-2,82336470316991000000;2,97120573185892000000;-0,49851123170513600000;-0,01946685346998670000;0,02365530259567270000;-0,01045538770667700000;0,00330776563937487000;
    m [kg/h];229,87798981838300000000;7,28094869278073000000;-1,82989947185668000000;0,07675072678372710000;-0,04929911818702500000;0,01548347598113250000;0,00028550956424787500;-0,00048243085879053700;0,00044045778395725100;-0,00013133866980480100;
    I [A];1,66861000902189000000;-0,11073788742793800000;0,08424911269322390000;-0,00273704256951700000;0,00215574359664638000;0,00025459688499864700;-0,00001890293305962620;0,00001095686852550460;0,00000789253111810644;-0,00000148589994471754;
    
    """
    """________________________________________________________________________________"""



    """Rule of thumb :: """
    eta_vol_lt = 0.9 #  Assuming constant value for Volumetric efficiency

    """________________________________________________________________________________"""

    """Energy balance"""
    h10 = dfc['h10 Enthalpy'].tolist()
    h11 = dfc['h11 Enthalpy'].tolist()
    pwrlt = dfc['Power Meter LT'].tolist()

    """Volumetric based on displacement"""
    t10 = dfc['T10 LT suction'].tolist()
    t11 = dfc['T11 LT discharge'].tolist()
    p10 = dfc['P4 LT suction'].tolist()
    p11 = dfc['P6 MT suction'].tolist()    # Used in volumetric efficiency
    # print('Average frequency percentage  ', sum(invlt)/len(invlt))

    """Running Capacity"""
    sl1 = dfc['stato_lt1'].tolist()
    sl2 = dfc['stato_lt2'].tolist()
    sl3 = dfc['stato_lt3'].tolist()

    ilt1 = dfc['inverter_bt_1'].tolist()

    """Displaced volume"""
    vcr = list((3.24 * np.array(sl1) * (np.array(ilt1) / 100 * 30 + 30) / 60 + np.array(sl2) * 3.5 + np.array(sl3) * 3.5)/3600)
    # vcr = list((3.24 * np.array(sl1) * (np.array(ilt1) / 100 * 30 + 30) / 60 + np.array(sl2) * 3.5 + np.array(sl3) * 3.5) / 3600)

    """ Variables to plot against each other"""
    time = time_C
    stl = list((3.24 * np.array(sl1) * (np.array(ilt1) / 100 * 30 + 30) / 60 + np.array(sl2) * 3.5 + np.array(sl3) * 3.5) / ( 3.5 * 2 + 3.24) * 100)

    rc = stl.copy()

    v10 = []
    for i in range(len(h10)):
        v10.append(1 / TDN(p10[i], h10[i], 0, 0, 0, 'CO2').d)

    """__________________________________________ LT ______________________________________"""

    """  WARNING :::::  CONFIDENTIAL INFORMATION """
    eta_vol_lt = []
    mval = - 0.0967
    pr_0 = 2
    eta_vol_0 = 0.86  #  Initial value suggested by Danfoss
    for i in range(len(p10)):
        fpr = mval*(p11[i]/p10[i] - pr_0) + eta_vol_0
        if fpr <= 0.4:
            eta_vol_lt.append(0.4)
        elif 0.4 < fpr < 0.9:
            eta_vol_lt.append(mval*(p11[i]/p10[i] - pr_0) + eta_vol_0)
        else:
            eta_vol_lt.append(0.9)
    """________________________________________________________________________________"""
    """Volumetric based on displacement"""
    if type(eta_vol_lt) == list:
        mlt_cal_vd = list(np.array(vcr)/np.array(v10)*np.array(eta_vol_lt)) #  [m3/kg]
    else:
        mlt_cal_vd = list(np.array(vcr)/np.array(v10)*eta_vol_lt) #  [m3/kg]

    """Direct measurement"""
    mlt = list(np.array(dfc['M4 LT liquid'].tolist()))

    """Energy balance"""
    mlt_cal_eb = list((np.array(pwrlt)) / (np.array(h11) - np.array(h10)))

    """Bitzer polynomial"""
    """For mass flow rate [Kg/h]"""

    mc_2jsl = [296.59201587773500000000, 9.42182985900289000000, -1.44621832461110000000, 0.09768881336021270000, -0.01079987535353640000, -0.01562349801007640000, 0.00029924094397134200, 0.00022803894511386300, -0.00043900058770621500, 0.00008925289341499110]
    mc_2ksl = [229.87798981838300000000, 7.28094869278073000000, -1.82989947185668000000, 0.07675072678372710000, -0.04929911818702500000, 0.01548347598113250000, 0.00028550956424787500, -0.00048243085879053700, 0.00044045778395725100, -0.00013133866980480100]

    pc_2jsl = [166.13703104020200000000, -115.73319947892600000000, 115.60055653982600000000, -2.51301687322319000000, 3.12780752312994000000, -0.44582034965388400000, -0.01433680094693460000, 0.02331698847080350000, -0.01009677754482320000, 0.00034107617277647700]
    pc_2ksl = [-92.73977285674720000000, -114.32967400843200000000, 96.93031634431390000000, -2.82336470316991000000, 2.97120573185892000000, -0.49851123170513600000, -0.01946685346998670000, 0.02365530259567270000, -0.01045538770667700000, 0.00330776563937487000]

    c = mc_2jsl


    to = np.array(dfc['LT evaporation temp'].tolist())-273.15

    pc = np.array(dfc['P6 MT suction'].tolist())

    tcl = []

    for iii in pc:
        tcl.append(PSI('T', 'P', iii, 'Q', 1, 'CO2'))


    tc = np.array(tcl)-273.15

    # tc = np.array(dfc['AK-PC 782A:   Tc-LT'].tolist())

    mdot_2jsl = (c[0] + c[1] * to + c[2] * tc + c[3] * to ** 2 + c[4] * to * tc + c[5] * tc ** 2 + c[6] * to ** 3 + c[7] * tc * to ** 2 + c[8] * to * tc ** 2 + c[9] * tc ** 3)/3600
    c = mc_2ksl
    mdot_2ksl = (c[0] + c[1] * to + c[2] * tc + c[3] * to ** 2 + c[4] * to * tc + c[5] * tc ** 2 + c[6] * to ** 3 + c[7] * tc * to ** 2 + c[8] * to * tc ** 2 + c[9] * tc ** 3)/3600
    c = pc_2jsl
    pwr_2jsl = (c[0] + c[1] * to + c[2] * tc + c[3] * to ** 2 + c[4] * to * tc + c[5] * tc ** 2 + c[6] * to ** 3 + c[7] * tc * to ** 2 + c[8] * to * tc ** 2 + c[9] * tc ** 3)
    c = pc_2ksl
    pwr_2ksl = (c[0] + c[1] * to + c[2] * tc + c[3] * to ** 2 + c[4] * to * tc + c[5] * tc ** 2 + c[6] * to ** 3 + c[7] * tc * to ** 2 + c[8] * to * tc ** 2 + c[9] * tc ** 3)

    mlt_bitzer = list((np.array(sl1) * (np.array(ilt1) / 100 * 30 + 30) / 60 * mdot_2ksl + np.array(sl2) * mdot_2jsl + np.array(sl3) * mdot_2jsl))

    plt_bitzer = list((np.array(sl1) * (np.array(ilt1) / 100 * 30 + 30) / 60 * pwr_2ksl + np.array(sl2) * pwr_2jsl + np.array(sl3) * pwr_2jsl))
    """________________________________________________________________________________"""

    """Direct measurement"""
    mmt = list((np.array(dfc['M4 LT liquid'].tolist()) + np.array(dfc['M3 MT liquid'].tolist())))

    """________________________________________________________________________________"""

    """________________________________________________________________________________"""

    """ Variables to plot against each other"""
    time = time_C

    """____________________________________________________________"""
    """___________________________ LT _____________________________"""
    """____________________________________________________________"""

    group = "LT"
    """Mass flow rate"""
    var1 = mov_ave(mlt_cal_vd, n)[n:]
    var2 = mov_ave(mlt_cal_eb, n)[n:]
    var3 = mov_ave(mlt_bitzer, n)[n:]
    var4 = mov_ave(mlt, n)[n:]

    """ X """
    pwr = mov_ave(pwrlt, n)[n:]
    mvd = mov_ave(mlt_cal_vd, n)[n:]
    meb = mov_ave(mlt_cal_eb, n)[n:]
    mbt = mov_ave(mlt_bitzer, n)[n:]
    stt = mov_ave(stl, n)[n:]

    """ X for n-1 measurement"""
    old = mov_ave(mlt, n)[n-1:-1]
    old_10 = mov_ave(mlt, n)[n - 10:-10]

    """Initiallize for n-1 data """
    inn = mov_ave(mlt_bitzer, n * 2)[n + 1]

    """ Y """
    mdot = mov_ave(mlt, n)[n:]


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
        # 'T21 Water in DHW',
        # 'T22 Water out DHW',
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
        # 'h21 Enthalpy',
        # 'h22 Enthalpy',
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

    data_ml.to_csv("Data_Calc/Data_"+str(group)+"_Week_" + str(week))
