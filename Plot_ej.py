
import pandas as pd                 # Dataframe library
import numpy as np                  # Scientific computing with nD object support
from functions import mov_ave, plt, sct_fit, fit,plot_1 ,plot_3, plot_6, sctFitAve, sctMVAve
import random as rd


"""________________________________________________________________________________"""
PDM = [
# 'MdotCompHPV_Week28',
# 'MdotCompHPV_Week29',
'MdotCompHPV_Week30',
# 'MdotCompHPV_Week31',
'MdotCompHPV_Week32',
# 'MdotCompHPV_Week33',
'MdotCompHPV_Week34',
# 'MdotCompHPV_Week35',
]



PDMD = [


]

"""________________________________________________________________________________"""

"""Label list set up"""
label = [0]*7
step = 1
n_ave= 240
label[0]='noname'

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


    df = pd.read_csv( 'Data_Mdot/'+PDM[pdm], skiprows=lambda x: logic(x), na_filter=True, skip_blank_lines=True, low_memory=False)
    print(df.columns)
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
    v1, label[1] = df['time'], 'Time [sec] '
    # v1, label[1] = df['T3 GC Outlet'], 'T3 GC Outlet'
    # v1, label[1] = df['Tair external air'], 'Tair external air'
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
    # v2, label[2] = df['Cooling load AC [W]'], 'Cooling load AC [W]'
    v2, label[2] = df['mac'], 'mac'
    v3, label[3] = df['mmt'], 'mmt'
    v4, label[4] = df['mmtc'], 'mmtc'
    v5, label[5] = df['mitc'], 'mitc'
    v6, label[6] = df['mhpv'], 'mhpv'
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


    time = df['time'].tolist()
    var1 = v1.tolist()
    var2 = v2.tolist()
    var3 = v3.tolist()
    var4 = v4.tolist()
    var5 = v5.tolist()
    var6 = v6.tolist()
    print(var6)
    print(label)
    var7= []
    for i in range(int(len(var6)/2)):
        var7.append(var6[i])
        var7.append(var6[i])



    plot_6(var1, var2,var3,var4,var5,var7,var7,label,PDM[pdm])

    from functions import plot_2
    suc = np.array(var2)
    mot = np.array(var4) +np.array(var5)-np.array(var7)

    mot = [0.01 if i < 0 else i for i in mot]
    suc = [0.01 if i < 0 else i for i in suc]
    rat = np.array(suc)/np.array(mot)
    rat = [0 if i < 0 else i for i in rat]
    rat = [0 if i > 1 else i for i in rat]
    plot_2(var1, suc,mot,label,PDM[pdm])
    plot_2(var1, rat, rat, label, PDM[pdm])
    plt.show()
    # var3 = (-np.array(df['P6 MT suction'])+np.array(df['P7 ejector inlet'])).tolist()
    # var3 = (-np.array(var1)+np.array(var2)).tolist()
    # plot_2(time, var1, var2, ["Time [s]", label[1], label[2]], PDM[pdm][0:2])
    # plt.scatter(mov_ave(var1, n_ave), mov_ave(var2, n_ave), s=0.2)


    # sctFitAve(var1, var2, po, col, label)




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


    #####################################

    # plot_1(time, mov_ave(var3, n_ave), ["Time [s]", label[1], label[2]], PDM[pdm][0:2])
    # plot_2(time, mov_ave(var1, n_ave), mov_ave(var2, n_ave), ["Time [s]", label[1], label[2]], PDM[pdm][0:2])

plt.show()

#