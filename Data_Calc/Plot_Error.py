
import pandas as pd                 # Dataframe library
import numpy as np                  # Scientific computing with nD object support
from functions import mov_ave, plt, sct_fit, fit,plot_1 ,plot_2
import random as rd


"""________________________________________________________________________________"""
""" Load data as CSV """


W28_ACLP1_HP1_ALC1 = ["Data_mlt_Week28"], ["Data_mmtWeek_28"], ["Data_mit_Week_28"], ['Data_MT_Week_28']
W29_ACLP1_HP0_ALC1 = ["Data_mlt_Week29"], ["Data_mmtWeek_29"], ["Data_mit_Week_29"], ['Data_MT_Week_29']
W30_ACLP1_HP0_ALC0 = ["Data_mlt_Week30"], ["Data_mmtWeek_30"], ["Data_mit_Week_30"], ['Data_MT_Week_30']
W31_ACLP1_HP1_ALC0 = ["Data_mlt_Week31"], ["Data_mmtWeek_31"], ["Data_mit_Week_31"], ['Data_MT_Week_31']
W32_ACDX1_HP0_ALC1 = ["Data_mlt_Week32"], ["Data_mmtWeek_32"], ["Data_mit_Week_32"], ['Data_MT_Week_32']
W33_ACDX1_HP0_ALC0 = ["Data_mlt_Week33"], ["Data_mmtWeek_33"], ["Data_mit_Week_33"], ['Data_MT_Week_33']
W34_ACDX1_HP1_ALC0 = ["Data_mlt_Week34"], ["Data_mmtWeek_34"], ["Data_mit_Week_34"], ['Data_MT_Week_34']
W35_ACDX1_HP1_ALC1 = ["Data_mlt_Week35"], ["Data_mmtWeek_35"], ["Data_mit_Week_35"], ['Data_MT_Week_35']


PDM = [
        # W28_ACLP1_HP1_ALC1,
        # W29_ACLP1_HP0_ALC1,
        # W30_ACLP1_HP0_ALC0,
        # W31_ACLP1_HP1_ALC0,
        # W32_ACDX1_HP0_ALC1,
        W33_ACDX1_HP0_ALC0,
        # W34_ACDX1_HP1_ALC0,
        # W35_ACDX1_HP1_ALC1
    ]

label = [0]*3
for i in PDM:
    # print(i[0][0])
    dfl = pd.read_csv(i[0][0], na_filter=True, skip_blank_lines=True, low_memory=False)
    dfm = pd.read_csv(i[1][0], na_filter=True, skip_blank_lines=True, low_memory=False)
    dfi = pd.read_csv(i[2][0], na_filter=True, skip_blank_lines=True, low_memory=False)
    dfo = pd.read_csv(i[3][0], na_filter=True, skip_blank_lines=True, low_memory=False)
    dic_df = {

        'time': dfl['time'],
        'mltc': dfl['m4'],
        'mmtc': dfm['mmt'],
        'mitc': dfi['mit'],
    }

    for col in dfo.columns:
        dic_df.update({col: dfo[col]})
    dat_ml = pd.DataFrame(dic_df)
    dat_ml.drop('Unnamed: 0', axis=1, inplace=True)
    dat_ml.drop('y', axis=1, inplace=True)
    dat_ml.drop('mdot_old', axis=1, inplace=True)
    dat_ml.drop('mdot_old_10', axis=1, inplace=True)


    mmt_measure = np.array(dfo['M4 LT liquid'])+np.array(dfo['M3 MT liquid'])
    """     Visible colors   """
    if i == 0:
        col = (1, 0, 0)
    if i == 1:
        col = (0, 0.9, 1)
    if i == 2:
        col = (0.6, 0.2, 0.8)
    if i == 3:
        col = (1, 0, 1)

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

    """___________________________________________________________________________________________________________
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  PERFORMANCE PLOTS  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ___________________________________________________________________________________________________________"""
    """________________________________________________________________________________"""



    mmt_measure = np.array(dfo['M3 MT liquid']) + np.array(dfo['M4 LT liquid'])
    mmt_measure = np.array(dfo['M4 LT liquid'])
    """______________________________________ X _________________________________________"""




    v1, label[1] = dfm['mmt'], "Mass flow estimation Data-Driven method  [kg/s]"
    v1, label[1] = dfl['m4'], "Mass flow estimation Data-Driven method  [kg/s]"

    """______________________________________ Y _________________________________________"""
    v2, label[2] = mmt_measure,  "Mass flow estimation direct measurement  [kg/s]"

    """_________________________________ var1, var2 ______________________________________"""
    time = dfo['time'].tolist()
    var1 = v1.tolist()
    var2 = v2.tolist()


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

    """___________________________________________________________________________________________________________
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  PERFORMANCE PLOTS  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ___________________________________________________________________________________________________________"""
    """________________________________________________________________________________"""


    x10u = np.array(var1)*1.15
    x10l = np.array(var1)*0.85



    plt.xlabel( "Mass flow estimation direct measurement  [kg/s]")
    plt.ylabel( "Mass flow estimation Data-Driven method  [kg/s]")
    plt.plot(var1, x10u, 'b,')
    plt.plot(var1, x10l, 'b,')
    plt.plot(var1, var1, 'r,')
    plt.scatter(var1, var2, marker='.', color='c', s=1)
    plt.legend(["+10%","-10%","Center line","Scatter data"])
plt.show()

#