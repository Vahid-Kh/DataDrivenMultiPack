
"""

Dataframe CSV format creator for :

        1 - raw data +
         2 - estimated mass flow rates based on data-driven model +
          3 - ejector estimations using CoolSelector 2 DLL files

    ---------------------------------------------------------------------
"""

import numpy as np
import pandas as pd
from TDN import PSI
from functions import plot_2, plot_3, plot_4, plot_5, plot_6,plot_4_ej, plot_7_ej, mov_ave
import matplotlib.pyplot as plt

"""________________________________________________________________________________"""

"""----------CNR DATA-----------"""
W28_ACLP1_HP1_ALC1 = "Data_Mdot/Data_HPV_W_28"
W29_ACLP1_HP0_ALC1 = "Data_Mdot/Data_HPV_W_29"
W30_ACLP1_HP0_ALC0 = "Data_Mdot/Data_HPV_W_30"
W31_ACLP1_HP1_ALC0 = "Data_Mdot/Data_HPV_W_31"
W32_ACDX1_HP0_ALC1 = "Data_Mdot/Data_HPV_W_32"
W33_ACDX1_HP0_ALC0 = "Data_Mdot/Data_HPV_W_33"
W34_ACDX1_HP1_ALC0 = "Data_Mdot/Data_HPV_W_34"
W35_ACDX1_HP1_ALC1 = "Data_Mdot/Data_HPV_W_35"

"""________________________________________________________________________________"""
PDM = [W28_ACLP1_HP1_ALC1, W29_ACLP1_HP0_ALC1, W30_ACLP1_HP0_ALC0, W31_ACLP1_HP1_ALC0,
       W32_ACDX1_HP0_ALC1, W33_ACDX1_HP0_ALC0, W34_ACDX1_HP1_ALC0, W35_ACDX1_HP1_ALC1]
PDM_mmt = [W28_ACLP1_HP1_ALC1, W29_ACLP1_HP0_ALC1, W30_ACLP1_HP0_ALC0, W31_ACLP1_HP1_ALC0,
           W32_ACDX1_HP0_ALC1, W33_ACDX1_HP0_ALC0, W34_ACDX1_HP1_ALC0, W35_ACDX1_HP1_ALC1]

"""________________________________________________________________________________"""
"""
Weekly mode of ejectors ::::

W28 :    LP1   HP1   LE1
W29 :    LP1   HP0   LE1
W30 :    LP1   HP0   LE0
W31 :    LP1   HP1   LE0
W32 :    LP0   HP0   LE1
W33 :    LP0   HP0   LE0
W34 :    LP0   HP1   LE0
W35 :    LP0   HP1   LE1

"""

"""________________________________________________________________________________"""
"""________________________________________________________________________________"""

# for weeknum in [28, 29, 30, 31, 32, 33, 34, 35]:
# for weeknum in [ 34]:  # For HP ejector only
for weeknum in [30, 32, 34]:  # For one ejector only
# for weeknum in [33]:  # For HP ejector only
# for weeknum in [30,34]:  # For HP ejector only
    w = weeknum - 28
    print('For week ::::: ', weeknum)
    """--------------------------------"""
    """--------Data_Week_Calc_CNR------"""
    """--------------------------------"""
    filename = PDM[w]
    """ DataFrame read from CSV file, na_filter=False, skip_blank_lines=False """
    df = pd.read_csv(filename, sep=',', na_filter=True, skip_blank_lines=True, low_memory=False)
    df_mmt = pd.read_csv(filename, sep=',', na_filter=True, skip_blank_lines=True, low_memory=False)

    """
    Ejector Rom Model Usage:
    Units: P [Pa]. T [K]. Sh [K]. H [J/kg]. m [kg/s]. EntrainmentRatio = SuctionM/MotiveM [-]
    
    These values are added so that e.g. ErrCode = 101 means outside suction and lift envelope (but inside motive envelope)
    """

    """Motive nozzle P , T and H values"""
    mot_p = df['P7 ejector inlet'].tolist()

    """Suction flow P , T and H values"""
    suc_p = df['P6 MT suction'].tolist()
    suc_p_lp = df['P3 AHU evaporation'].tolist()
    mot_t = df['T5 Inlet IHX 2'].tolist()
    suc_t_lp = df['T7 Ejector inlet'].tolist()

    """ Suction superheat """
    suc_sh_hp = list(np.array(df['T14 MT suction'].tolist())-np.array([PSI('T', 'P', x, 'Q', 1, 'CO2') for x in suc_p]))
    suc_sh_le=[]
    for x in range(len(suc_p)):
        suc_sh_le.append(df['T14 MT suction'].tolist()[x]-PSI('T', 'P', suc_p[x], 'Q', 0, 'CO2'))

    suc_sh_lp = list(np.array(df['T7 Ejector inlet'].tolist()) - np.array([PSI('T', 'P', x, 'Q', 1, 'CO2') for x in suc_p_lp]))

    """Outlet Pressure values"""
    out_p = df['P2 receiver'].tolist()

    """________________________________________________________________________________"""
    """________________________________________________________________________________"""

    """ Weekly mode for each ejector running mode  :  """
    hp_st = [1, 0, 0, 1, 0, 0, 1, 1]   # State of ejector
    lp_st = [1, 1, 1, 1, 0, 0, 0, 0]   # State of ejector
    le_st = [1, 1, 0, 0, 1, 0, 0, 1]   # State of ejector

    """   Inputs for DLL function   """

    """ HP """
    mmhp  = df['mmhp'].tolist()         # Motive mass flow in [kg/s]
    smhp  = df['smhp'].tolist()         # Suction mass flow in [kg/s]
    rmshp = df['rmshp'].tolist()        # Motive to suction mass flow ratio

    """ LP """
    mmlp  = df['mmlp'].tolist()          # Motive mass flow in [kg/s]
    smlp  = df['smlp'].tolist()          # Suction mass flow in [kg/s]
    rmslp = df['rmslp'].tolist()         # Motive to suction mass flow ratio

    """ LE """
    mmle  = df['mmle'].tolist()         # Motive mass flow in [kg/s]
    smle  = df['smle'].tolist()         # Suction mass flow in [kg/s]
    rmsle = df['rmsle'].tolist()        # Motive to suction mass flow ratio

    """________________________________________________________________________________"""
    """___________________________________  Plot  _____________________________________"""
    """________________________________________________________________________________"""
    mode = [
            '_ LP:1 _ HP:1 _ LE:1 ',    # W28
            '_ LP:1 _ HP:0 _ LE:1 ',    # W29
            '_ LP:1 _ HP:0 _ LE:0 ',    # W30    LP only
            '_ LP:1 _ HP:1 _ LE:0 ',    # W31
            '_ LP:0 _ HP:0 _ LE:1 ',    # W32    LE only
            '_ LP:0 _ HP:0 _ LE:0 ',    # W33
            '_ LP:0 _ HP:1 _ LE:0 ',    # W34    HP only
            '_ LP:0 _ HP:1 _ LE:1 '     # W35
            ]
    """________________________________________________________________________________"""
    time = df['time'].tolist()
    """________________________________________________________________________________"""

    #  ____________________________________
    #  !!!!!!!!!!!!!! LP  !!!!!!!!!!!!!!!!!
    #  ____________________________________

    if weeknum == 30:

        suc_m_lp = np.array(df['mac'].tolist())

        mot_m_lp = (np.array(df['mmt'].tolist())+np.array(df['mit'].tolist()))-np.array(df['mhv'].tolist())*0.8

        smr = list(suc_m_lp/mot_m_lp)

        suc_mot_rat = []
        for j in range(len(smr)):
            if smr[j] > 1:
                suc_mot_rat.append(1/smr[j])
                # suc_mot_rat.append(rmslp[j])
            elif smr[j] < 0:
                suc_mot_rat.append(0)
            else:
                suc_mot_rat.append(smr[j])


        suc_mot_rat = mov_ave(suc_mot_rat, 60)

        p_drop = list((np.array(mot_p)-np.array(out_p))/1e5)
        p_lift = list((np.array(out_p)-np.array(suc_p_lp))/1e5)
        sub_cool = list((np.array(df['T3 GC Outlet'].tolist())-np.array(mot_t)))
        # index_lp = []
        # for ii in range(len(mot_p)):
        #     if out_p[ii] > 10 and np.log((out_p[ii]) / (suc_p_lp[ii])) > 1e-6:
        #         index_lp.append((np.log((mot_p[ii]) / (out_p[ii])) / np.log((out_p[ii]) / (suc_p_lp[ii]))))
        #
        #     else:
        #         index_lp.append(0)

        suc_sh_lp = [x for x in suc_sh_lp]
        plot_2(time, suc_mot_rat, rmslp, ['time', 'Entrainment ratio(S/M) data driven model', 'Entrainment ratio(S/M) Lab+RoM model'], str(weeknum) + mode[w])
        plot_4_ej(time, suc_mot_rat, p_drop, p_lift, suc_sh_lp, ['time', 'Entrainment ratio(S/M) data driven model', 'Entrainment ratio(S/M) Lab+RoM model', ' Pressure lift[Bar]', 'Superheat of suction [K]'], str(weeknum) + mode[w])
        plot_7_ej(time, suc_mot_rat, rmslp, mot_m_lp, p_drop, p_lift, suc_sh_lp, sub_cool, ['time', 'Entrainment (S/M) ratio data driven', 'Entrainment (S/M) ratio CoolSelector', 'Motive mass flow rate data driven [Kg/s] ', 'Pressure drop[Bar]',' Pressure lift[Bar]','Superheat of suction [K]','Subcooling of Motive flow[K]'], str(weeknum)+ mode[w])

    #  ____________________________________
    #  !!!!!!!!!!!!!! LE  !!!!!!!!!!!!!!!!!
    #  ____________________________________

    elif weeknum == 32:

        suc_m_le = np.array(df['M3 MT liquid'].tolist()) + np.array(df['M4 LT liquid'].tolist()) - np.array(df['mmt'].tolist())
        mot_m_le = np.array(df['mmt'].tolist()) + np.array(df['mit'].tolist()) - np.array(df['mac'].tolist())
        suc_mot_ratio = list(suc_m_le / mot_m_le)

        p_drop = list((np.array(mot_p) - np.array(out_p)) / 1e5)
        p_lift = list((np.array(out_p) - np.array(suc_p)) / 1e5)
        sub_cool = list((np.array(df['T3 GC Outlet'].tolist()) - np.array(mot_t)))

        suc_sh_le = [x for x in suc_sh_le]

        suc_mot_rat = []
        for j in suc_mot_ratio:
            if j > 1:
                suc_mot_rat.append(1/j)
            else:
                suc_mot_rat.append(j)

        index_le = list(np.log(np.array(mot_p) / np.array(out_p)) / np.log(np.array(out_p) / np.array(suc_p)))

        plot_2(time, suc_mot_rat, rmsle, ['time', 'Entrainment (S/M) ratio data driven', 'Entrainment (S/M) ratio CoolSelector'], str(weeknum) + mode[w])
        # plot_3(time, suc_mot_rat, rmsle, index_le, ['time', 'Entrainment (S/M) ratio data driven', 'Entrainment (S/M) ratio CoolSelector', '2.5 index calculated'], str(weeknum) + mode[w])
        # plot_3(time, rmsle, p_drop, p_lift,['time', 'Entrainment (S/M) ratio CoolSelector', 'Pressure drop[Bar]', ' Pressure lift[Bar]','Superheat of suction [K]'], str(weeknum) + mode[w])
        ll = [1e20]

        ll.extend(time)

        ll.pop()
        plot_4_ej(time, rmsle, p_drop, p_lift, ll, ['time', 'Entrainment (S/M) ratio CoolSelector', 'Pressure drop[Bar]', ' Pressure lift[Bar]', 'Superheat of suction [K]'], str(weeknum) + mode[w])
        plot_7_ej(time, suc_mot_rat, rmsle, mot_m_le, p_drop, p_lift, suc_sh_le, sub_cool, ['time', 'Entrainment (S/M) ratio data driven', 'Entrainment (S/M) ratio CoolSelector', 'Motive mass flow rate data driven [Kg/s] ', 'Pressure drop[Bar]', ' Pressure lift[Bar]', 'Superheat of suction [K]', 'Subcooling of Motive flow[K]'], str(weeknum) + mode[w])

    #  ____________________________________
    #  !!!!!!!!!!!!!! HP  !!!!!!!!!!!!!!!!!
    #  ____________________________________

    elif weeknum == 34:

        suc_m_hp = np.array(df['M3 MT liquid'].tolist()) + np.array(df['M4 LT liquid'].tolist()) - np.array(
            df['mmt'].tolist())
        mot_m_hp = np.array(df['mmt'].tolist()) + np.array(df['mit'].tolist()) - np.array(df['mac'].tolist())-np.array(df['mhv'].tolist())*0.8
        mac = df['mac'].tolist()
        suc_mot_ratio = list(suc_m_hp / mot_m_hp)

        suc_mot_rat = []
        for j in suc_mot_ratio:
            if j > 1:
                suc_mot_rat.append(1/j)
            else:
                suc_mot_rat.append(j)

        index_hp = list(np.log(np.array(mot_p) / np.array(out_p)) / np.log(np.array(out_p) / np.array(suc_p)))

        p_drop = list((np.array(mot_p) - np.array(out_p)) / 1e5)
        p_lift = list((np.array(out_p) - np.array(suc_p)) / 1e5)
        sub_cool = list((np.array(df['T3 GC Outlet'].tolist()) - np.array(mot_t)))

        suc_sh_hp = [x for x in suc_sh_hp]
        suc_mot_rat = mov_ave(suc_mot_rat,10)

        plot_2(time, suc_mot_rat, rmshp, ['time', 'Entrainment (S/M) ratio data driven', 'Entrainment (S/M) ratio CoolSelector'], str(weeknum) + mode[w])
        plot_3(time, suc_mot_rat, rmshp, index_hp, ['time', 'Entrainment (S/M) ratio data driven', 'Entrainment (S/M) ratio CoolSelector', '2.5 index calculated'], str(weeknum) + mode[w])
        plot_4_ej(time, rmshp, p_drop, p_lift, suc_sh_hp, ['time', 'Entrainment (S/M) ratio CoolSelector', 'Pressure drop[Bar]', ' Pressure lift[Bar]', 'Superheat of suction [K]'], str(weeknum) + mode[w])

        # plot_4_ej(time, rmshp, p_drop, p_lift, suc_sh_hp, ['time', 'Entrainment (S/M) ratio CoolSelector', 'Pressure drop[Bar]', ' Pressure lift[Bar]', 'Superheat of suction [K]'], str(weeknum) + mode[w])
        # plot_7_ej(time, suc_mot_rat, rmshp, mot_m_hp, p_drop, p_lift, suc_sh_hp, sub_cool, ['time', 'Entrainment (S/M) ratio data driven', 'Entrainment (S/M) ratio CoolSelector', 'Motive mass flow rate data driven [Kg/s] ', 'Pressure drop[Bar]', ' Pressure lift[Bar]', 'Superheat of suction [K]', 'Subcooling of Motive flow[K]'], str(weeknum) + mode[w])
        plot_7_ej(time, suc_mot_rat, rmshp, mot_m_hp, suc_p, out_p, suc_sh_hp, mot_p,
                  ['time', 'Entrainment (S/M) ratio data driven', 'Entrainment (S/M) ratio CoolSelector',
                   'Motive mass flow rate data driven [Kg/s] ', 'Pressure drop[Bar]', ' Pressure lift[Bar]',
                   'Superheat of suction [K]', 'Subcooling of Motive flow[K]'], str(weeknum) + mode[w])

        """________________________________________________________________________________"""

    elif weeknum == 33:

        mhpv = list(np.array(df['mhv'].tolist())*0.85)
        mhp_in = list(np.array(df['mmt'].tolist()) + np.array(df['mit'].tolist()) - np.array(df['mac'].tolist()))

        plot_2(time, mhpv, mhp_in, ['time', 'Mdot HPv ICMTS 20B CoolSelector', 'Mdot estimation using Data-Driven model'], str(weeknum) + mode[w])

"""________________________________________________________________________________"""

plt.show()
