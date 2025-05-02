import pandas as pd
import matplotlib.pyplot as plt

"""________________________________________________________________________________"""
""" LT  """
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
        W28_ACLP1_HP1_ALC1, W29_ACLP1_HP0_ALC1, W30_ACLP1_HP0_ALC0, W31_ACLP1_HP1_ALC0,
        W32_ACDX1_HP0_ALC1, W33_ACDX1_HP0_ALC0, W34_ACDX1_HP1_ALC0, W35_ACDX1_HP1_ALC1
    ]

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


    # with pd.option_context('display.max_rows', 100, 'display.max_columns', None):  # more options can be specified also
    #     print(dat_ml)
    print(dat_ml.columns)
    # print(dat_ml.head(6))
    # print(i[0][0][9:])
    # plt.plot(dat_ml['mac'])
    path = "C:\\Users\\U375297\\Documents\\PycharmProjects\\Danfoss\\MultiPack\\Data_Mdot\\"
    dat_ml.to_csv(path+"MTotComp_" + i[0][0][9:])

# plt.show()