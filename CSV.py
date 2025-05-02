
import pandas as pd                 # Dataframe library
import numpy as np                  # Scientific computing with nD object support
from functions import mov_ave, plt
from TDN import TDN, PSI, TDNex
import seaborn as sns

"""________________________________________________________________________________"""
PDM = [
    "W01_LP0_HP0_LE0",
    "W02_LP0_HP0_LE0",
    "W03_LP0_HP0_LE0",
    "W04_LP0_HP0_LE0",
    "W05_LP0_HP0_LE0",
    "W06_LP0_HP0_LE0",
    "W07_LP0_HP0_LE0",
    "W08_LP1_HP1_LE1",
    "W09_LP1_HP1_LE1",
    "W10_LP1_HP1_LE1",
    "W11_LP1_HP1_LE1",
    "W12_LP1_HP1_LE1",
    "W13_LP1_HP1_LE1",
    "W14_LP1_HP1_LE1",
    "W15_LP1_HP1_LE1",
    "W16_LP1_HP1_LE1",
    "W17_LP1_HP1_LE1",
    "W18_LP1_HP1_LE1",
    "W19_LP1_HP1_LE1",
    "W20_LP1_HP1_LE1",
    "W21_LP1_HP1_LE1",
    "W22_LP1_HP1_LE1",
    "W23_LP1_HP1_LE1",
    "W24_LP1_HP1_LE1",
    "W25_LP1_HP1_LE1",
    "W26_LP1_HP1_LE1",
    "W27_LP1_HP1_LE1",
    "W28_LP1_HP1_LE1",
    "W29_LP1_HP0_LE1",
    "W30_LP1_HP0_LE0",
    "W31_LP1_HP1_LE0",
    "W32_LP0_HP0_LE1",
    "W33_LP0_HP0_LE0",
    "W34_LP0_HP1_LE0",
    "W35_LP0_HP1_LE1",
]

"""________________________________________________________________________________"""

"""Label list set up"""
label = [0]*100
step_c = 1
# nrow = 3000
n = 0    # Moving averaging sample size
dtmin = 2   # Condernsor dt min



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

"""________________________________________________________________________________"""


def logic(index):

    if index % step_c == 0:
        return False
    return True


"""----------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------- """
"""Steps for reading data, takes one data out of #Step """

wn = []
pdml = len(PDM) + 1
leg = PDM[:pdml] * 2
leg = sorted(leg, key=lambda x: (x.isdigit(), x))

for pdm in range(len(PDM)):
    """ To append data frames together """
    if pdm < 17:

        def logic(index):
            if index % step_c == 0:
                return False
            return True

        try:
            df = pd.read_csv('Data/' + PDM[pdm], skiprows=lambda x: logic(x), na_filter=True, skip_blank_lines=True, low_memory=False)
            print(PDM[pdm])

        except:
            print(pdm)

    if pdm > 17:

        def logic(index):

            if index % step_c == 0:
                return False
            return True


        try:
            df = pd.read_csv('Data/' + PDM[pdm], skiprows=lambda x: logic(x), na_filter=True, skip_blank_lines=True, low_memory=False)
            # df = df.append(dfc)
            print(PDM[pdm])
        except:
            print(pdm)

    """ DataFrame read from CSV file, na_filter=False, skip_blank_lines=False """
    # df = pd.read_csv(weekdata, sep=',', na_filter=True, skip_blank_lines=True, low_memory=False)

    """________________________________________________________________________________"""
    """ Labels ::: """

    """__________ X ___________ """

    label[1] = 'T3 GC Outlet'
    label[7] = 'Tair external air'
    # label[1] = 'Tair external air'

    """ Mdot of LT MT and AC evap  """
    label[20] = 'M1 AHU liquid (cooling)'
    label[21] = 'M3 MT liquid'
    label[22] = 'M4 LT liquid'
    label[23] = 'M5 AHU (no ejectors)'

    label[25] = 'P1 discharge'
    var25 = mov_ave(df[label[25]].tolist(), n)[n:]
    """__________ Y ___________ """

    label[2] = 'Power Meter LT'
    label[3] = 'Power Meter MT'
    label[4] = 'Power Meter AUX'

    """Power meter """
    # label[5] = 'Power Meter MT'
    # label[5] = 'Power Meter AUX'
    label[5] = 'Total Power'
    """Pressure """
    # label[6] = 'P6 MT suction'
    label[6] = 'P2 receiver'
    label[8] = 'P6 MT suction'
    label[9] = 'P7 ejector inlet'

    """ Cycles of comp """

    label[10] = 'Number of Cycles MT1'
    label[11] = 'Number of Cycles MT2'
    label[12] = 'Number of Cycles MT3'
    label[13] = 'Number of Cycles AUX1'
    label[14] = 'Number of Cycles AUX2'
    label[15] = 'Number of Cycles AUX3'
    label[16] = 'Number of Cycles AUX4'
    label[17] = 'Number of Cycles LT1'
    label[18] = 'Number of Cycles LT2'
    label[19] = 'Number of Cycles LT3'

    """________________________________________________________________________________"""
    """Make Mov Ave"""

    """ X """
    var1 = mov_ave(list(np.array(df[label[1]].tolist()) - 273.15), n)[n:]
    var7 = mov_ave(list(np.array(df[label[7]].tolist()) - 273.15), n)[n:]

    """ Y  """
    var2 = mov_ave(df[label[2]].tolist(), n)[n:]
    var3 = mov_ave(df[label[3]].tolist(), n)[n:]
    var4 = mov_ave(df[label[4]].tolist(), n)[n:]
    var5 = mov_ave(df[label[5]].tolist(), n)[n:]
    var8 = mov_ave(list(np.array(df[label[6]].tolist()) - np.array(df[label[8]].tolist())), n)[n:]
    var9 = mov_ave(list(np.array(df[label[9]].tolist()) - np.array(df[label[6]].tolist())), n)[n:]
    label[8] = 'Pressure lift, MT suc to Rec '
    label[9] = 'Pressure drop, Ej inlet to Rec '

    var6 = mov_ave(list(np.array(df[label[6]].tolist())/1e5), n)[n:]

    # for i in range(len(var1)):
    #     if var1[i]>50 or -5>var1[i]:
    #         var1[i] =25
    weekname = [PDM[pdm]]*len(var1)

    """ Num of cycles LT IT MT  """
    var10 = mov_ave(list((np.array(df[label[10]].tolist())+np.array(df[label[11]].tolist())+np.array(df[label[12]].tolist()))/3), n)[n:]
    var11 = mov_ave(list((np.array(df[label[13]].tolist())+np.array(df[label[14]].tolist())+np.array(df[label[15]].tolist())+np.array(df[label[16]].tolist()))/4), n)[n:]
    var12 = mov_ave(list((np.array(df[label[17]].tolist())+np.array(df[label[18]].tolist())+np.array(df[label[19]].tolist()))/3), n)[n:]

    """ Mdot evap AC MT LT """
    if 8 <int(PDM[pdm][1:3]) < 32 or 35 < int(PDM[pdm][1:3]):
        var20 = mov_ave(list(np.array(df[label[20]].tolist())), n)[n:]
    else:
        var20 = mov_ave(list(np.array(df[label[23]].tolist())*10), n)[n:]

    var21 = mov_ave(df[label[21]].tolist(), n)[n:]

    if int(PDM[pdm][1:3]) == 35:
        dfm4 = pd.read_csv('Data/' + 'Data_35', usecols=['time', 'M4 LT liquid'], skiprows=lambda x: logic(x))
        var22 = dfm4[label[22]].tolist()
        # test = mov_ave(df[label[22]].tolist(), n)[n:]
        time = dfm4['time'].tolist()
        timeo = df['time'].tolist()

        for ii in range(len(var21)-len(var22)+n):
            var22.insert(0, df[label[22]].tolist()[ii])
            time.insert(0, df['time'].tolist()[ii])

        var22 = mov_ave(var22, n)[n:]
    else:
        var22 = mov_ave(df[label[22]].tolist(), n)[n:]

    """__________________________________ COP  Calc ___________________________________"""

    dhlt = []
    dhmt = []
    dhac = []
    trlt = []
    trmt = []
    trac = []
    tamb = list(np.array(df['T3 GC Outlet']) + dtmin)

    for j in range(df.shape[0]):
        dhlt.append(PSI('H', 'P', df['P4 LT suction'].tolist()[j], 'T', df['T23 LT section outlet'].tolist()[j], 'CO2')
                    - PSI('H', 'P', df['P2 receiver'].tolist()[j], 'Q', 0, 'CO2'))
        dhmt.append(PSI('H', 'P', df['P6 MT suction'].tolist()[j], 'T', df['T9 MT section outlet'].tolist()[j], 'CO2')
                    - PSI('H', 'P', df['P2 receiver'].tolist()[j], 'Q', 0, 'CO2'))

        if 8 < int(PDM[pdm][1:3]) < 32 or 35 < int(PDM[pdm][1:3]):
            dhac.append(PSI('H', 'P', df['P3 AHU evaporation'].tolist()[j], 'T', list((np.array(df['T19 Outlet AHU (cooling)']) + np.array(df['T20 Outlet AHU (cooling)']))/2)[j], 'CO2') - PSI('H', 'P', df['P2 receiver'].tolist()[j],'Q', 0, 'CO2'))

        else:
            dhac.append(PSI('H', 'P', df['P3 AHU evaporation'].tolist()[j], 'T', list((np.array(df['T19 Outlet AHU (cooling)']) + np.array(df['T20 Outlet AHU (cooling)']))/2)[j], 'CO2') - PSI('H', 'P', df['P7 ejector inlet'].tolist()[j], 'T', df['T3 GC Outlet'].tolist()[j], 'CO2'))
        trlt.append(1-(PSI('T', 'P', df['P4 LT suction'].tolist()[j], 'Q', 1, 'CO2')/tamb[j]))
        trmt.append(1-(PSI('T', 'P', df['P6 MT suction'].tolist()[j], 'Q', 1, 'CO2')/tamb[j]))
        trac.append(1-(PSI('T', 'P', df['P3 AHU evaporation'].tolist()[j], 'Q', 1, 'CO2')/tamb[j]))

    qlt = np.array(mov_ave(dhlt, n)[n:]) * np.array(var22)
    qmt = np.array(mov_ave(dhmt, n)[n:]) * np.array(var21)
    qac = np.array(mov_ave(dhac, n)[n:]) * np.array(var20)

    COP = list((qlt+qmt+qac)/np.array(mov_ave(df['Total Power'].tolist(), n)[n:]))

    """__________________________________ COP  IDEAL  ___________________________________"""
    """ ASS : ISENTROPIC EFFICIENCY = 1 """
    pwr_mt = []
    pwr_it = []

    for j in range(df.shape[0]):
        tdn_ms = TDN(df['P6 MT suction'].tolist()[j], 0, df['T14 MT suction'].tolist()[j], 0, 0, 'CO2')
        tdn_is = TDN(df['P2 receiver'].tolist()[j],   0, (df['T15 Aux_HP suction'].tolist()[j]+df['T16 Aux suction'].tolist()[j])/2, 0, 0, 'CO2')

        try:
            pwr_mt.append(TDN(df['P1 discharge'].tolist()[j], 0, 0, tdn_ms.s, 0, 'CO2').h-tdn_ms.h)
            pwr_it.append(TDN(df['P1 discharge'].tolist()[j], 0, 0, tdn_is.s, 0, 'CO2').h-tdn_is.h)

        except:
            print('sth went wrong : ', j)
            pwr_mt.append(pwr_mt[-1])
            pwr_it.append(pwr_it[-1])

    # ##################################################################################
    # #################################### MT Comp #####################################
    # ##################################################################################

    """Displacement & Eta"""

    eta_vol_mt = 0.9
    """________________________________________________________________________________"""

    """Energy balance"""
    h14 = df['h14 Enthalpy'].tolist()
    h1 = df['h1 Enthalpy'].tolist()
    pwrmt = df['Power Meter MT'].tolist()

    """Volumetric based on displacement"""
    t14 = df['T14 MT suction'].tolist()
    p14 = df['P6 MT suction'].tolist()
    p1 = df['P1 discharge'].tolist()

    sm1 = df['stato_mt1'].tolist()
    sm2 = df['stato_mt2'].tolist()
    sm3 = df['stato_mt3'].tolist()

    imt1 = df['inverter_mt_1'].tolist()

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
    mmt = list((np.array(df['M4 LT liquid'].tolist()) + np.array(df['M3 MT liquid'].tolist())))

    """Bitzer polynomial"""
    to = np.array(df['MT evaporation temp'].tolist())-273.15
    p_HP = np.array(df['P1 discharge'].tolist())/1e5

    for ii in range(len(p_HP)):
        c = dfbit['M4FTC30KTC'].tolist() if p_HP[ii] > 73.8 else dfbit['M4FTC30KSC'].tolist()

        mdot_4ftc = (c[0] + c[1] * to[ii] + c[2] * p_HP[ii] + c[3] * to[ii] ** 2 + c[4] * to[ii] * p_HP[ii] + c[5] * p_HP[ii] ** 2 + c[6] * to[ii] ** 3 + c[7] * p_HP[ii] * to[ii] ** 2 + c[8] * to[ii] * p_HP[ii] ** 2 + c[9] * p_HP[ii] ** 3)/3600

        c = dfbit['M4HTC20KTC'].tolist() if p_HP[ii] > 73.8 else dfbit['M4HTC20KSC'].tolist()
        mdot_4htc = (c[0] + c[1] * to[ii] + c[2] * p_HP[ii] + c[3] * to[ii] ** 2 + c[4] * to[ii] * p_HP[ii] + c[5] *
                     p_HP[ii] ** 2 + c[6] * to[ii] ** 3 + c[7] * p_HP[ii] * to[ii] ** 2 + c[8] * to[ii] * p_HP[
                         ii] ** 2 + c[9] * p_HP[ii] ** 3) / 3600

    mmt_bitzer = list((np.array(sm1) * (np.array(imt1) / 100 * 30 + 30) / 60 * mdot_4htc + np.array(
        sm2) * mdot_4ftc + np.array(sm3) * mdot_4ftc))

    # ##################################################################################
    # #################################### IT Comp #####################################
    # ##################################################################################
    """________________________________________________________________________________"""

    """Displacement & Eta"""
    eta_vol_it = 0.9
    """________________________________________________________________________________"""

    """Energy balance"""
    h15i = df['h15 Enthalpy'].tolist()  # Inlets
    h16i = df['h16 Enthalpy'].tolist()  # Inlets
    h15 = list((np.array(h15i) + np.array(h16i)) / 2)
    h1 = df['h1 Enthalpy'].tolist()  # Outlet
    pwrit = df['Power Meter AUX'].tolist()

    """Volumetric based on displacement"""
    t15 = df['T15 Aux_HP suction'].tolist()
    t16 = df['T16 Aux suction'].tolist()
    p15i = df['P5 Aux HP suction'].tolist()
    p16i = df['P2 receiver'].tolist()
    p1 = df['P1 discharge'].tolist()
    p15 = list((np.array(p16i) + np.array(p15i)) / 2)

    si1 = df['stato_aux1'].tolist()
    si2 = df['stato_aux2'].tolist()
    si3 = df['stato_aux3'].tolist()
    si4 = df['stato_aux4'].tolist()
    iit1 = df['inverter_aux_1'].tolist()
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
    to = np.array(df['T16 Aux suction'].tolist()) - 273.15
    p_HP = np.array(df['P1 discharge'].tolist()) / 1e5

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

    # ############################################################################################
    # ############################################################################################
    # ############################################################################################

    pwr_mt = np.array(mov_ave(pwr_mt, n)[n:])* np.array(mov_ave(mmt_bitzer, n)[n:])
    pwr_it = np.array(mov_ave(pwr_it, n)[n:])* np.array(mov_ave(mit_bitzer, n)[n:])

    COP_idl = list((qlt + qmt + qac) / ((np.array(mov_ave(df['Power Meter LT'].tolist(), n)[n:])) + pwr_it + pwr_mt))

    """__________________________________ 2nd Law Calc ___________________________________"""
    trlt = np.array(mov_ave(trlt, n)[n:])
    trmt = np.array(mov_ave(trmt, n)[n:])
    trac = np.array(mov_ave(trac, n)[n:])

    eta2nd = list((qlt*trlt+qmt*trmt+qac*trac)/np.array(mov_ave(df['Total Power'].tolist(), n)[n:]))
    """________________________________________________________________________________"""
    exergylt = []
    exergymt = []
    exergyac = []
    for j in range(df.shape[0]):
        exergylt.append(TDNex(df['P4 LT suction'].tolist()[j], 0, df['T23 LT section outlet'].tolist()[j], 0, 0, 'co2', tamb[j]).exergy()-
                        TDNex(df['P4 LT suction'].tolist()[j], PSI('H', 'P', df['P2 receiver'].tolist()[j], 'Q', 0, 'CO2'), 0, 0, 0, 'co2', tamb[j]).exergy())
        exergymt.append(TDNex(df['P6 MT suction'].tolist()[j], 0, df['T9 MT section outlet'].tolist()[j], 0, 0, 'co2',tamb[j]).exergy() -
                        TDNex(df['P6 MT suction'].tolist()[j], PSI('H', 'P', df['P2 receiver'].tolist()[j], 'Q', 0, 'CO2'), 0, 0, 0, 'co2', tamb[j]).exergy())


        if 8 < int(PDM[pdm][1:3]) < 32 or 35 < int(PDM[pdm][1:3]):
            exergyac.append(
                TDNex(df['P3 AHU evaporation'].tolist()[j], 0,  list((np.array(df['T19 Outlet AHU (cooling)']) + np.array(df['T20 Outlet AHU (cooling)'])) / 2)[j], 0, 0, 'co2',tamb[j]).exergy() -
                TDNex(df['P3 AHU evaporation'].tolist()[j], PSI('H', 'P', df['P2 receiver'].tolist()[j], 'Q', 0, 'CO2'), 0, 0,0, 'co2', tamb[j]).exergy()
            )

        else:
            exergyac.append(
                TDNex(df['P3 AHU evaporation'].tolist()[j], 0,  list((np.array(df['T19 Outlet AHU (cooling)']) + np.array(df['T20 Outlet AHU (cooling)'])) / 2)[j], 0, 0, 'co2',tamb[j]).exergy() -
                TDNex(df['P3 AHU evaporation'].tolist()[j], PSI('H', 'P', df['P7 ejector inlet'].tolist()[j], 'T',df['T3 GC Outlet'].tolist()[j], 'CO2'), 0, 0,0, 'co2', tamb[j]).exergy()
            )

    exlt = np.array(mov_ave(exergylt, n)[n:]) * np.array(var22)
    exmt = np.array(mov_ave(exergymt, n)[n:]) * np.array(var21)
    exac = np.array(mov_ave(exergyac, n)[n:]) * np.array(var20)

    eta2ndex = list(abs((exlt+exmt+exac)/np.array(mov_ave(df['Total Power'].tolist(), n)[n:])))


    """________________________________________________________________________________"""
    # var11, label[11] = var10.copy(), 'Number of Cycles MT'
    # var11, label[11] = var11.copy(), 'Number of Cycles IT'
    # var11, label[11] = var12.copy(), 'Number of Cycles LT'

    # var21, label[21] = var20.copy(), 'Mass flow rate in evaporators AC'
    # var21, label[21] = var21.copy(), 'Mass flow rate in evaporators MT'
    # var21, label[21] = var22.copy(), 'Mass flow rate in evaporators LT'
    var21, label[21] = list(np.array(var21) + np.array(var22) + np.array(var20)), 'Total Mass flow rate in evaporators '

    """___________________________________________________________________________________________________________
    ____________________________________________________PLOTS_____________________________________________________
    ___________________________________________________________________________________________________________"""
    """ 
    First plots the lines and then 'ro' spesifies red dots  __ r ::  for red and o :: for circle
        Color               Shape                  shape
        b : blue            "8"	: octagon          "," : pixel 
        g : green           "s"	: square           "o" : circle 
        r : red             "p"	: pentagon         "v" : triangle_down 
        c : cyan            "P"	: plus (filled)    "x" : x
        m : magenta         "*"	: star             "X" : x (filled)
        y : yellow          "h"	: hexagon1         "D" : diamond
        k : black           "H"	: hexagon2         "d" : thin_diamond  
        w : white           "+"	: plus                       
    """

    """________________________________________________________________________________"""
    # df.drop('Unnamed: 0', axis=1, inplace=True)
    for col in range(df.shape[1]):
        df[df.columns[col]] = mov_ave(df[df.columns[col]].tolist(), n)

    df=df[n:]
    df['2nd law efficiency (COP/COP Carnot)' ] = eta2nd
    df['2nd law efficiency Exergy based'     ] = eta2ndex
    df['Cooling load LT [W]'                 ] = qlt
    df['Cooling load MT [W]'                 ] = qmt
    df['Cooling load AC [W]'                 ] = qac
    df['COP[-]'                              ] = COP
    df['Ideal COP[-] compressor eta_isen = 1'] = COP_idl
    df['Pressure lift, MT suc to Rec'        ] = var8
    df['Pressure drop, Ej inlet to Rec'      ] = var9
    df['Average number of cycles MT'         ] = var10
    df['Average number of cycles IT'         ] = var11
    df['Average number of cycles LT'         ] = var12
    df['AC mass flow rate [kg/s]'            ] = var20
    df['MT mass flow rate [kg/s]'            ] = var21
    df['LT mass flow rate [kg/s]'            ] = var22

    print(df.columns)
    print(pdm)
    print(df['Ideal COP[-] compressor eta_isen = 1'])
    df.to_csv("Data_Mdot/" + str(PDM[pdm]))

