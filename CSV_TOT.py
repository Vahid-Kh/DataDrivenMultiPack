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
for iiii in [ 28, 29, 30, 31, 32, 33, 34, 35]:
# for iiii in [35]:

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

    """___________________________________________________________________________________"""

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

    stm = list(
        (14.4 * np.array(sm1) * (np.array(imt1) / 100 * 30 + 30) / 60 + np.array(sm2) * 17.8 + np.array(sm3) * 17.8) / (
                    17.8 * 2 + 14.4) * 100)
    rc = stm.copy()

    """Displaced volume"""
    vcr = list((14.4 * np.array(sm1) * (np.array(imt1) / 100 * 30 + 30) / 60 + np.array(sm2) * 17.8 + np.array(
        sm3) * 17.8) / 3600)

    v14 = []
    for i in range(len(h14)):
        v14.append(1 / TDN(p14[i], 0, t14[i], 0, 0, 'CO2').d)

    """_____________________________________ MT ___________________________________________"""

    """  WARNING :::::  CONFIDENTIAL INFORMATION """
    mval = - 0.0967
    pr_0 = 2
    eta_vol_0 = 0.86  # Initial value suggested by Danfoss
    eta_vol_mt = []
    for i in range(len(p14)):
        fpr = mval * (p1[i] / p14[i] - pr_0) + eta_vol_0
        if fpr <= 0.4:
            eta_vol_mt.append(0.4)
        elif 0.4 < fpr < 0.9:
            eta_vol_mt.append(mval * (fpr) + eta_vol_0)
        else:
            eta_vol_mt.append(0.9)
    """________________________________________________________________________________"""

    """Volumetric based on displacement"""
    if type(eta_vol_mt) == list:
        mmt_cal_vd = list(np.array(vcr) / np.array(v14) * np.array(eta_vol_mt) * 0.81)  # [m3/kg]
    else:
        mmt_cal_vd = list(np.array(vcr) / np.array(v14) * eta_vol_mt)  # [m3/kg]

    """Energy balance"""
    mmt_cal_eb = list((np.array(pwrmt)) / (np.array(h1) - np.array(h14)))

    """Direct measurement"""
    m3m4 = list((np.array(dfc['M4 LT liquid'].tolist()) + np.array(dfc['M3 MT liquid'].tolist())))

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


    """________________________________________________________________________________"""

    """ X """

    mebm = mov_ave(mmt_cal_eb, n)[n:]
    mbtm = mov_ave(mmt_bitzer, n)[n:]


    """________________________________________________________________________________"""

    """      IT COMPRESSOR GROUP
             -------->   N°2 4FTC – 30K    Displacement (1450 RPM 50Hz)	17,8 m3/h
                                           Displacement (1750 RPM 60Hz)	21,5 m3/h
    Polynomial:
    y = c1 + c2*to + c3*p_HP + c4*to^2 + c5*to*p_HP + c6*p_HP^2 + c7*to^3 + c8*p_HP*to^2 + c9*to*p_HP^2 + c10*p_HP^3

    Coefficients:
    ;c1;c2;c3;c4;c5;c6;c7;c8;c9;c10
    Q [W];0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;
    P [W];-13643,28386766220000000000;-666,71084263225200000000;614,32617126939600000000;-8,53075194384595000000;8,94204364536806000000;-3,13325231781035000000;-0,03290496561987360000;0,02071123587534440000;-0,01403220393964770000;0,00720092009729605000;
    m [kg/h];1713,48733596902000000000;54,08089603726060000000;-5,29454016123850000000;0,84083583901891500000;-0,08071099253171230000;0,00500979706160115000;0,01051434993889650000;-0,00056487233694372300;-0,00001517351860330420;0,00001151066500037660;
    I [A];-5,21031130106921000000;-0,82002430699295500000;0,66199948251390000000;-0,01022777819204650000;0,00976212410081571000;-0,00238589490518005000;-0,00004669608309241090;0,00000689607492902588;-0,00000272237737647322;0,00000411361511514571;
             -------->   N°1 6FTE  - 50K   Displacement (1450 RPM 50Hz)	26,1 m3/h
                                           Displacement (1750 RPM 60Hz)	31,5 m3/h
     Polynomial:
    y = c1 + c2*to + c3*p_HP + c4*to^2 + c5*to*p_HP + c6*p_HP^2 + c7*to^3 + c8*p_HP*to^2 + c9*to*p_HP^2 + c10*p_HP^3

    Coefficients:
    ;c1;c2;c3;c4;c5;c6;c7;c8;c9;c10
    Q [W];0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;
    P [W];-15179,34653465370000000000;-464,76089108911400000000;754,70346534654100000000;-4,01655742574261000000;1,45824059405950000000;-3,04439702970303000000;0,01023326732673290000;-0,05662407920792040000;0,03846002970296980000;0,00535540990099028000;
    m [kg/h];2396,20919901144000000000;69,44488997941970000000;-5,00691806645456000000;0,89933950704311000000;-0,00410373098917569000;-0,00457899885315816000;0,00873555952226036000;0,00163967376135646000;-0,00027724105256122200;-0,00000000165694955946;
    I [A];-12,77437637595140000000;-0,88585754644045700000;1,60550156266857000000;-0,01021438602415680000;0,00838224822566439000;-0,00993741438641449000;0,00001826091361082530;-0,00001527328831839150;0,00001228713095414150;0,00002451198070785530;

             IT Valve separated (VARISPEED SERIES)
             @@@@@@@@  WARNING ::: DATA IS FOR MTE -10K WHICH IS THE ONLY SIMILAR MODEL AVAILABLE IN BITZER SOFTWARE @@@@@@@@
             -------->   N°1 4MTC  - 10K   Displacement (1450 RPM 50Hz)	6,5 m3/h
                                           Displacement (1750 RPM 60Hz)	7,8 m3/h
    Polynomial:
    y = c1 + c2*to + c3*p_HP + c4*to^2 + c5*to*p_HP + c6*p_HP^2 + c7*to^3 + c8*p_HP*to^2 + c9*to*p_HP^2 + c10*p_HP^3

    Coefficients:
    ;c1;c2;c3;c4;c5;c6;c7;c8;c9;c10
    Q [W];0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;0,00000000000000000000;
    P [W];-4382,67634199997000000000;-132,05744640000000000000;185,89802219999900000000;-1,01561159700000000000;-0,26110268909999600000;-0,54099135089999100000;0,00344413347300000000;-0,02375192358000000000;0,01719785826000000000;-0,00000000000000002818;
    m [kg/h];657,01624068665400000000;26,10576311752670000000;-4,23401414159409000000;0,59904521603669500000;-0,09928305379032660000;0,02405203148063410000;0,00843630458267610000;-0,00131558951278288000;0,00023077486161974100;-0,00007192875085841990;
    I [A];0,77462424959847400000;-0,07504133652723010000;0,14511366625791000000;-0,00012093213136762200;-0,00260795655080557000;0,00028868093096700100;0,00000491586415055961;-0,00004647902450104570;0,00003554125399509320;-0,00000302594180135315;


    """
    """________________________________________________________________________________"""

    """Displacement & Eta"""
    eta_vol_it = 0.9
    """________________________________________________________________________________"""

    """Energy balance"""
    h15i = dfc['h15 Enthalpy'].tolist()  # Inlets
    h16i = dfc['h16 Enthalpy'].tolist()  # Inlets
    h15 = list((np.array(h15i) + np.array(h16i)) / 2)
    h1 = dfc['h1 Enthalpy'].tolist()  # Outlet
    pwrit = dfc['Power Meter AUX'].tolist()

    """Volumetric based on displacement"""
    t15 = dfc['T15 Aux_HP suction'].tolist()
    t16 = dfc['T16 Aux suction'].tolist()
    p15i = dfc['P5 Aux HP suction'].tolist()
    p16i = dfc['P2 receiver'].tolist()
    p1 = dfc['P1 discharge'].tolist()
    p15 = list((np.array(p16i) + np.array(p15i)) / 2)

    si1 = dfc['stato_aux1'].tolist()
    si2 = dfc['stato_aux2'].tolist()
    si3 = dfc['stato_aux3'].tolist()
    si4 = dfc['stato_aux4'].tolist()
    iit1 = dfc['inverter_aux_1'].tolist()
    sti = list((7.8 * np.array(si1) * (np.array(iit1) / 100 * 30 + 30) / 60 + np.array(si2) * 17.8 + np.array(
        si3) * 17.8 + np.array(si4) * 26.1) / (17.8 * 2 + 7.8 + 26.1) * 100)

    rc = sti.copy()

    vcr = list((7.8 * np.array(si1) * (np.array(iit1) / 100 * 30 + 30) / 60 + np.array(si2) * 17.8 + np.array(
        si3) * 17.8 + np.array(si4) * 26.1) / 3600)

    v15 = []
    for i in range(len(h15)):
        v15.append((1 / TDN(p16i[i], 0, t16[i], 0, 0, 'CO2').d + 1 / TDN(p15i[i], 0, t15[i], 0, 0, 'CO2').d) / 2)
    """_________________________________________ IT _______________________________________"""

    """  WARNING :::::  CONFIDENTIAL INFORMATION """
    mval = - 0.0967
    pr_0 = 2
    eta_vol_0 = 0.86  # Initial value suggested by Danfoss
    eta_vol_it = []
    for i in range(len(p1)):
        fpr = mval * (p1[i] / p15[i] - pr_0) + eta_vol_0
        if fpr <= 0.4:
            eta_vol_it.append(0.4)
        elif 0.4 < fpr < 0.9:
            eta_vol_it.append(mval * (fpr) + eta_vol_0)
        else:
            eta_vol_it.append(0.9)
    """________________________________________________________________________________"""

    """________________________________________________________________________________"""
    """Volumetric based on displacement"""
    if type(eta_vol_it) == list:
        mit_cal_vd = list(np.array(vcr) / np.array(v15) * np.array(eta_vol_it))  # [m3/kg]
    else:
        mit_cal_vd = list(np.array(vcr) / np.array(v15) * eta_vol_it)  # [m3/kg]

    """Energy balance"""
    mit_cal_eb = list((np.array(pwrit)) / (np.array(h1) - np.array(h15)))

    """Bitzer polynomial"""


    """  Mass flow rate [Kg/h]  """
    to = np.array(dfc['T16 Aux suction'].tolist()) - 273.15
    p_HP = np.array(dfc['P1 discharge'].tolist()) / 1e5

    for ii in range(len(p_HP)):
        c = dfbit['M4FTC30KTC'].tolist() if p_HP[ii] > 73.8 else dfbit['M4FTC30KSC'].tolist()
        mdot_4ftc = (c[0] + c[1] * to[ii] + c[2] * p_HP[ii] + c[3] * to[ii] ** 2 + c[4] * to[ii] * p_HP[ii] + c[5] *
                     p_HP[ii] ** 2 + c[6] * to[ii] ** 3 + c[7] * p_HP[ii] * to[ii] ** 2 + c[8] * to[ii] * p_HP[ii] ** 2
                     + c[9] * p_HP[ii] ** 3)/3600

        c = dfbit['M6FTE50KTC'].tolist() if p_HP[ii] > 73.8 else dfbit['M6FTE50KSC'].tolist()
        mdot_6fte = (c[0] + c[1] * to[ii] + c[2] * p_HP[ii] + c[3] * to[ii] ** 2 + c[4] * to[ii] * p_HP[ii] + c[5] *
                     p_HP[ii] ** 2 + c[6] * to[ii] ** 3 + c[7] * p_HP[ii] * to[ii] ** 2 + c[8] * to[ii] * p_HP[
                         ii] ** 2 + c[9] * p_HP[ii] ** 3) / 3600

        c = dfbit['M4MTC10KTC'].tolist() if p_HP[ii] > 73.8 else dfbit['M4MTC10KSC'].tolist()
        mdot_4mtc = (c[0] + c[1] * to[ii] + c[2] * p_HP[ii] + c[3] * to[ii] ** 2 + c[4] * to[ii] * p_HP[ii] + c[5] *
                     p_HP[ii] ** 2 + c[6] * to[ii] ** 3 + c[7] * p_HP[ii] * to[ii] ** 2 + c[8] * to[ii] * p_HP[
                         ii] ** 2 + c[9] * p_HP[ii] ** 3) / 3600

    mit_bitzer = list((mdot_4mtc * np.array(si1) * (np.array(iit1) / 100 * 30 + 30) / 60 + np.array(
        si2) * mdot_4ftc + np.array(si3) * mdot_4ftc + np.array(si4) * mdot_6fte))


    """____________________________________________________________"""
    """____________________________________________________________"""
    """________________________ Extra Var _________________________"""
    """____________________________________________________________"""
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
        'T21 Water in DHW',
        'T22 Water out DHW',
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
        'DHW water',

        'Power Meter MT',
        'Power Meter AUX',
        'Power Meter LT',

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
        'h21 Enthalpy',
        'h22 Enthalpy',
        'h23 Enthalpy',
        'h8 Enthalpy calc',
        'hmix Enthalpy',
        'T8 calculated',

        'Cooling duty LT evap',
        'Cooling duty rooftop AC',

        'inverter_aux_1',
        'inverter_bt_1',
        'inverter_mt_1',
        'stato_mt1',
        'stato_mt2',
        'stato_mt3',
        'stato_aux1',
        'stato_aux2',
        'stato_aux3',
        'stato_aux4',
        'stato_lt1',
        'stato_lt2',
        'stato_lt3'

    ]

    """____________________________________________________________"""
    """_________________      Dict format        __________________"""
    """____________________________________________________________"""

    time = time[n:]
    print(len(time))
    """____________________________________________________________"""

    if iiii < 32:
        mac = list(mov_ave(dfc['M1 AHU liquid (cooling)'].tolist(), n))[n:]
    else:
        mac = list(np.array(mov_ave(dfc['M5 AHU (no ejectors)'].tolist(), n)) * 10)[n:]
    print(len(mac))
    """ PREPARE DATA TO CSV """
    dict_df = {

        'time': time,

        'pwrlt': mov_ave(pwrlt, n)[n:],
        'stl':   mov_ave(stl, n)[n:],
        'pwrm':  mov_ave(pwrmt, n)[n:],
        'stm':   mov_ave(stm, n)[n:],
        'pwri':  mov_ave(pwrit, n)[n:],
        'stti':  mov_ave(sti, n)[n:],
        'mac':   mac,

        }
    print(len(pwrlt)-n)
    print(len(sti)-n)

    m3m4 = list((np.array(dfc['M4 LT liquid'].tolist()) + np.array(dfc['M3 MT liquid'].tolist())))

    m3m4 = mov_ave(m3m4, n)[n:]
    print(len(m3m4))

    for i in range(len(lcd)):
        cd[i] = mov_ave(dfc[lcd[i]].tolist(), n)[n:]
        dict_df.update({lcd[i]: cd[i]})

        if iiii == 35 and lcd[i] == 'M4 LT liquid':
            df_lt_35 = pd.read_csv('Data/Data_Week_only[35]', sep=',', na_filter=True, skip_blank_lines=True, low_memory=False)
            dict_df.update({lcd[i]: df_lt_35['m4'].tolist()})
            m3m4 = list((np.array(df_lt_35['m4'].tolist()) + np.array(mov_ave(dfc['M3 MT liquid'].tolist(), n)[n:])))

    print(len(cd[4]))
    dict_df.update({'m3m4': m3m4})

    df_mmt = pd.read_csv('Data_Calc/Data_Week_' + str(iiii), sep=',', na_filter=True, skip_blank_lines=True, low_memory=False)
    dict_df.update({'mmt': df_mmt['mmt'].tolist()})

    df_mit = pd.read_csv('Data_Calc/Data_mit_Week_' + str(iiii), sep=',', na_filter=True, skip_blank_lines=True,low_memory=False)
    dict_df.update({'mit': df_mit['mit'].tolist()})

    print(len(df_mmt['mmt'].tolist()))
    print(len(df_mit['mit'].tolist()))
    """____________________________________________________________"""
    """______________       DataFrame format          _____________"""
    """____________________________________________________________"""
    data = pd.DataFrame(dict_df)

    # data = data.assign(y=y)

    """____________________________________________________________"""
    """______________             To CSV              _____________"""
    """____________________________________________________________"""

    data.to_csv("Data_Week_" + str(week))
