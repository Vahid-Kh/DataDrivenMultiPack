
import pandas as pd                 # Dataframe library
import numpy as np                  # Scientific computing with nD object support
from functions import mov_ave, plt, sct_fit, fit,plot_1 ,plot_2, sctFitAve
import random as rd


"""________________________________________________________________________________"""
PDM = [
    # "W01_LP0_HP0_LE0",
    # "W02_LP0_HP0_LE0",
    # "W03_LP0_HP0_LE0",
    # "W04_LP0_HP0_LE0",
    # "W05_LP0_HP0_LE0",
    # "W06_LP0_HP0_LE0",
    # "W07_LP0_HP0_LE0",
    # "W08_LP1_HP1_LE1",
    # "W09_LP1_HP1_LE1",
    # "W10_LP1_HP1_LE1",
    # "W11_LP1_HP1_LE1",
    # "W12_LP1_HP1_LE1",
    # "W13_LP1_HP1_LE1",
    # "W14_LP1_HP1_LE1",
    # "W15_LP1_HP1_LE1",
    # "W16_LP1_HP1_LE1",
    # "W17_LP1_HP1_LE1",
    # "W18_LP1_HP1_LE1",
    # "W19_LP1_HP1_LE1",
    # "W20_LP1_HP1_LE1",
    # "W21_LP1_HP1_LE1",
    # "W22_LP1_HP1_LE1",
    # "W23_LP1_HP1_LE1",
    # "W24_LP1_HP1_LE1",
    # "W25_LP1_HP1_LE1",
    # "W26_LP1_HP1_LE1",
    # "W27_LP1_HP1_LE1",
    # "W28_LP1_HP1_LE1",
    # "W29_LP1_HP0_LE1",
    "W30_LP1_HP0_LE0",
    # "W31_LP1_HP1_LE0",
    # "W32_LP0_HP0_LE1",
    "W33_LP0_HP0_LE0",
    # "W34_LP0_HP1_LE0",
    # "W35_LP0_HP1_LE1",
    # 'W28_CD_LP1_HP1_LE1',
    # 'W29_CD_LP1_HP0_LE1',
    # 'W30_CD_LP1_HP0_LE0',
    # 'W31_CD_LP1_HP1_LE0',
    # 'W32_CD_LP0_HP0_LE1',
    # 'W33_CD_LP0_HP0_LE0',
    # 'W34_CD_LP0_HP1_LE0',
    # 'W35_CD_LP0_HP1_LE1',
]



PDMD = [


]

"""________________________________________________________________________________"""

"""Label list set up"""
label = [0]*100
step = 1
n_ave= 240


"""________________________________________________________________________________"""


def logic(index):
    if index % step == 0:
        return False
    return True


"""________________________________________________________________________________"""


for pdm in range(len(PDM)):
    """     Random colors    """
    # col = (
    #         rd.random(),
    #         rd.random(),
    #         rd.random()
    #         )
    """     Danfoss colors   """
    # if pdm == 0:
    #     col = (1, 0, 0)
    # if pdm == 1:
    #     col = (0, 0, 0)
    # if pdm == 2:
    #     col = (0.5, 0.5, 0.5)
    # if pdm == 3:
    #     col = (0.8, 0.8, 0.8)
    # if pdm == 4:
    #     col = (0.6, 0.1, 0.1)
    # if pdm == 5:
    #     col = (0.2, 0.2, 0.2)
    # if pdm == 6:
    #     col = (1, 0.5, 0.5)
    # if pdm == 7:
    #     col = (1, 0.9, 0.9)

    """     Visible colors   """
    if pdm == 0:
        col = (1, 0, 0)
    if pdm == 1:
        col = (0, 0.9, 1)
    if pdm == 2:
        col = (0.6, 0.2, 0.8)
    if pdm == 3:
        col = (1, 1, 0)
    if pdm == 4:
        col = (0.4, 1, 0)
    if pdm == 5:
        col = (0, 0.2, 1)
    if pdm == 6:
        col = (1, 0, 1)
    if pdm == 7:
        col = (0, 0, 0)

    if PDM[pdm][5]=='D':
        df = pd.read_csv('Data_cleaned/' + PDM[pdm], skiprows=lambda x: logic(x), na_filter=True, skip_blank_lines=True, low_memory=False)
    else:
        df = pd.read_csv('Data_Mdot/' + PDM[pdm], skiprows=lambda x: logic(x), na_filter=True, skip_blank_lines=True, low_memory=False)

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

#     """ Order of Polynomial fit """
#     po = 10
#     n = 1
#     """________________________________________________________________________________"""
#
#     wn = []
#     pdml = len(PDM) + 1
#     leg = PDM[:pdml] * 2
#     wt = " "
#     for i in range(len(leg)):
#
#         if len(leg)-1> i >=len(leg)/2:
#             leg[i] += " scatter data"
#
#         elif i <len(leg)/2:
#             wt += leg[i][:3] + ", "
#             leg[i] += " polynomial regression order " + str(po)
#         else:
#             wt = wt[:-2]
#             wt += " & " + leg[i][:3]
#             leg[i] += " scatter data"

    totcycl = np.array(df['Average number of cycles MT']) + np.array(df['Average number of cycles IT']) + np.array(df['Average number of cycles LT'])
    totload = np.array(df['Cooling load LT [W]']) + np.array(df['Cooling load MT [W]']) + np.array(df['Cooling load AC [W]'])
    totmass = np.array(df['LT mass flow rate [kg/s]']) + np.array(df['MT mass flow rate [kg/s]']) + np.array(df['AC mass flow rate [kg/s]'])
    """______________________________________ X _________________________________________"""
    # v1, label[1] = df['time'], 'Time [sec] '
    # v1, label[1] = df['T3 GC Outlet'], 'T3 GC Outlet'
    v1, label[1] = df['Tair external air'], 'Tair external air'
    # v1, label[1] = totload, 'Total cooling load [W]'
    # v1, label[1] = totmass, 'Total mass flow rate [W]'
    # v1, label[1] = df['Cooling load LT [W]'], 'Cooling load LT [W]'
    # v1, label[1] = df['Cooling load MT [W]'], 'Cooling load MT [W]'
    # v1, label[1] = df['Cooling load AC [W]'], 'Cooling load AC [W]'
    # v1, label[1] = df['P2 receiver'],'P2 receiver [Pa]'
    # v1, label[1] = df[],
    # v1, label[1] = df[],

    """______________________________________ Y _________________________________________"""
    # 2nd law from Exergy based is more accurate
    # v2, label[2] = df['2nd law efficiency Exergy based'], '2nd law efficiency Exergy based'
    # v2, label[2] = df['2nd law efficiency (COP/COP Carnot)'], '2nd law efficiency (COP_COP Carnot)'
    # v2, label[2] = df['COP[-]'], 'COP[-]'
    # v2, label[2] = df['Total Power'],'Total Power[W]'
    # v2, label[2] = df['Power Meter LT'],'Power Meter LT[W]'
    # v2, label[2] = df['Power Meter MT'],'Power Meter MT[W]'
    # v2, label[2] = df['Power Meter AUX'],'Power Meter AUX[W]'
    # v2, label[2] = df['P2 receiver'],'P2 receiver [Pa]'
    # v2, label[2] = df['P6 MT suction'],'P6 MT suction [Pa]'
    # v2, label[2] = df['P7 ejector inlet'], 'P7 ejector inlet [Pa]'
    # v2, label[2] = df['Pressure lift, MT suc to Rec'],'Pressure lift, MT suc to Rec [Pa]'
    # v2, label[2] = df['Pressure drop, Ej inlet to Rec'],'Pressure drop, Ej inlet to Rec [Pa]'
    # v2, label[2] = df['Ideal COP[-] compressor eta_isen = 1'], 'Ideal COP[-] compressor eta_isen = 1'
    # v2, label[2] = df[],
    # v2, label[2] = df[],
    # v2, label[2] = totmass, 'Total mass flow rate [W]'
    # v2, label[2] = totload, 'Total cooling load [W]'
    # v2, label[2] = df['Cooling load LT [W]'], 'Cooling load LT [W]'
    # v2, label[2] = df['Cooling load MT [W]'], 'Cooling load MT [W]'
    v2, label[2] = df['Cooling load AC [W]'], 'Cooling load AC [W]'
    # v2, label[2] = df[],
    # v2, label[2] = df[],
    # v2, label[2] = totcycl,'Average total number of cycles of compressors'
    # v2, label[2] = df['Average number of cycles MT'], 'Average number of cycles MT'
    # v2, label[2] = df['Average number of cycles IT'], 'Average number of cycles IT'
    # v2, label[2] = df['Average number of cycles LT'], 'Average number of cycles LT'

    # [28 29 33 34]  # To see effect of HP ejector
    # [28 31 32 33]  # To see effect of Liquid ejector
    # [28 30 33 35]  # To see effect of LP ejector
    # [3 4 5 6 11 12 13 ]  # To see effect ejector and no ejector mode in winter
    # [28 29 30 31 32 33 34 35]  # To see effect in various summer weeks
    """_________________________________ var1, var2 ______________________________________"""
    time = df['time'].tolist()
    var1 = v1.tolist()
    var2 = v2.tolist()

    # var3 = (-np.array(df['P6 MT suction'])+np.array(df['P7 ejector inlet'])).tolist()
    # var3 = (-np.array(var1)+np.array(var2)).tolist()
    # plot_2(time, var1, var2, ["Time [s]", label[1], label[2]], PDM[pdm][0:2])
    # plt.scatter(mov_ave(var1, n_ave), mov_ave(var2, n_ave), s=0.2)

    po = 10
    sctFitAve(var1, var2, po, col, label)

    # sct_fit(var1, var3, po, col, label)
    """To fix the legend"""
    pdml = 18
    leg =  [""] * len(PDM) * 3

    wt = " "
    lenLeg = len(leg)
    for i in range(lenLeg):

        if i<=lenLeg/3*2-1 and i%2==0:

            leg[i] += PDM[int(i/2)][:pdml] + " polynomial regression order " + str(po)

        elif i<=lenLeg/3*2 and i%2==1:
            leg[i] += PDM[int((i-1)/2)][:pdml] + " Average value "
            print(PDM[i-len(PDM)][:pdml])
        else:
            leg[i] +=PDM[i-len(PDM)*2][:pdml] + " scatter data"

    # for i in range(len(leg)):
    #
    #     if len(leg)-1> i >=len(leg)/2:
    #         leg[i] += " scatter data"
    #
    #     elif i <len(leg)/2:
    #         wt += leg[i][:3] + ", "
    #         leg[i] += " polynomial regression order " + str(po)
    #     else:
    #         wt = wt[:-2]
    #         wt += " & " + leg[i][:3]
    #         leg[i] += " scatter data"

    plt.legend(leg)

    #####################################

    # plot_1(time, mov_ave(var3, n_ave), ["Time [s]", label[1], label[2]], PDM[pdm][0:2])
    # plot_2(time, mov_ave(var1, n_ave), mov_ave(var2, n_ave), ["Time [s]", label[1], label[2]], PDM[pdm][0:2])

plt.show()


