
"""

Dataframe CSV format creator for :

        1 - raw data +
         2 - estimated mass flow rates based on data-driven model +
          3 - ejector estimations using CoolSelector 2 DLL files
"""

""" Libraries import """

import numpy as np
import pandas as pd

from TDN import PSI
from functions import plot_3,plot_4,plot_5
import matplotlib.pyplot as plt
from EjctrEstmtr import mEjecBlock

"""----------CNR DATA-----------"""
W28_ACLP1_HP1_ALC1 = "MdotEjCalc/Data_Week_28"
W29_ACLP1_HP0_ALC1 = "MdotEjCalc/Data_Week_29"
W30_ACLP1_HP0_ALC0 = "MdotEjCalc/Data_Week_30"
W31_ACLP1_HP1_ALC0 = "MdotEjCalc/Data_Week_31"
W32_ACDX1_HP0_ALC1 = "MdotEjCalc/Data_Week_32"
W33_ACDX1_HP0_ALC0 = "MdotEjCalc/Data_Week_33"
W34_ACDX1_HP1_ALC0 = "MdotEjCalc/Data_Week_34"
W35_ACDX1_HP1_ALC1 = "MdotEjCalc/Data_Week_35"


PDM = [W28_ACLP1_HP1_ALC1, W29_ACLP1_HP0_ALC1, W30_ACLP1_HP0_ALC0, W31_ACLP1_HP1_ALC0,
       W32_ACDX1_HP0_ALC1, W33_ACDX1_HP0_ALC0, W34_ACDX1_HP1_ALC0, W35_ACDX1_HP1_ALC1]

"""________________________________________________________________________________"""
"""________________________________________________________________________________"""

for weeknum in [30,32,34]:
#
# for weeknum in [32]:
    w = weeknum - 28
    print('For week ::::: ', weeknum)
    """--------------------------------"""
    """--------Data_Week_Calc_CNR------"""
    """--------------------------------"""
    filename = PDM[w]
    """ DataFrame read from CSV file, na_filter=False, skip_blank_lines=False """
    df = pd.read_csv(filename, sep=',', na_filter=True, skip_blank_lines=True, low_memory=False)

    """
    Ejector Rom Model Usage:
    Units: P [Pa]. T [K]. Sh [K]. H [J/kg]. m [kg/s]. EntrainmentRatio = SuctionM/MotiveM [-]
    Inputs:
    Possible ejector names:
    EjectorName = 'Multi Ejector HP 1875'  4 cartridge
    EjectorName = 'Multi Ejector HP 3875'  6 cartridge
    EjectorName = 'Multi Ejector LP 935'   4 cartridge
    EjectorName = 'Multi Ejector LP 1935'  6 cartridge
    EjectorName = 'CTM 1 LE 200' 
    EjectorName = 'CTM 1 LE 400'Data_Ejector.py
    EjectorName = 'CTM 2 LE 600' 
    
    MotiveP, MotiveT,MotiveH: Motive pressure, temperature and enthalpy respectively
    SuctionP,SuctionSh,SuctionH: Suction pressure, superheat and enthalpy respectively
    OutletP: Outlet pressure
    
    Possible values of ErrCode:
    0  : No errors
    -1  : Coolselector2 installation not found
    -2  : Requested ejector not found
    If ErrCode is larger than 0 then operation is outside ejector envelope:
    A value of 1 indicates outside suction envelope
    A value of 10 indicates outside motive envelope
    A value of 100 indicates outside pressure lift envelope
    These values are added so that e.g. ErrCode = 101 means outside suction and lift envelope (but inside motive envelope)
    """

    ej_type = [
                'Multi Ejector HP 3875',       # HP
                'Multi Ejector LP 1935',       # LP
                'CTM 2 LE 600'                 # LE

                ]

    """Motive nozzle P , T and H values"""
    mot_p = df['P7 ejector inlet'].tolist()
    mot_t = df['T5 Inlet IHX 2'].tolist()
    mot_h = df['h5 Enthalpy'].tolist()

    """Suction flow P , T and H values"""
    suc_p = df['P6 MT suction'].tolist()
    suc_p_lp = df['P3 AHU evaporation'].tolist()

    suc_t_lp = df['T7 Ejector inlet'].tolist()

    suc_h_hp = [PSI('H', 'P', x, 'Q', 1, 'CO2') for x in suc_p]
    suc_h_le = [PSI('H', 'P', x, 'Q', 0, 'CO2') for x in suc_p]
    suc_h_lp = [PSI('H', 'P', suc_p_lp[i], 'T', suc_t_lp[i], 'CO2') for i in range(len(suc_p_lp))]

    suc_sh_hp = list(np.array(df['T14 MT suction'].tolist())-np.array([PSI('T', 'P', x, 'Q', 1, 'CO2') for x in suc_p]))
    suc_sh_le = [PSI('T', 'P', x, 'Q', 0, 'CO2') for x in suc_p]
    suc_sh_lp = list(np.array(df['T7 Ejector inlet'].tolist()) - np.array([PSI('T', 'P', x, 'Q', 1, 'CO2') for x in suc_p_lp]))

    """Outlet Pressure values"""
    out_p = df['P2 receiver'].tolist()

    """________________________________________________________________________________"""
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

    """ Weekly mode for each ejector running mode  :  """
    hp_st = [1, 0, 0, 1, 0, 0, 1, 1]   # State of ejector
    lp_st = [1, 1, 1, 1, 0, 0, 0, 0]   # State of ejector
    le_st = [1, 1, 0, 0, 1, 0, 0, 1]   # State of ejector

    """   Inputs for DLL function   """
    """@@@@@@@@@@@@@@@@@@@@@      Check value selected for SH      """


    """ HP """
    mmhp  = []         # Motive mass flow in [kg/s]
    smhp  = []         # Suction mass flow in [kg/s]
    rmshp = []        # Motive to suction mass flow ratio

    """ LP """
    mmlp  = []         # Motive mass flow in [kg/s]
    smlp  = []         # Suction mass flow in [kg/s]
    rmslp = []        # Motive to suction mass flow ratio

    """ LE """
    mmle  = []         # Motive mass flow in [kg/s]
    smle  = []         # Suction mass flow in [kg/s]
    rmsle = []        # Motive to suction mass flow ratio

    def PaToBar(lst):
        return list(np.array(lst)/1e5)

    def WToKw(lst):
        return list(np.array(lst)/1e3)

    def KToC(lst):
        return list(np.array(lst)-273.15)

    """HP ejector calculation from dll """
    if hp_st[w] == 1:
        """
        ['P_MN', 'T_MN', 'P_SN ', 'T_SN', 'P_OUT']
        """
        dict = {
            'mot_p': PaToBar(mot_p),
            'mot_t': KToC(mot_t),
            'suc_p': PaToBar(suc_p),
            'suc_t_lp': KToC(suc_t_lp),
            'out_p': PaToBar(out_p),
        }

        dfe = pd.DataFrame(dict)
        rmshp = mEjecBlock(dfe, 'Multi Ejector HP 3875', True)
        rmshp = [0 if i < 0 else i for i in rmshp]


    elif hp_st[w] == 0:
        rmshp = [0]*len(mot_p)

    """LP ejector calculation from dll """
    if lp_st[w] == 1:
        q_lp = []
        for iii in range(len(suc_p)):
            q_lp.append(PSI('Q', 'P', suc_p[iii], 'T', suc_t_lp[iii], 'CO2'))
        dict = {
            'mot_p': PaToBar(mot_p),
            'mot_t': KToC(mot_t),
            # 'mot_h': WToKw(mot_h),
            'suc_p': PaToBar(suc_p),
            'suc_t_lp': KToC(suc_t_lp),
            # 'q': q_lp,
            # 'suc_h_lp': WToKw(suc_h_lp),

            'out_p': PaToBar(out_p),
        }

        dfe = pd.DataFrame(dict)

        rmslp = mEjecBlock(dfe, 'Multi Ejector LP 1935', True)
        rmslp = [0 if i < 0 else i for i in rmslp]

        dict = {
            'mot_p': PaToBar(mot_p),
            'mot_t': KToC(mot_t),
            'suc_p': PaToBar(suc_p),
            'suc_t_lp': KToC(suc_t_lp),
            'out_p': PaToBar(out_p),
            'rmslp': rmslp
        }

        dfe = pd.DataFrame(dict)
        with pd.option_context('display.max_rows', 10, 'display.max_columns', None):  # more options can be specified also
            print(dfe)

    elif lp_st[w] == 0:
        rmslp = [0] * len(mot_p)

    """Liq ejector calculation from dll """
    if le_st[w] == 1:

        dict = {
            'mot_p': PaToBar(mot_p),
            'mot_t': KToC(mot_t),
            'suc_p': PaToBar(suc_p),
            'suc_t_lp': KToC(suc_t_lp),
            'out_p': PaToBar(out_p),
        }


        dfe = pd.DataFrame(dict)
        with pd.option_context('display.max_rows', 10, 'display.max_columns', None):  # more options can be specified also
            print(dfe)
        rmsle = mEjecBlock(dfe, 'CTM 2 LE 600', True)
        rmsle = [0 if i < 0 else i for i in rmsle]


    elif le_st[w] == 0:

        rmsle = [0]*len(mot_p)

    p_drop = list((np.array(mot_p) - np.array(out_p)) / 1e5)
    p_lift = list((np.array(out_p) - np.array(suc_p)) / 1e5)
    """ 
    Accounting for number of ejectors in the system :
    
                2 # of HP
                2 # of LP
                1 # of LE
    """

    """__________________DF Update with Ej data______________________________"""
    """__________________DF Update with Ej data______________________________"""

    df = df.assign(rmshp=rmshp)
    df = df.assign(rmslp=rmslp)
    df = df.assign(rmsle=rmsle)

    """_______________________________ DF To CSV ____________________________"""
    """_______________________________ DF To CSV ____________________________"""

    df.to_csv("Data_" + str(weeknum))

plt.show()