
import pandas as pd               # Dataframe library
import numpy as np                # Scientific computing with nD object support
import matplotlib.pyplot as plt
from datetime import datetime, time, date
from functions import mov_ave, plot_corr, patch_spine_invisible

# ______________________________________________________________________________________________ #

source = "Danfoss"
# source = "CNR"

""" Load data as CSV """
if source == "Danfoss":
    """------DANFOSS DATA-----"""
    W28_ACLP1_HP1_ALC1 = "CNT-Porto Mós CNT-Porto Mós 07181621.csv"
    W29_ACLP1_HP0_ALC1 = "CNT-Porto Mós CNT-Porto Mós 07251740.csv"
    W30_ACLP1_HP0_ALC0 = "CNT-Porto Mós CNT-Porto Mós 08011828.csv"
    W31_ACLP1_HP1_ALC0 = "CNT-Porto Mós CNT-Porto Mós 08081807.csv"
    W32_ACDX1_HP0_ALC1 = "CNT-Porto Mós CNT-Porto Mós 08141822.csv"
    W33_ACDX1_HP0_ALC0 = "CNT-Porto Mós CNT-Porto Mós 08221642.csv"
    W34_ACDX1_HP1_ALC0 = "CNT-Porto Mós CNT-Porto Mós 08291846.csv"
    W35_ACDX1_HP1_ALC1 = "CNT-Porto Mós CNT-Porto Mós 09111019.csv"

    PDM = [W28_ACLP1_HP1_ALC1, W29_ACLP1_HP0_ALC1, W30_ACLP1_HP0_ALC0, W31_ACLP1_HP1_ALC0, W32_ACDX1_HP0_ALC1,
           W33_ACDX1_HP0_ALC0, W34_ACDX1_HP1_ALC0, W35_ACDX1_HP1_ALC1]


if source == "CNR":
    """------CNR DATA-----"""
    W28_ACLP1_HP1_ALC1 = "11_07_2019_to_18_07_2019_converted.csv"
    W29_ACLP1_HP0_ALC1 = "18_07_2019_to_25_07_2019_converted.csv"
    W30_ACLP1_HP0_ALC0 = "25_07_2019_to_01_08_2019_converted.csv"
    W31_ACLP1_HP1_ALC0 = "01_08_2019_to_08_08_2019_converted.csv"
    W32_ACDX1_HP0_ALC1 = "08_08_2019_to_15_08_2019_converted.csv"
    W33_ACDX1_HP0_ALC0 = "15_08_2019_to_22_08_2019_converted.csv"
    W34_ACDX1_HP1_ALC0 = "22_08_2019_to_29_08_2019_converted.csv"
    W35_ACDX1_HP1_ALC1 = "29_08_2019_to_05_09_2019_converted.csv"

    PDM = [W28_ACLP1_HP1_ALC1, W29_ACLP1_HP0_ALC1, W30_ACLP1_HP0_ALC0, W31_ACLP1_HP1_ALC0, W32_ACDX1_HP0_ALC1,
           W33_ACDX1_HP0_ALC0, W34_ACDX1_HP1_ALC0, W35_ACDX1_HP1_ALC1]

"""Select a week : from 28 to 35 """
week = 29

for i in range(28, week):
    weekdata = PDM[i-28]
    """ Load data as CSV """

    if source == "CNR":
        df = pd.read_csv(weekdata,  sep=';')  # takes all rows
        dfh = pd.read_csv("11_07_2019_to_18_07_2019_converted.csv", nrows=1,  sep=';')
        df.drop(df.columns[0], axis=1, inplace=True)
        df.drop('Calculated values ==>', axis=1, inplace=True)

        """Change date format from 2019 - 08 - 01 17: 05:45.119  "%Y-%m-%d %H:%M:%S.%f "  to Seconds"""
        t0 = datetime.strptime(df.loc[0][0], "%Y-%m-%d %H:%M:%S.%f")  # Time refrence for date conversion
        for i in range(df.shape[0]):
            DT = datetime.strptime(df.loc[i][0], "%Y-%m-%d %H:%M:%S.%f")
            df.at[i, 'time'] = (DT - t0).total_seconds()

        df = df.apply(pd.to_numeric, errors='coerce')
        df = df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

    if source == "Danfoss":
        df = pd.read_csv(weekdata, skiprows=[0, 2, 3, 4, 5])  # takes all rows
        # df = pd.read_csv(weekdata, nrows=100, skiprows=[0, 2, 3, 4, 5]) # takes 100 rows only
        dfh = pd.read_csv("PDM_Header.csv")

        """Change date format from  " %H:%M:%S %d/%m/%Y"  to Seconds"""

        t0 = datetime.strptime(df.loc[0][0], " %H:%M:%S %d/%m/%Y")  # Time refrence for date conversion
        for i in range(df.shape[0]):
            DT = datetime.strptime(df.loc[i][0], " %H:%M:%S %d/%m/%Y")
            df.at[i, 'Name'] = (DT - t0).total_seconds()

        df = df.apply(pd.to_numeric, errors='coerce')
        df = df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

    """Header of data file"""
    dfh = pd.read_csv("PDM_Header.csv")

    # ______________________________________________________________________________________________ #

    """ df.loc first indicate row and second indicates column"""
    print(df.shape)
    print(df.head(6))
    # print(df.tail(6))
    # print(df.iloc[4][0])
    # print(df.size)

    """ Print data in a column"""
    # print(df['Controlo Inj. UTA1:   Actual SH Reference'])

    """ To check for Null values"""
    # print(df.isnull().values.any())
    # print(df.isnull().values)

    """ Print column names"""
    # print(df.columns)

    """ Map data"""
    """ 
     Maps every 1 to random :
     # corr_map = {1: 'random '}
     Applies the mapping instruction to the certain column of data :
     # dfc['AK-PC 782A:   Trec reference'] = dfc['AK-PC 782A:   Trec reference'].map(corr_map)
    """

    """ 
    Checks True/False ratio for Corr
    # num_t = len(dfc.loc[dfc['AK-PC 782A:   Trec reference'] != 1.0])
    # num_f = len(dfc.loc[dfc['AK-PC 782A:   Trec reference'] == 1.0])
    # print("Number of false: " + str(num_f) + "    Ratio of false:" + str(round(num_f/(num_f+num_t),4)))
    """
    # ______________________________________________________________________________________________ #

    # ______________________________________________________________________________________________ #
    """Loops through the data and eliminates the columns that mostly contain null values """
    for j in range(10):
        for i in range(1, len(df.columns)-1):
            if i >= len(df.columns):
                break
            try:
                if round((float(df.iloc[6][i])-float(df.iloc[60][i])), 6)==0 or df.iloc[6][i] == 0 or df.isnull().iloc[6][i]:
                    df.drop(df.columns[i], axis=1, inplace=True)
            except:
                print("TRY  FAILED", df.iloc[6][i], df.iloc[60][i]," NON FLOAT VALUE")

    # ______________________________________________________________________________________________ #

    """____   !!!!! ____   WRITE ___ !!!!! ___"""
    """AFTER REMOVING NaN, Missing and Zeros """
    """Correlation """

    df.corr().to_csv("Corr_" + weekdata)
    dfc = pd.read_csv("Corr_" + weekdata)

    # ______________________________________________________________________________________________ #

    """Prints correlated variables"""

    num_corr = 0
    num_corr_1 = 0
    corr_list = []

    """Prints the pair of correlated items:  dfci dataframe saves the as PDF"""

    for i in range(1, dfc.shape[1] - 1):
        for j in range(1, dfc.shape[1] - 1):
            if dfc.loc[i][j] > 0.98 and i+1 != j:
                # print(str(dfc.columns[i]) + " -> " + str(i) + dfc.columns[j], " -> ", str(j), "  ",
                # str(round(dfc.loc[i][j], 3)))
                corr_list.append([dfc.columns[i], str(i), dfc.columns[j], str(j), "  ",
                str(round(dfc.loc[i][j], 3))])
                num_corr += 1

            if dfc.loc[i][j] > 0.999 and i+1 != j:
                num_corr_1 += 1
    """Based on a list of list creates the dataframe of mapping of corrolated pairs of data"""
    dfci = pd.DataFrame(corr_list, columns=['Sensor name ', ' index ', ' Sensor name ', 'index ', ' ', 'Correlation strength '])
    dfci.to_excel("Corr_pairs_" + weekdata + ".xlsx")
    # ______________________________________________________________________________________________ #

    print("Number of correlated columns : " + str(num_corr))
    print("Number of 100% correlated columns : " + str(num_corr_1))
    plot_corr(df)

    """
    Save plot as a file:
    Format :  'png', 'pdf', 'svg'.  
    Here PDF format is used.
    """

    plt.savefig("Corr_fig_" + weekdata, dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype=None,
                format='pdf', ransparent=False, bbox_inches=None, pad_inches=0.1, frameon=None, metadata=None)


plt.show()

