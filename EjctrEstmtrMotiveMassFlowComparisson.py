import numpy as np
import pandas as pd
from TDN import PSI
from functions import plot_2, plot_3, plot_4, plot_5, plot_6, plot_4_ej, plot_7_ej, mov_ave
import matplotlib.pyplot as plt
import numpy as np  # Scientific computing with nD object support
from datetime import datetime
from TDN import TDN
from functions import mov_ave, plot_corr, plot_5, print_weekly_ave, print_lengly_ave, is_nan
from sklearn.metrics import r2_score as r2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics, linear_model
from sklearn.ensemble import IsolationForest
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.tsa.vector_ar.var_model import VAR

"""Data input"""

""" SELECT EJECTOR TYPE """
""" !!!!!!  For separate cartridge !!!!! """
""" LP """
# ejctrSize = "LP_EJ1" # 60  kg/h @90bar , 35C
# ejctrSize = "LP_EJ2" # 125 kg/h @90bar , 35C
# ejctrSize = "LP_EJ3" # 250 kg/h @90bar , 35C
# ejctrSize = "LP_EJ4" # 500 kg/h @90bar , 35C
""" HP """
# ejctrSize = "HP_EJ1" # 125 kg/h @90bar , 35C
# ejctrSize = "HP_EJ2" # 250 kg/h @90bar , 35C
# ejctrSize = "HP_EJ3" # 500 kg/h @90bar , 35C
# ejctrSize = "HP_EJ4" # 1000 kg/h @90bar , 35C
""" LE """
# ejctrSize = "LEJ1"   # 200 kg/h @90bar , 35C
# ejctrSize = "LEJ2"   # 400 kg/h @90bar , 35C

train_ratio = 0.99
outlierRatio = 0.01
regressionMethod = [
    " Bayesian Ridge ",
    # " Linear Discriminant Analysis ",
    # " Linear Regression ",
    # " Bayesian Ridge alpha 0.5 ",
    # " Kernel Ridge ",
    # " SGD Regressor ",
    # " GaussianProcessRegressor(Takes ages to run ...) ",
    # " Huber Regressor ",
    # " Theil Sen Regressor "
    # " Bla Bla "
]


def mEjecEst(lstInp, ejctrSize, LabOnly):
    if LabOnly == True:
        fileName = r'C:\Users\U375297\Danfoss\RAC Tech Center - Programming Projects - Documents\Python Projects\MultiPack\Ejector Data\LabDataOnly.xlsx'
    else:
        fileName = r'C:\Users\U375297\Danfoss\RAC Tech Center - Programming Projects - Documents\Python Projects\MultiPack\Ejector Data\LabCFDROM.xlsx'

    df = pd.read_excel(fileName, sheet_name=ejctrSize)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna(axis='rows', how='any', thresh=None, subset=None, inplace=False)
    """ To shuffle dataset """
    df = df.sample(frac=1).reset_index(drop=True)

    trainPar = ["P_MN",
                "T_MN",
                # "h_MN",
                "P_SN ",
                "T_SN",
                # "q_SN",
                # "h_SN",
                "P_OUT",
                ]

    mMotLabl = "MFR_MN"
    mSucLabl = "MFR_SN"

    """ COOOOOOLLLLL:::  To display all columns and rows"""
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print(df.tail)
    # with pd.option_context('display.max_rows', 10, 'display.max_columns', None):  # more options can be specified also
    #     print(df)

    """________________________________________________________________________________"""
    data_tr = df[trainPar]
    """________________________________________________________________________________"""
    mMot = df[mMotLabl]
    """Set negative values to < 0 > """
    mMot = [0 if i < 0 else i for i in mMot]
    """________________________________________________________________________________"""
    mSuc = df[mSucLabl]
    """Set negative values to < 0 > """
    mSuc = [0 if i < 0 else i for i in mSuc]
    """___________________________________________________________________________________"""

    """  ______________Multivariate Linear Regression____________  """
    """Making train and validation set"""
    """ Outlier removal """

    """____________________________________________________"""
    iso = IsolationForest(contamination=outlierRatio)
    yhat = iso.fit_predict(data_tr, mMot)
    # select all rows that are not outliers
    mask = yhat != -1

    data_trM, mMotM, mSucM = [], [], []
    for s in range(len(mask)):
        if mask[s]:
            data_trM.append(data_tr.values.tolist()[s])
            mMotM.append(mMot[s])
            mSucM.append(mSuc[s])
    data_tr, mMot, mSuc = data_trM, mMotM, mSucM
    """____________________________________________________"""

    print("Outlier Ratio : ", (df.shape[0] - len(data_tr)), "/", df.shape[0], "; Train Ratio : ", train_ratio)
    print("Train Parameters : ", trainPar)
    """___________________________________________________________________________________"""
    """___________________________________________________________________________________"""

    """ Regression model selection """
    """_________-  Multivariate Linear Regression -_______________ """
    for regMeth in regressionMethod:
        print('Method for regression: ',regMeth)

        X_train = data_tr[:int(train_ratio * (len(data_tr)))]
        X_test = data_tr[int(train_ratio * (len(data_tr))):]
        y_train = mMot[:int(train_ratio * (len(mMot)))]
        y_test = mMot[int(train_ratio * (len(mMot))):]

        if regMeth == " Bayesian Ridge ":
            """ Bayesian Ridge """
            regressor = linear_model.BayesianRidge()
            regressor2 = linear_model.BayesianRidge()

        elif regMeth == " Linear Discriminant Analysis ":
            """ Linear Discriminant Analysis """
            regressor = linear_model.RidgeCV(alphas=np.logspace(-6, 6, 13))
            regressor2 = linear_model.RidgeCV(alphas=np.logspace(-6, 6, 13))

        elif regMeth == " Linear Regression ":
            """ Linear Regression """
            regressor = linear_model.LinearRegression()
            regressor2 = linear_model.LinearRegression()

        elif regMeth == " Bayesian Ridge alpha 0.5 ":
            """ Bayesian Ridge alpha 0.5 """
            regressor = linear_model.Ridge(alpha=.5)
            regressor2 = linear_model.Ridge(alpha=.5)

        elif regMeth == " Kernel Ridge ":
            """ KernelRidge """
            from sklearn.kernel_ridge import KernelRidge
            regressor = KernelRidge(alpha=1.0)
            regressor2 = KernelRidge(alpha=1.0)

        elif regMeth == " SGD Regressor ":
            """ SGDRegressor """
            from sklearn.linear_model import SGDRegressor
            from sklearn.pipeline import make_pipeline
            from sklearn.preprocessing import StandardScaler
            regressor = make_pipeline(StandardScaler(), SGDRegressor(max_iter=1000, tol=1e-3))
            regressor2 = make_pipeline(StandardScaler(), SGDRegressor(max_iter=1000, tol=1e-3))

        elif regMeth == " Gaussian Process Regressor(Takes ages to run ...) ":
            """ GaussianProcessRegressor(Takes ages to run ...) """
            from sklearn.datasets import make_friedman2
            from sklearn.gaussian_process import GaussianProcessRegressor
            from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
            kernel = DotProduct() + WhiteKernel()
            regressor = GaussianProcessRegressor(kernel=kernel, random_state=0)
            regressor2 = GaussianProcessRegressor(kernel=kernel, random_state=0)

        elif regMeth == " Huber Regressor ":
            """ HuberRegressor """
            from sklearn.linear_model import HuberRegressor, LinearRegression
            from sklearn.datasets import make_regression
            regressor = linear_model.HuberRegressor()
            regressor2 = linear_model.HuberRegressor()

        elif regMeth == " Theil Sen Regressor ":
            """ TheilSenRegressor """
            from sklearn.linear_model import TheilSenRegressor
            from sklearn.datasets import make_regression
            regressor = linear_model.TheilSenRegressor()
            regressor2 = linear_model.TheilSenRegressor()

        else:
            """ Linear Regression """
            regressor = linear_model.LinearRegression()
            regressor2 = linear_model.LinearRegression()

        # #  # """ ???????????????????????????????????
        # #  # """
        # #  # poly = PolynomialFeatures(degree=2)
        # #  # regressor  = poly.fit_transform
        # #  # regressor2 = poly.fit_transform

        """___________________________________________________________________________________"""
        """___________________________________________________________________________________"""
        """___________________________________________________________________________________"""

        """ Create the Linear Model (LinearRegression) """
        regressor.fit(X_train, y_train)
        # print('Train Score Motive:', regressor.score(X_train, y_train))
        print('Test Score Motive:', regressor.score(X_test, y_test))
        """ Interpreting the Coefficient and the Intercept """
        # mMot_pred = regressor.predict(X_test)

        """  ______________Multivariate Linear Regression____________  """
        """Making train and validation set"""
        y_train = mSuc[:int(train_ratio * (len(mMot)))]
        y_test = mSuc[int(train_ratio * (len(mMot))):]
        regressor2.fit(X_train, y_train)
        # print('Train Score Suction:', regressor2.score(X_train, y_train))
        print('Test Score Suction:', regressor2.score(X_test, y_test))
        # print(' # of columns used: ', len(trainPar), ';   Train ratio : ', train_ratio)
        """ Interpreting the Coefficient and the Intercept """
        # mSuc_pred = regressor.predict(X_test)


        """ Try later
               
               
               zn = interpolate.griddata(
            points, values, (grid_xn, grid_yn), fill_value=0, method='cubic')
            
            
            """

    return regressor.predict(lstInp)


# print(mEjecEst(lstInp, ejctrSize, LabOnly=False))

ejtplst = [
    'Multi Ejector HP 1875',  # #"4 cartridge"
    'Multi Ejector HP 3875',  # #"6 cartridge"
    'Multi Ejector LP 935',  # #"4 cartridge"
    'Multi Ejector LP 1935',  # #"6 cartridge"
    'CTM 1 LE 200',
    'CTM 1 LE 400',
    'CTM 2 LE 600', ]

""" !!!!!!  For separate cartridge !!!!! """
""" LP """
# ejctrSize = "LP_EJ1" # 60  kg/h @90bar , 35C
# ejctrSize = "LP_EJ2" # 125 kg/h @90bar , 35C
# ejctrSize = "LP_EJ3" # 250 kg/h @90bar , 35C
# ejctrSize = "LP_EJ4" # 500 kg/h @90bar , 35C
""" HP """
# ejctrSize = "HP_EJ1" # 125 kg/h @90bar , 35C
# ejctrSize = "HP_EJ2" # 250 kg/h @90bar , 35C
# ejctrSize = "HP_EJ3" # 500 kg/h @90bar , 35C
# ejctrSize = "HP_EJ4" # 1000 kg/h @90bar , 35C
""" LE """


# ejctrSize = "LEJ1"   # 200 kg/h @90bar , 35C
# ejctrSize = "LEJ2"   # 400 kg/h @90bar , 35C
def mEjecBlock(lstInp, ejecType, LabOnly):
    if ejecType == 'CTM 2 LE 600':
        le200 = mEjecEst(lstInp, "LEJ1", LabOnly)
        le400 = mEjecEst(lstInp, "LEJ2", LabOnly)
        print("le200", np.mean(le200),
              "le400", np.mean(le400),
              sep='/n')
        sum = list(np.array(le200) * 200 / 600 + np.array(le400) * 400 / 600)

    elif ejecType == 'Multi Ejector LP 1935':
        lp60 = mEjecEst(lstInp, "LP_EJ1",  LabOnly)
        lp125 = mEjecEst(lstInp, "LP_EJ2", LabOnly)
        lp250 = mEjecEst(lstInp, "LP_EJ3", LabOnly)
        lp500 = mEjecEst(lstInp, "LP_EJ4", LabOnly)
        print("lp60  : ", np.mean(lp60),
              "lp125 : ", np.mean(lp125),
              "lp250 : ", np.mean(lp250),
              "lp500 : ", np.mean(lp500),
              sep='/n')
        sum = (np.array(lp60) * 60 / 1935 +
               np.array(lp125) * 125 / 1935 +
               np.array(lp250) * 250 / 1935 +
               np.array(lp500) * 1500 / 1935
               ).tolist()

    elif ejecType == 'Multi Ejector HP 3875':
        hp125 = mEjecEst(lstInp, "HP_EJ1", LabOnly )
        hp250 = mEjecEst(lstInp, "HP_EJ2", LabOnly )
        hp500 = mEjecEst(lstInp, "HP_EJ3", LabOnly )
        hp1000 = mEjecEst(lstInp, "HP_EJ4", LabOnly)
        print("hp60  : ", np.mean(hp125),
              "hp125 : ", np.mean(hp250),
              "hp250 : ", np.mean(hp500),
              "hp500 : ", np.mean(hp1000),
              sep='/n'
              )
        sum = (np.array(hp125) * 125 / 3875 +
               np.array(hp250) * 250 / 3875 +
               np.array(hp500) * 500 / 3875 +
               np.array(hp1000) * 3000 / 3875
               ).tolist()
    else:
        print("Requested ejector is not defined, can be defined by knowing the cartridge capacities as in the function")
        sum = 0

    return sum

# hptest = [[50.00,10.00, 26.00,	-10.65,	30.00],  # #
#           [50.00,10.00, 26.00,	-10.65,	35.00],  # #
#           [50.00,10.00, 26.00,	-10.65,	40.00],  # #
#           [50.00,10.00, 26.00,	-10.65,	30.00]]  # #
#
# lptest = [[50.00, 10.00, 26.00, -10.65, 28.00],  # # HP2=0,208 Hp3=0,181 HP4=0,176
#           [50.00, 10.00, 26.00, -10.65, 32.00],  # # HP2=0     Hp3=0     HP4=0
#           [50.00, 10.00, 26.00, -10.65, 36.00],  # # HP2=0,042 Hp3=0     HP4=0
#           [50.00, 10.00, 26.00, -10.65, 32.00]]  # # HP2=0     Hp3=0,170 HP4=0,144
#
# letest = [[50.87, 4.00, 26.00, -10.65, 29.00],   # # LE1=0,268 LE2=0,417
#           [50.87, 9.00, 26.00, -10.65, 29.00],   # # LE1=0,437 LE2=0,556
#           [50.87, 14.0, 26.00, -10.65, 29.00],   # # LE1=0,395 LE2=0,532
#           [50.87, 4.00, 26.00, -10.65, 31.00]]   # # LE1=0,297 LE2=0,412
#
# print(mEjecBlock(hptest, 'CTM 2 LE 600', LabOnly=False))
# # print(mEjecBlock(lptest, 'Multi Ejector LP 1935', LabOnly=False))
# # print(mEjecBlock(letest, 'Multi Ejector HP 3875', LabOnly=False))
