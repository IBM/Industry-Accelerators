# ----------------------------------------------------------------------------------------------------------------------
# IMPORT NEEDED LIBRARIES (AKA PACKAGES AKA TOOLBOXES)
# ----------------------------------------------------------------------------------------------------------------------

#
from IPython.display import display, Image
from IPython.core.interactiveshell import InteractiveShell

#
import warnings
import itertools
import time
import math
import uuid
import multiprocessing
import datetime
from datetime import datetime as dt
# from collections import Iterable

#
import ast
import json
import sys
import os
import glob
from scipy.special import softmax
# import pydotplus
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

get_ipython().run_line_magic('matplotlib', 'inline')

#
from sklearn import *
from sklearn.metrics import *
from sklearn.model_selection import *
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeRegressor, _tree, export_graphviz
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LinearRegression, SGDRegressor, Lasso, LogisticRegression
# from sklearn.externals import joblib

#
from ibm_watson_machine_learning import APIClient

# notify scientist: completed analyses
print("DONE: 'STEP 0.1a: Import Software Packages' analysis")

# ----------------------------------------------------------------------------------------------------------------------
# MAKE CONSTANTS
# ----------------------------------------------------------------------------------------------------------------------

#
InteractiveShell.ast_node_interactivity = "all"

warnings.filterwarnings('ignore')

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', -1)

#
valu_numrowshead = 10

# ......................................................................................................................

#
name_suffix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

#
name_offering = "wxsignals"

#
name_client = "clientname"

# ......................................................................................................................

# make list of all weather variables
# https://docs.google.com/document/d/1UNNj2LOZWxnRVq3miD-uH21qmoUl2xWjANWdDoQwUEo/edit#
list_columnsweather_all = [
    'DewpointLocalDayAvg',
    'DewpointLocalDayMax',
    'DewpointLocalDayMin',
    'DewpointLocalDaytimeAvg',
    'DewpointLocalDaytimeMax',
    'DewpointLocalDaytimeMin',
    'DewpointLocalNighttimeAvg',
    'DewpointLocalNighttimeMax',
    'DewpointLocalNighttimeMin',
    'DewpointLocalMorningAvg',
    'DewpointLocalMorningMax',
    'DewpointLocalMorningMin',
    'DewpointLocalAfternoonAvg',
    'DewpointLocalAfternoonMax',
    'DewpointLocalAfternoonMin',
    'DewpointLocalEveningAvg',
    'DewpointLocalEveningMax',
    'DewpointLocalEveningMin',
    'DewpointLocalOvernightAvg',
    'DewpointLocalOvernightMax',
    'DewpointLocalOvernightMin',
    'FeelsLikeLocalDayAvg',
    'FeelsLikeLocalDayMax',
    'FeelsLikeLocalDayMin',
    'FeelsLikeLocalDaytimeAvg',
    'FeelsLikeLocalDaytimeMax',
    'FeelsLikeLocalDaytimeMin',
    'FeelsLikeLocalNighttimeAvg',
    'FeelsLikeLocalNighttimeMax',
    'FeelsLikeLocalNighttimeMin',
    'FeelsLikeLocalMorningAvg',
    'FeelsLikeLocalMorningMax',
    'FeelsLikeLocalMorningMin',
    'FeelsLikeLocalAfternoonAvg',
    'FeelsLikeLocalAfternoonMax',
    'FeelsLikeLocalAfternoonMin',
    'FeelsLikeLocalEveningAvg',
    'FeelsLikeLocalEveningMax',
    'FeelsLikeLocalEveningMin',
    'FeelsLikeLocalOvernightAvg',
    'FeelsLikeLocalOvernightMax',
    'FeelsLikeLocalOvernightMin',
    'GustLocalDayAvg',
    'GustLocalDayMax',
    'GustLocalDayMin',
    'GustLocalDaytimeAvg',
    'GustLocalDaytimeMax',
    'GustLocalDaytimeMin',
    'GustLocalNighttimeAvg',
    'GustLocalNighttimeMax',
    'GustLocalNighttimeMin',
    'GustLocalMorningAvg',
    'GustLocalMorningMax',
    'GustLocalMorningMin',
    'GustLocalAfternoonAvg',
    'GustLocalAfternoonMax',
    'GustLocalAfternoonMin',
    'GustLocalEveningAvg',
    'GustLocalEveningMax',
    'GustLocalEveningMin',
    'GustLocalOvernightAvg',
    'GustLocalOvernightMax',
    'GustLocalOvernightMin',
    'MSLPLocalDayAvg',
    'MSLPLocalDayMax',
    'MSLPLocalDayMin',
    'MSLPLocalDaytimeAvg',
    'MSLPLocalDaytimeMax',
    'MSLPLocalDaytimeMin',
    'MSLPLocalNighttimeAvg',
    'MSLPLocalNighttimeMax',
    'MSLPLocalNighttimeMin',
    'MSLPLocalMorningAvg',
    'MSLPLocalMorningMax',
    'MSLPLocalMorningMin',
    'MSLPLocalAfternoonAvg',
    'MSLPLocalAfternoonMax',
    'MSLPLocalAfternoonMin',
    'MSLPLocalEveningAvg',
    'MSLPLocalEveningMax',
    'MSLPLocalEveningMin',
    'MSLPLocalOvernightAvg',
    'MSLPLocalOvernightMax',
    'MSLPLocalOvernightMin',
    'PrecipAmountLocalDayAvg',
    'PrecipAmountLocalDayMax',
    'PrecipAmountLocalDayMin',
    'PrecipAmountLocalDaytimeAvg',
    'PrecipAmountLocalDaytimeMax',
    'PrecipAmountLocalDaytimeMin',
    'PrecipAmountLocalNighttimeAvg',
    'PrecipAmountLocalNighttimeMax',
    'PrecipAmountLocalNighttimeMin',
    'PrecipAmountLocalMorningAvg',
    'PrecipAmountLocalMorningMax',
    'PrecipAmountLocalMorningMin',
    'PrecipAmountLocalAfternoonAvg',
    'PrecipAmountLocalAfternoonMax',
    'PrecipAmountLocalAfternoonMin',
    'PrecipAmountLocalEveningAvg',
    'PrecipAmountLocalEveningMax',
    'PrecipAmountLocalEveningMin',
    'PrecipAmountLocalOvernightAvg',
    'PrecipAmountLocalOvernightMax',
    'PrecipAmountLocalOvernightMin',
    'RelativeHumidityLocalDayAvg',
    'RelativeHumidityLocalDayMax',
    'RelativeHumidityLocalDayMin',
    'RelativeHumidityLocalDaytimeAvg',
    'RelativeHumidityLocalDaytimeMax',
    'RelativeHumidityLocalDaytimeMin',
    'RelativeHumidityLocalNighttimeAvg',
    'RelativeHumidityLocalNighttimeMax',
    'RelativeHumidityLocalNighttimeMin',
    'RelativeHumidityLocalMorningAvg',
    'RelativeHumidityLocalMorningMax',
    'RelativeHumidityLocalMorningMin',
    'RelativeHumidityLocalAfternoonAvg',
    'RelativeHumidityLocalAfternoonMax',
    'RelativeHumidityLocalAfternoonMin',
    'RelativeHumidityLocalEveningAvg',
    'RelativeHumidityLocalEveningMax',
    'RelativeHumidityLocalEveningMin',
    'RelativeHumidityLocalOvernightAvg',
    'RelativeHumidityLocalOvernightMax',
    'RelativeHumidityLocalOvernightMin',
    'SnowAmountLocalDayAvg',
    'SnowAmountLocalDayMax',
    'SnowAmountLocalDayMin',
    'SnowAmountLocalDaytimeAvg',
    'SnowAmountLocalDaytimeMax',
    'SnowAmountLocalDaytimeMin',
    'SnowAmountLocalNighttimeAvg',
    'SnowAmountLocalNighttimeMax',
    'SnowAmountLocalNighttimeMin',
    'SnowAmountLocalMorningAvg',
    'SnowAmountLocalMorningMax',
    'SnowAmountLocalMorningMin',
    'SnowAmountLocalAfternoonAvg',
    'SnowAmountLocalAfternoonMax',
    'SnowAmountLocalAfternoonMin',
    'SnowAmountLocalEveningAvg',
    'SnowAmountLocalEveningMax',
    'SnowAmountLocalEveningMin',
    'SnowAmountLocalOvernightAvg',
    'SnowAmountLocalOvernightMax',
    'SnowAmountLocalOvernightMin',
    'TemperatureLocalDayAvg',
    'TemperatureLocalDayMax',
    'TemperatureLocalDayMin',
    'TemperatureLocalDaytimeAvg',
    'TemperatureLocalDaytimeMax',
    'TemperatureLocalDaytimeMin',
    'TemperatureLocalNighttimeAvg',
    'TemperatureLocalNighttimeMax',
    'TemperatureLocalNighttimeMin',
    'TemperatureLocalMorningAvg',
    'TemperatureLocalMorningMax',
    'TemperatureLocalMorningMin',
    'TemperatureLocalAfternoonAvg',
    'TemperatureLocalAfternoonMax',
    'TemperatureLocalAfternoonMin',
    'TemperatureLocalEveningAvg',
    'TemperatureLocalEveningMax',
    'TemperatureLocalEveningMin',
    'TemperatureLocalOvernightAvg',
    'TemperatureLocalOvernightMax',
    'TemperatureLocalOvernightMin',
    'UVIndexLocalDayAvg',
    'UVIndexLocalDayMax',
    'UVIndexLocalDayMin',
    'UVIndexLocalDaytimeAvg',
    'UVIndexLocalDaytimeMax',
    'UVIndexLocalDaytimeMin',
    'UVIndexLocalNighttimeAvg',
    'UVIndexLocalNighttimeMax',
    'UVIndexLocalNighttimeMin',
    'UVIndexLocalMorningAvg',
    'UVIndexLocalMorningMax',
    'UVIndexLocalMorningMin',
    'UVIndexLocalAfternoonAvg',
    'UVIndexLocalAfternoonMax',
    'UVIndexLocalAfternoonMin',
    'UVIndexLocalEveningAvg',
    'UVIndexLocalEveningMax',
    'UVIndexLocalEveningMin',
    'UVIndexLocalOvernightAvg',
    'UVIndexLocalOvernightMax',
    'UVIndexLocalOvernightMin',
    'VisibilityLocalDayAvg',
    'VisibilityLocalDayMax',
    'VisibilityLocalDayMin',
    'VisibilityLocalDaytimeAvg',
    'VisibilityLocalDaytimeMax',
    'VisibilityLocalDaytimeMin',
    'VisibilityLocalNighttimeAvg',
    'VisibilityLocalNighttimeMax',
    'VisibilityLocalNighttimeMin',
    'VisibilityLocalMorningAvg',
    'VisibilityLocalMorningMax',
    'VisibilityLocalMorningMin',
    'VisibilityLocalAfternoonAvg',
    'VisibilityLocalAfternoonMax',
    'VisibilityLocalAfternoonMin',
    'VisibilityLocalEveningAvg',
    'VisibilityLocalEveningMax',
    'VisibilityLocalEveningMin',
    'VisibilityLocalOvernightAvg',
    'VisibilityLocalOvernightMax',
    'VisibilityLocalOvernightMin',
    'WindSpeedLocalDayAvg',
    'WindSpeedLocalDayMax',
    'WindSpeedLocalDayMin',
    'WindSpeedLocalDaytimeAvg',
    'WindSpeedLocalDaytimeMax',
    'WindSpeedLocalDaytimeMin',
    'WindSpeedLocalNighttimeAvg',
    'WindSpeedLocalNighttimeMax',
    'WindSpeedLocalNighttimeMin',
    'WindSpeedLocalMorningAvg',
    'WindSpeedLocalMorningMax',
    'WindSpeedLocalMorningMin',
    'WindSpeedLocalAfternoonAvg',
    'WindSpeedLocalAfternoonMax',
    'WindSpeedLocalAfternoonMin',
    'WindSpeedLocalEveningAvg',
    'WindSpeedLocalEveningMax',
    'WindSpeedLocalEveningMin',
    'WindSpeedLocalOvernightAvg',
    'WindSpeedLocalOvernightMax',
    'WindSpeedLocalOvernightMin']

# make list of client-requested weather variables
# todo: compute set-theory overlap of "client pick vs algorithm pick" results
list_columnsweather_client = [
    "RelativeHumidityLocalDaytimeAvg",
    "TemperatureLocalDaytimeMax",
    "TemperatureLocalDaytimeMin",
    "DewpointLocalMorningAvg",
    "FeelsLikeLocalDaytimeMin",
    "FeelsLikeLocalDaytimeMax",
    "FeelsLikeLocalDaytimeAvg",
    "WindSpeedLocalDaytimeAvg",
    "GustLocalDayMax",
    "PrecipAmountLocalDayMax",
    "PrecipAmountLocalDayMin",
    "PrecipAmountLocalDayAvg",
    "PrecipAmountLocalDaytimeAvg",
    "PrecipAmountLocalEveningAvg",
    "SnowAmountLocalDayMax"]

# make list of scientist-decided weather variables
# https://docs.google.com/document/d/1UNNj2LOZWxnRVq3miD-uH21qmoUl2xWjANWdDoQwUEo/edit#
list_columnsweather_few = [
    "DewpointLocalMorningAvg",
    "FeelsLikeLocalDaytimeMin",
    "FeelsLikeLocalDaytimeMax",
    "FeelsLikeLocalDaytimeAvg",
    "GustLocalDayMax",
    "GustLocalDaytimeAvg",
    "GustLocalMorningAvg",
    "PrecipAmountLocalDayMax",
    "PrecipAmountLocalDayMin",
    "PrecipAmountLocalDayAvg",
    "PrecipAmountLocalDaytimeAvg",
    "PrecipAmountLocalEveningAvg",
    "RelativeHumidityLocalDaytimeMin",
    "RelativeHumidityLocalDaytimeMax",
    "RelativeHumidityLocalDaytimeAvg",
    "SnowAmountLocalDayMax",
    "TemperatureLocalDaytimeMax",
    "TemperatureLocalDaytimeMin",
    "TemperatureLocalDaytimeAvg",
    "UVIndexLocalDaytimeAvg",
    "VisibilityLocalDaytimeAvg",
    "WindSpeedLocalDaytimeAvg"]

#
valu_formatdateandtime = "%Y%m%d %H:%M:%S"

#
name_columndatetime = "dateandtime"
# name_columnbusiness = "business"
# name_columnmethod = "method"
# name_columnproducttype = "producttype"


# make list of dependent variables
list_variablesdependent_all = ["sales"]
list_variablesdependent = ["sales"]

# make lists of independent variables
list_variablesindependent_time = ["minute",
                                  "hour",
                                  "weekday",
                                  "day",
                                  "month",
                                  "quarter",
                                  "year"]

# make list of columns to "stratifyby" the data for stratification
list_columnsstratby = ["placeId"]

# make list of ohe (one hot encoding) variables
list_colstring_ohe = []

#
# TODO: further ponder the best implementation here (e.g., as if user had gui); for instance, perhaps
#     : keep all original independent except unselected variables in "weather" set or "ohe" set.
#
# TODO: compare models built using 'list_columnsweather_client' vs 'list_columnsweather_<some or all>'
list_colpick_weather = list_columnsweather_few

list_colpick_nonweather = list_variablesdependent + list_columnsstratby + list_colstring_ohe + list_variablesindependent_time + [
    "date"]

list_columnsother = list(set(list_colpick_nonweather) -
                         set(list_variablesdependent + list_columnsstratby + list_colstring_ohe + ["date"]))

# ......................................................................................................................
# CONFIGURATION FOR STEP 1.2: TRANSFORM DATA
# ......................................................................................................................

# make list of columns to "groupby" the data for aggregation
list_columnsgroupby = ["date", "placeId", "producttype"]

#
# todo: determine why "left" is not the chosen value --> why there are data anomalies (see above notes)
# todo: determine why the "EventDate" and "order_date" columns are not mismatch since people probably purchase
#     : tickets well before the event start date; determine if "sales" data has most apt correspondence
valu_howjoin = "inner"

#
dict_columnsdtypes_client = {
    "date": "str",
    "dateandtime": "str",
    "placeId": "str",
    "placeName": "str",
    "postalcode": "str",
    #     "state": "str",
    "countrycode": "str",
    "productname": "str",
    "producttype": "str",
    "discount": "float",
    "closed": "bool",
    "sales": "float"}

#
dict_columnsrename_client = {
}

#
# TODO: optionally redundantly explicitly include the weather variables in each dict object
dict_columnsdtypes_weather = {"date": "str", "postalcode": "str"}
dict_columnsrename_weather = {"date": "dateW", "postalcode": "postalcodeW"}

#
#
# note: Cannot access callable attribute 'mode' of 'SeriesGroupBy' objects, try using the 'apply' method
# note: this info needs correspondence to the planned derived variables
# todo: make this an abstract/generalizable process
# todo: make distinct count of applicable variables
#
dict_columnsagg_agg = {
    "placeName": "first",
    "postalcode": "first",
    "minute": "min",
    "hour": "min",
    "weekday": "first",
    "day": "first",
    "month": "first",
    "quarter": "first",
    "year": "first",
    "discount": "mean",
    "sales": "sum"}

#
dict_columnsrename_agg = {
}

#
dict_columnsdtypes_agg = {
    "placeName": "str",
    "postalcode": "str",
    "minute": "int",
    "hour": "int",
    "weekday": "int",
    "day": "int",
    "month": "int",
    "quarter": "int",
    "year": "int",
    "discount": "float",
    "sales": "float"}

# ......................................................................................................................
# CONFIGURATION FOR STEP 1.3: EXPLORE DATA
# ......................................................................................................................

#
list_columnscomboby = list(set(list_columnsgroupby) - {"date"})

# ......................................................................................................................
# CONFIGURATION FOR STEP 2.1: BUILD PREDICTIVE MODELS
# ......................................................................................................................

#
list_keepyears_build = [2016, 2017]
list_keepyears_apply = [2018]
list_keepyears_applyblind = [2018]

datestart_applymodelblind = "2018-01-02"
datestop_applymodelblind = "2018-12-31"

#
# list_thresholdsdvars = [10000]
list_thresholdsdvars = [np.inf]

#
# list_mla = [
#     KNeighborsRegressor(n_neighbors=5, weights="distance", algorithm="auto", leaf_size=30, p=2, metric="minkowski"),
#     SVR(kernel="linear", C=100, gamma="auto", epsilon=0.1),
#     SVR(kernel="rbf", C=100, gamma=0.1, epsilon=0.1),
#     GaussianProcessRegressor(1.0 * RBF(1.0)),
#     DecisionTreeRegressor(max_depth=5, max_features=20, criterion="mae"),
#     RandomForestRegressor(max_depth=5, n_estimators=10, max_features=None, criterion="mae"),
#     AdaBoostRegressor(),
#     MLPRegressor(alpha=1, max_iter=1000),
#     SGDRegressor(),
#     Lasso(alpha=0.1, max_iter=1000)]
#
list_mla = [
    SVR(kernel="linear", C=100, gamma="auto", epsilon=0.1),
    RandomForestRegressor(max_depth=5, n_estimators=3, max_features=20, criterion="mae")]

#
valu_adhocthreshold = 45  # todo: change to lower number for demo purposes and to higher number for full purposes
num_permutes = 10  # todo: change back to 100 or make multiple times > 10
num_cvrepeats = 5  # todo: change to higher number if compute power facilitates such
valu_rescaledata = False
valu_fractiontest = 0.25
valu_randomstate = 123
valu_metricpickbestmodel = "test_neg_median_absolute_error"
# list_cvmetrics = ["neg_mean_absolute_error", "neg_median_absolute_error", "max_error", "explained_variance", "r2"]
list_cvmetrics = ["neg_mean_absolute_error", "neg_median_absolute_error", "explained_variance", "r2"]

#
#     list_treebasedmla = ["DECISIONTREE", "EXTRATREE", "GRADIENTBOOSTING", "ISOLATIONFOREST", "RANDOMFOREST"]
list_treebasedmla = ["DECISIONTREE"]
list_mlagroup1 = ["LINEARSVR", "LINEARSVC", "SVR", "SVC", "NUSVR", "NUSVC", "ONECLASSSVM", "SGD", "LASSO"]
list_mlagroup2 = ["DECISIONTREE", "EXTRATREE", "ADABOOST", "GRADIENTBOOSTING", "RANDOMFOREST"]

#
#     num_jobs = int(multiprocessing.cpu_count() / 2.0) # todo: change to max (i.e., remove divisor)
num_jobs = 2

# ......................................................................................................................
# CONFIGURATION FOR STEP 2.2: SAVE PREDICTIVE MODELS
# ......................................................................................................................

# specify a name for the deployment workspace
space_name = "{}_{}".format(name_offering, name_client)

# specify the WML client credentials

wml_credentials = {
   "token": os.environ['USER_ACCESS_TOKEN'],
   "instance_id" : "openshift",
   "url": os.environ['RUNTIME_ENV_APSX_URL'],
   "version": "3.5"
}

# notify scientist: completed analyses
print("DONE: 'STEP 0.1b: Set Parameters' analysis")


# ----------------------------------------------------------------------------------------------------------------------
# MAKE FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------

#
# https://scikit-learn.org/stable/modules/classes.html#sklearn-metrics-metrics
# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html
# https://scikit-learn.org/stable/modules/model_evaluation.html#scoring

#
def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)

    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


#
def makemetrics_modelperf(y_act, y_pred):
    mae = mean_absolute_error(y_act, y_pred)
    mape = mean_absolute_percentage_error(y_act, y_pred)
    rms = math.sqrt(mean_squared_error(y_act, y_pred))
    mse = mean_squared_error(y_act, y_pred)
    vs = explained_variance_score(y_act, y_pred)
    r2 = r2_score(y_act, y_pred)

    return {
        'mae': mae,
        'mape': mape,
        'rms': rms,
        'mse': mse,
        'vs': vs,
        'r2': r2}


#
def tree_to_code(tree_fit, feature_names):
    tree_ = tree_fit.tree_
    feature_name = [feature_names[ii] if ii != _tree.TREE_UNDEFINED else "undefined!" for ii in tree_.feature]
    print("def tree({}):".format(", ".join(feature_names)))

    #
    def treerecurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            print("{}if {} <= {}:".format(indent, name, threshold))
            treerecurse(tree_.children_left[node], depth + 1)
            print("{}else:  # if {} > {}".format(indent, name, threshold))
            treerecurse(tree_.children_right[node], depth + 1)
        else:
            print("{}return {}".format(indent, tree_.value[node]))

    #
    treerecurse(0, 1)

    #
    return None


#
def derivevariables_time(df, columnname):
    #
    df["date"] = pd.to_datetime(df[columnname], format=valu_formatdateandtime).dt.date.astype("str")

    #
    df["minute"] = pd.to_datetime(df[columnname], format=valu_formatdateandtime).dt.minute.astype("int")
    df["hour"] = pd.to_datetime(df[columnname], format=valu_formatdateandtime).dt.hour.astype("int")

    #
    # df["time"] = df[columnname].apply(lambda v: str(v)[-8:]) # todo: determine aptness or/and a better solution
    # df["hourandminute"] = df["time"].str[:2] # todo: need lambda to pull both hour and minute as single value

    #
    df["weekday"] = pd.to_datetime(df[columnname], format=valu_formatdateandtime).dt.weekday.astype("int").apply(
        lambda v: 1 if (v == 6) else (v + 2))  # note: presumes sunday (value = 1) as 1st weekday

    #
    df["day"] = pd.to_datetime(df[columnname], format=valu_formatdateandtime).dt.day.astype("int")
    df["month"] = pd.to_datetime(df[columnname], format=valu_formatdateandtime).dt.month.astype("int")
    df["year"] = pd.to_datetime(df[columnname], format=valu_formatdateandtime).dt.year.astype("int")
    df["quarter"] = pd.to_datetime(df[columnname], format=valu_formatdateandtime).dt.quarter.astype("int")

    #
    return df


#
def mydfdescribe(xx):
    # todo: maybe later use https://aws.amazon.com/blogs/big-data/test-data-quality-at-scale-with-deequ/
    #     : recall that KJ wrote code for this but perhaps first use a simpler iteration of such concepts
    #
    # choose columnar quality metrics (e.g., nunique, isnan, dtype, min, max, kurtosis)
    list_dfconcatnames = [
        "dtypes",
        "nunique",
        "count",
        "percent_nan",
        "percent_blank",
        "percent_zero",
        "percent_negative",
        "min",
        "max",
        "kurtosis"]

    # compute columnar quality metrics (e.g., nunique, isnan, dtype, min, max, kurtosis)
    list_dfconcat = []

    for nn in list_dfconcatnames:

        #
        temp = []
        for ii in xx.columns:
            try:
                if "dtypes" == nn:
                    tempval = xx[ii].dtype
                elif "nunique" == nn:
                    tempval = xx[ii].nunique()
                elif "count" == nn:
                    tempval = xx[ii].count()
                elif "percent_nan" == nn:
                    tempval = 1 - xx[ii].count() / len(xx)
                elif "percent_blank" == nn:
                    tempval = xx.loc[xx[ii].apply(lambda v: str(v).replace(' ', '')) == '', ii].count() / len(xx)
                elif "percent_zero" == nn:
                    tempval = xx.loc[xx[ii] == 0, ii].count() / len(xx)
                elif "percent_negative" == nn:
                    tempval = xx.loc[xx[ii] < 0, ii].count() / len(xx)
                elif "min" == nn:
                    tempval = xx[ii].min(axis=0, skipna=True, numeric_only=False)
                elif "max" == nn:
                    tempval = xx[ii].max(axis=0, skipna=True, numeric_only=False)
                elif "kurtosis" == nn:
                    tempval = xx[ii].kurtosis(axis=0, skipna=True, numeric_only=False)
                else:
                    tempval = None
            except TypeError:
                if "min" in nn:
                    tempval = min(xx[ii][~pd.isnull(xx[ii])].astype("str").values)
                elif "max" in nn:
                    tempval = max(xx[ii][~pd.isnull(xx[ii])].astype("str").values)
                else:
                    tempval = None
            finally:
                temp.append(tempval)

        list_dfconcat.append(pd.DataFrame({nn: temp}, index=xx.columns))

    #
    return pd.concat(list_dfconcat, axis=1)


# DEFINE "MAKE STRATIFIED DATASETS" FUNCTION
def makedatastrata(df, type_dataset, list_keepyears):
    # ...........................................................................................................
    # TODO: MAYBE MAKE THIS A SEPARATE FUNCTION???
    # ...........................................................................................................

    # filter certain variables
    # note: this computation must have occurrence before the 'ohe' process, which can drop the filtered columns
    # TODO: THIS LINE IS STILL A HARDCODED SOLUTION THAT NEEDS MORE APT ABSTRACTION LATER LORD WILLING
    # dfM = df.loc[(df["sales"] > 0) & (df["venue_id"] > 0), :]
    # dfM = df.loc[:, sorted(df.columns.to_list())]
    # dfM = df.loc[~df["producttypeName"].isin(["nan", "unknown", "vendor"]), :]
    dfM = df.copy()

    # select certain variables
    dfM = dfM.loc[:, list_colpick_weather + list_colpick_nonweather]

    #
    # note: this computation must have occurrence after 'select certain variables' and before 'ohe' processes
    # note: some categorical variables may have numerical dtype but lack "ordinal scale" interpretation
    # list_colall_original = dfM.columns.to_list()
    list_ivariables_num = list(set(dfM._get_numeric_data().columns.tolist()) -
                               set(list_variablesdependent + list_columnsstratby + list_colstring_ohe))
    # list_colstr_original = list(set(list_colall) - set(list_colnumeric))

    # transform categorical variables
    # NOTE: apparently there is not a parameter that permits retention of pre-transformed variables
    temp = dfM.loc[:, list_colstring_ohe].reset_index()
    dfM = pd.get_dummies(dfM, columns=list_colstring_ohe, prefix=list_colstring_ohe, prefix_sep='_', dummy_na=False)
    dfM = pd.concat([dfM.reset_index(), temp], axis=1, ignore_index=False).drop(columns=["index"])

    # create a "dataset group" column
    dfM["group"] = list(zip(*[dfM.loc[:, ii] for ii in list_columnsstratby]))

    # create a "dataset ohe columns" column
    dfM["columns_ohe"] = pd.Series(list(zip(*[dfM.loc[:, ii] for ii in list_colstring_ohe])))

    # # drop certain variables
    # df = df.drop(columns=list_columnsdrop, inplace=False, errors="ignore")

    #
    print("dataset size ({}): {}".format("dfM", dfM.shape))
    display(dfM)

    # ...........................................................................................................
    # TODO: MAYBE MAKE THIS A SEPARATE FUNCTION???
    # ...........................................................................................................

    #
    list_columnsstratby_distinctvals = [df.loc[:, ii].unique().tolist() for ii in list_columnsstratby]
    list_loop = list(itertools.product(*list_columnsstratby_distinctvals))

    #
    datastrata = []

    # compute datasets
    for ii, ii_threshold in zip(list_variablesdependent, list_thresholdsdvars):

        #
        valu_thresh = ii_threshold
        name_dvar = ii
        print("dependent variable (aka criterion variable): {}".format(ii.upper()))
        print("dependent variable has existence in the data: {}".format(name_dvar in dfM.columns.tolist()))

        #
        list_columnsdropnow = ["group", "year", "columns_ohe"] + list_columnsstratby + list_colstring_ohe + list(
            set(list_variablesdependent) - {name_dvar})

        #
        for jj in list_loop:
            #
            name_dataset = "{}_{}_{}".format(name_client, type_dataset, str(jj)).lower()

            # select certain rows
            # note: yet does not address "np.nan" values in "name_dvar" column for "valu_thresh" value
            bool_pickrows = (
                    (dfM["year"].isin(list_keepyears)) & \
                    (dfM["group"] == jj) & \
                    (dfM[name_dvar] < valu_thresh))

            dfpick = dfM.loc[bool_pickrows, :]

            #
            tpick = dfpick.pop("date")
            qpick = dfpick.pop("columns_ohe")
            ypick = dfpick.pop(name_dvar)
            Xpick = dfpick.drop(columns=list_columnsdropnow, inplace=False, errors="ignore")

            #
            dict_datasetnow = {"name_data": name_dataset,
                               "q": qpick,
                               "X": Xpick,
                               "y": ypick,
                               "variables_independent_num": list_ivariables_num,
                               "date": tpick}

            datastrata.append(dict_datasetnow)

            #
            print("dataset: {}; sample size: {}".format(name_dataset, len(ypick)))

    #
    return datastrata


#
def makemodels(datastrata, list_mla):
    # ..................................................................................................................
    #
    # ..................................................................................................................

    # todo: change plot to either (a) always plot the criterion (dependent variable) versus the predictors (i.e., either an
    #     : arbitrary variable or one corresponding to the largest explained info if not the transformed variable itself) or
    #     : (b) plot the criterion values as a color overlay on the 2d space of the two most "informative" variables via a
    #     : transformation algorithm (e.g., t-SNE, PCA, ICA) or just two adhoc variables perhaps
    #     :
    #     : https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding
    #     : https://en.wikipedia.org/wiki/Independent_component_analysis
    #     : https://en.wikipedia.org/wiki/Principal_component_analysis

    # #
    # figure = plt.figure(figsize=(27, 9))
    # ii = 1
    # h = .02  # step size in the mesh
    # cm = plt.cm.RdBu
    # cm_bright = ListedColormap(['#FF0000', '#0000FF'])

    #
    results_modelbuild = []

    # iterate over datasets
    for ds_cnt, datasetnow in enumerate(datastrata):

        # get dataset
        g = datasetnow["name_data"]
        #         q = datasetnow["q"]
        X = datasetnow["X"]
        y = datasetnow["y"]
        list_ivariables_num = datasetnow["variables_independent_num"]
        #         t = datasetnow["date"]

        #
        n = len(y)
        print("\rsample size of group {}: {}\n".format(g, n))
        if n < valu_adhocthreshold:
            print("skipped")
            continue

        # get column (variable) names
        # note: must preserve list order for the below "variables importance" analysis
        name_dvariable = y.name
        list_ivariables = X.columns.to_list()  # note: includes transformed categorical variables
        list_ivariables_str = list(set(list_ivariables) - set(list_ivariables_num))  # note: see 1-above note
        print("dependent variable (aka criterion variable): {}".format(name_dvariable.upper()))

        # get column (variable) values then optionally transform numerical independent variables
        y = y.values
        if valu_rescaledata == True:
            list_ivariables = list_ivariables_num + list_ivariables_str  # note: align with concat...
            datascaler = RobustScaler().fit(X.loc[:, list_ivariables_num])
            X1 = datascaler.transform(X.loc[:, list_ivariables_num])
            X2 = X.loc[:, list_ivariables_str]
            X = np.concatenate((X1, X2), axis=1)
        else:
            datascaler = None
            X = X.values

        # replace missing (e.g., nan) or/and invalid (e.g., infinite) values
        # todo: determine if a need of other imputation conditions or/and techniques
        print("any nan:", np.any(np.isnan(X)), "; ", "all finite:", np.all(np.isfinite(X)))
        X[np.isnan(X)] = -1
        X[~np.isfinite(X)] = -2
        print("any nan:", np.any(np.isnan(X)), "; ", "all finite:", np.all(np.isfinite(X)))

        # split dataset (i.e., compute training data and testing data) for "internal" model validation
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=valu_randomstate)

        # ..................................................................................................................
        # just plot the dataset first
        # ..................................................................................................................

        # #
        # x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
        # # y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
        # y_min, y_max = y.min() - .5, y.max() + .5
        # xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
        #                      np.arange(y_min, y_max, h))
        #
        # #
        # ax = plt.subplot(len(datastrata), len(regressors) + 1, ii)
        #
        # # Plot the training points
        # # ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright, edgecolors='k')
        # ax.scatter(X_train[:, 0], y_train, c=y_train, cmap=cm_bright, edgecolors='k')
        #
        # # Plot the testing points
        # # ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright, alpha=0.6, edgecolors='k')
        # ax.scatter(X_test[:, 0], y_test, c=y_test, cmap=cm_bright, alpha=0.6, edgecolors='k')
        #
        # #
        # ax.set_xlim(xx.min(), xx.max())
        # ax.set_ylim(yy.min(), yy.max())
        # ax.set_xticks(())
        # ax.set_yticks(())
        # if ds_cnt == 0:
        #     ax.set_title("Input data")
        #
        # #
        # ii += 1

        # ..................................................................................................................
        #
        # ..................................................................................................................

        # iterate over machine-learning algorithms
        for mla in list_mla:

            #
            dict_results = {}

            #
            name_mla = type(mla).__name__.upper().replace("REGRESSOR", "").replace("CLASSIFIER", "")
            print("\rmla: {}\n".format(name_mla))

            # compute estimated model "internal" performance via cross-validation results
            ttic = time.time()
            dict_cvresults = cross_validate(mla, X_test, y_test, cv=num_cvrepeats,
                                            scoring=list_cvmetrics, return_estimator=True, return_train_score=True)
            ttoc = time.time()
            print(dict_cvresults)
            print("elapsed time of model in-validation:", ttoc - ttic)

            # compute variable importances
            # notes: if a need then use https://en.wikipedia.org/wiki/Softmax_function
            dict_cvresults["variables_importances"] = []

            for rr in range(0, num_cvrepeats):

                # get model
                modelnowrr = dict_cvresults["estimator"][rr]

                # compute "model variables" coefficients
                #
                # note: this is easier implementation if scikitlearn has ".coef_" for all such arrays and algorithms
                #
                # note: I tried a "softmax" on "mlagroup2" methods for consistency but it yielded much lower values;
                #     : I yet should more study its math juxtaposed to "tree-based variables coefficients" math.
                #
                if name_mla in list_mlagroup1:
                    # note: not all algorithms yield coefficients
                    try:
                        arr_varcoef = np.array(modelnowrr.coef_.flatten("C").tolist())
                        arr_varcoef = softmax(arr_varcoef / np.linalg.norm(arr_varcoef, 1))
                        # arr_varcoef = softmax(np.array(modelnowrr.coef_.flatten("C").tolist()))
                    except Exception as badtry:
                        arr_varcoef = np.array([np.nan] * X.shape[1])
                        print(badtry)

                elif name_mla in list_mlagroup2:
                    # arr_varcoef = np.array(modelnowrr.feature_importances_.flatten("C").tolist())
                    # arr_varcoef = softmax(arr_varcoef / np.linalg.norm(arr_varcoef, 1))
                    #                 arr_varcoef = softmax(np.array(modelnowrr.feature_importances_.flatten("C").tolist()))
                    arr_varcoef = np.array(modelnowrr.feature_importances_.flatten("C").tolist())
                else:
                    arr_varcoef = np.array([np.nan] * X.shape[1])

                # compute ranked important variables (features)
                #
                # notes: maybe get only variables with coef magnitudes > threshold (besides zero)
                #      : however, this decision introduces "subjective objectivity" via the threshold choice
                #
                # todo: determine if variables with zero importance actually have presence in the model equation
                list_riv = sorted(zip(list_ivariables, arr_varcoef.tolist()), reverse=True, key=lambda x: np.abs(x[1]))
                list_riv = list(filter(lambda v: np.abs(v[1]) > 0, list_riv))  # TODO: LATER IGNORE THIS LINE?
                dict_cvresults["variables_importances"].append(list_riv)
                print("\rimportant variables (cv result {}): {}\n".format(rr, list_riv))

                # compute tree-based model as code (and consequently printable rules): each model
                # todo: implement solution for adaboost if using a tree-based algorithm
                if name_mla in list_treebasedmla:
                    print("\reach model decision rules: ...\n")
                    tree_to_code(modelnowrr, list_ivariables)

            # choose a "best" model
            # https://scikit-learn.org/stable/modules/model_evaluation.html
            # https://www.geeksforgeeks.org/python-split-dictionary-of-lists-to-list-of-dictionaries/
            list_cvresults = [dict(zip(dict_cvresults, ii)) for ii in zip(*dict_cvresults.values())]
            cvresults_modelbestindex = np.argmax(dict_cvresults[valu_metricpickbestmodel], axis=0)
            cvresults_modelbest = list_cvresults[cvresults_modelbestindex]
            cvresults_modelbestscore = np.abs(list_cvresults[cvresults_modelbestindex][valu_metricpickbestmodel])
            print("\rbest model score (abs(max({}))): {}\n".format(valu_metricpickbestmodel, cvresults_modelbestscore))
            print("\rbest model important variables: {}\n".format(cvresults_modelbest["variables_importances"]))

            # compute tree-based model as code (and consequently printable rules): best model
            # todo: implement solution for adaboost if using a tree-based algorithm
            if name_mla in list_treebasedmla:
                print("\rbest model decision rules: ...\n")
                tree_to_code(cvresults_modelbest["estimator"], list_ivariables)

            # store "model build" validation results
            dict_results["name_data"] = g
            dict_results["variables_independent"] = list_ivariables
            dict_results["variable_dependent"] = name_dvariable
            dict_results["datascaler"] = datascaler
            dict_results["name_mla"] = name_mla
            dict_results["cvresults_models"] = list_cvresults
            dict_results["cvresults_modelbest"] = cvresults_modelbest
            dict_results["cvresults_modelbestscore"] = cvresults_modelbestscore
            dict_results["cvresults_modelbestindex"] = cvresults_modelbestindex
            results_modelbuild.append(dict_results)

            # ..............................................................................................................
            # make more plots
            # ..............................................................................................................

            # #
            # ax = plt.subplot(len(datastrata), len(regressors) + 1, ii)
            #
            # # todo: make something usefully relevant for regression analyses if a possible sensibility
            # # # Plot the decision boundary. For that, we will assign a color to each
            # # # point in the mesh [x_min, x_max]x[y_min, y_max].
            # # if hasattr(mla, "decision_function"):
            # #     Z = mla.decision_function(np.c_[xx.ravel(), yy.ravel()])
            # # else:
            # #     Z = mla.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
            #
            # # todo: make something usefully relevant for regression analyses if a possible sensibility
            # # # Put the result into a color plot
            # # Z = Z.reshape(xx.shape)
            # # ax.contourf(xx, yy, Z, cmap=cm, alpha=.8)
            #
            # # Plot the training points
            # # ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright, edgecolors='k')
            # ax.scatter(X_train[:, 0], y_train, c=y_train, cmap=cm_bright, edgecolors='k')
            #
            # # Plot the testing points
            # # ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright, edgecolors='k', alpha=0.6)
            # ax.scatter(X_test[:, 0], y_test, c=y_test, cmap=cm_bright, edgecolors='k', alpha=0.6)
            #
            # #
            # ax.set_xlim(xx.min(), xx.max())
            # ax.set_ylim(yy.min(), yy.max())
            # ax.set_xticks(())
            # ax.set_yticks(())
            # if ds_cnt == 0:
            #     ax.set_title(name)
            # ax.text(xx.max() - .3, yy.min() + .3, ('%.2f' % cvscores_med).lstrip('0'),
            #         size=15, horizontalalignment='right')
            #
            # #
            # ii += 1

    # #
    # plt.tight_layout()
    # plt.show()

    # notify scientist: completed analyses
    print("DONE: MAKEMODELS!")

    # return main result
    return results_modelbuild


#
def evalmodels_build(datastrata, results_modelbuild):
    #
    valu_metricpickbestmodel_rename = valu_metricpickbestmodel.replace("test_", "").replace("train_", "")

    # initialize "results storage" output
    list_results = []

    #
    for resultsnow in results_modelbuild:

        #
        modeldatanow = resultsnow["name_data"]
        modelivarnow = resultsnow["variables_independent"]
        modeldvarnow = resultsnow["variable_dependent"]
        modelnamenow = resultsnow["name_mla"]
        modelnow = resultsnow["cvresults_modelbest"]["estimator"]
        modelscorenow = np.abs(resultsnow["cvresults_modelbest"][valu_metricpickbestmodel])
        datasetnow = datastrata[[ii["name_data"] for ii in datastrata].index(modeldatanow)]
        datascalernow = resultsnow["datascaler"]

        #
        #         print(datasetnow, modeldatanow, modeldvarnow, modelnamenow, modelscorenow)
        print(modeldatanow, modeldvarnow, modelnamenow, modelscorenow)

        # ..................................................................................................................
        # compute "variables importance" plot
        # ..................................................................................................................

        #
        # https://stackoverflow.com/questions/7558908/unpacking-a-list-tuple-of-pairs-into-two-lists-tuples
        try:  # TODO: REVERT LATER
            list_variables, list_variablescoef = zip(*resultsnow["cvresults_modelbest"]["variables_importances"])
        except Exception as badtry:
            print(badtry)
        else:
            f, ax = plt.subplots(figsize=(15, 100))
            sns.barplot(x=list(list_variablescoef), y=list(list_variables), orient="h")
            ax.set_xlim(0.0, 1.0)
            ax.set_xlabel("IMPORTANCE OF VARIABLE: PREDICT " + modeldvarnow.upper())
            ax.set_title(modelnamenow)
            plt.tight_layout()
            plt.show()

        # ..................................................................................................................
        # compute "tree-based machine-learning algorithm tree" plot (todo: implement for more than decision tree)
        # ..................................................................................................................

        #
        if modelnamenow in list_treebasedmla:

            #
            if modelnow.max_depth <= 6:

                #
                dot_file = export_graphviz(modelnow, out_file='model.dot', feature_names=modelivarnow)
                get_ipython().system('dot -Tpng model.dot -o model.png -Gdpi=600')
                Image(filename='model.png')

            else:

                #
                print("I had issue making the image for tree depth > 6; but perhaps try the pydotplus approach.")

        # ..................................................................................................................
        # compute dataset
        # ..................................................................................................................

        # get dataset
        datanamenow = datasetnow["name_data"]
        q = datasetnow["q"]
        X = datasetnow["X"]
        y = datasetnow["y"]
        list_ivariables_num = datasetnow["variables_independent_num"]
        t = datasetnow["date"]

        # get column (variable) names
        # note: must preserve list order for the below "variables importance" analysis
        name_dvariable = y.name
        list_ivariables = X.columns.to_list()  # note: includes transformed categorical variables
        list_ivariables_str = list(set(list_ivariables) - set(list_ivariables_num))  # note: see 1-above note
        #         print("dependent variable (aka criterion variable): {}".format(name_dvariable.upper()))

        # get column (variable) values then optionally transform numerical independent variables
        t = t.values
        y = y.values
        if valu_rescaledata == True:
            list_ivariables = list_ivariables_num + list_ivariables_str  # note: align with concat...
            #             X1 = RobustScaler().fit_transform(X.loc[:, list_ivariables_num])
            X1 = datascalernow.transform(X.loc[:, list_ivariables_num])
            X2 = X.loc[:, list_ivariables_str]
            X = np.concatenate((X1, X2), axis=1)
        else:
            X = X.values

        # replace missing (e.g., nan) or/and invalid (e.g., infinite) values
        # todo: determine if a need of other imputation conditions or/and techniques
        print("any nan:", np.any(np.isnan(X)), "; ", "all finite:", np.all(np.isfinite(X)))
        X[np.isnan(X)] = -1
        X[~np.isfinite(X)] = -2
        print("any nan:", np.any(np.isnan(X)), "; ", "all finite:", np.all(np.isfinite(X)))

        # split dataset (i.e., compute training data and testing data) for "internal" model validation
        X_train, X_test, y_train, y_test, t_train, t_test = train_test_split(X, y, t,
                                                                             test_size=valu_fractiontest,
                                                                             random_state=valu_randomstate)

        # ..................................................................................................................
        # compute performance metrics
        # ..................................................................................................................

        # compute performance metrics
        predperf = makemetrics_modelperf(y_test, modelnow.predict(X_test))
        print("prediction performance metrics: ", predperf)

        # ..................................................................................................................
        # compute "crossvalidated predictions" output
        # ..................................................................................................................

        #
        y_pred = cross_val_predict(modelnow, X_test, y_test, cv=num_cvrepeats)
        #         y_pred_mean = np.mean(y_pred)
        #         y_pred_sem = np.std(y_pred, ddof=1) / math.sqrt(len(y_pred))
        xbar = np.array(range(0, len(y_test)), dtype="float")

        # ..................................................................................................................
        # update "results storage" output
        # ..................................................................................................................

        #
        list_results.append({"name_data": datanamenow,
                             "variables_independent": modelivarnow,
                             "variable_dependent": modeldvarnow,
                             "name_mla": modelnamenow,
                             "q": q, "t": t_test, "y": y_test, "ypred": y_pred, "metrics": predperf})

        # widthbar = 0.30

        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # plotbar1 = ax.bar(xbar, y_test, widthbar, color='black', yerr=0.0)
        # plotbar2 = ax.bar(xbar, y_pred, widthbar, color='gray', yerr=y_pred_sem)

        # # add some
        # ax.set_ylabel('Scores')
        # ax.set_title('Scores by group and gender')
        # ax.set_xticks(xbar + widthbar / 2)
        # # ax.set_xticklabels( ('G1', 'G2', 'G3', 'G4', 'G5') )
        # ax.legend((plotbar1[0], plotbar2[0]), ("Truth", "Prediction") )
        # plt.show()

        # ..................................................................................................................
        # compute "crossvalidated predictions" plot: scatter plot
        # ..................................................................................................................

        fig, ax = plt.subplots()
        ax.scatter(y_test, y_pred, edgecolors=(0, 0, 0))
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
        ax.set_xlabel("OBSERVED " + modeldvarnow.upper())
        ax.set_ylabel("PREDICTED " + modeldvarnow.upper())
        ax.set_title(modelnamenow)
        plt.show()

        # ..................................................................................................................
        # compute "crossvalidated predictions" plot: index-series plot
        # ..................................................................................................................

        #
        # NOTE: this plot cannot manage multiple stratifications (i.e., predictions across category combos)
        # TODO: add %change values as separate "line" on the same axes
        fig, ax = plt.subplots()
        ax.plot(xbar, y_test, "k*", lw=4, label="OBSERVED")
        ax.plot(xbar, y_pred, "b.", lw=4, label="PREDICTED")
        #         ax.errorbar(xbar, y_pred, yerr=y_pred_sem, fmt="b.", lw=1, label="PREDICTED") # TODO: try this later
        ax.set_xlabel("INDEX")
        ax.set_ylabel(modeldvarnow.upper())
        ax.set_title(modelnamenow)
        ax.legend()
        plt.show()

        #         #
        #         time.sleep(3)

        # ..................................................................................................................
        # compute "permutation test" plot
        # ..................................................................................................................

        #
        num_luckvalues = np.unique(y_test).size
        score_luck = 1.0 / num_luckvalues
        #         print("score luck: ", score_luck)

        #
        score, permutation_scores, pvalue = permutation_test_score(modelnow, X_test, y_test,
                                                                   scoring=valu_metricpickbestmodel_rename,
                                                                   cv=num_cvrepeats, n_permutations=num_permutes,
                                                                   n_jobs=num_jobs)

        print("permuted {}: {} (p = {}, n = {})".format(valu_metricpickbestmodel_rename,
                                                        score, pvalue, num_permutes))

        # make "permutation scores" histogram
        fig, ax = plt.subplots()
        plt.hist(permutation_scores, int(math.sqrt(num_permutes)), label="PERMUTED", edgecolor='black')
        ylim = plt.ylim()
        # BUG: vlines(..., linestyle='--') fails on older versions of matplotlib
        # plt.vlines(score, ylim[0], ylim[1], linestyle='--',
        #          color='g', linewidth=3, label='Classification Score'
        #          ' (pvalue %s)' % pvalue)
        # plt.vlines(1.0 / n_classes, ylim[0], ylim[1], linestyle='--',
        #          color='k', linewidth=3, label='Luck')
        plt.plot(2 * [score], ylim, '--g', linewidth=3, label="PREDICTED (p = {})".format(pvalue))
        #         plt.plot(2 * [score_luck], ylim, '--k', linewidth=3, label="LUCK")
        plt.ylim(ylim)
        plt.ylabel("COUNT")
        plt.xlabel(valu_metricpickbestmodel_rename.upper())
        ax.set_title(modelnamenow)
        plt.legend()
        plt.show()

        # ..................................................................................................................
        # implement this later, Lord Willing
        # ..................................................................................................................

        # https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.learning_curve.html#sklearn.model_selection.learning_curve

    # notify scientist: completed analyses
    print("DONE: EVALMODELS_BUILD!")

    #
    return list_results


#
# TODO: FIX CODE TO ORIGINAL SOLUTION THAT LOOPS BY DATASET RATHER THAN MODEL RESULT TO HANDLE VARIANTS OF THE
#     : SAME DATASET WITH SAME PREFIX (E.G., "REAL" VS "FAUX" DATA INSTANCES)
def evalmodels_apply(datastrata, results_modelbuild):
    #
    list_results = []

    #
    for resultsnow in results_modelbuild:

        #
        modeldatanow = resultsnow["name_data"]
        modelivarnow = resultsnow["variables_independent"]
        modeldvarnow = resultsnow["variable_dependent"]
        modelnamenow = resultsnow["name_mla"]
        modelnow = resultsnow["cvresults_modelbest"]["estimator"]
        modelscorenow = np.abs(resultsnow["cvresults_modelbest"][valu_metricpickbestmodel])
        datascalernow = resultsnow["datascaler"]

        #
        templist = [ii["name_data"].replace("_real", "").replace("_faux", "") for ii in datastrata]
        datasetnow = datastrata[templist.index(modeldatanow.replace("_real", "").replace("_faux", ""))]

        #
        # print(datasetnow, modeldatanow, modeldvarnow, modelnamenow, modelscorenow)
        print(modeldatanow, modeldvarnow, modelnamenow, modelscorenow)

        # ..................................................................................................................
        # compute dataset
        # ..................................................................................................................

        # get dataset
        datanamenow = datasetnow["name_data"]
        q = datasetnow["q"]
        X = datasetnow["X"]
        y = datasetnow["y"]
        list_ivariables_num = datasetnow["variables_independent_num"]
        t = datasetnow["date"]

        # get column (variable) names
        # note: must preserve list order for the below "variables importance" analysis
        name_dvariable = y.name
        list_ivariables = X.columns.to_list()  # note: includes transformed categorical variables
        list_ivariables_str = list(set(list_ivariables) - set(list_ivariables_num))  # note: see 1-above note
        #         print("dependent variable (aka criterion variable): {}".format(name_dvariable.upper()))

        # get column (variable) values then optionally transform numerical independent variables
        y = y.values
        if valu_rescaledata == True:
            list_ivariables = list_ivariables_num + list_ivariables_str  # note: align with concat...
            # X1 = RobustScaler().fit_transform(X.loc[:, list_ivariables_num])
            X1 = datascalernow.transform(X.loc[:, list_ivariables_num])
            X2 = X.loc[:, list_ivariables_str]
            X = np.concatenate((X1, X2), axis=1)
        else:
            X = X.values

        # replace missing (e.g., nan) or/and invalid (e.g., infinite) values
        # todo: determine if a need of other imputation conditions or/and techniques
        print("any nan:", np.any(np.isnan(X)), "; ", "all finite:", np.all(np.isfinite(X)))
        X[np.isnan(X)] = -1
        X[~np.isfinite(X)] = -2
        print("any nan:", np.any(np.isnan(X)), "; ", "all finite:", np.all(np.isfinite(X)))

        # ..................................................................................................................
        # compute performance metrics
        # ..................................................................................................................

        # compute performance metrics
        # TODO: maybe use the "mae" value from this in errorbar plot
        predperf = makemetrics_modelperf(y, modelnow.predict(X))
        print("prediction performance metrics: ", predperf)

        # ..................................................................................................................
        # compute "crossvalidated predictions" output
        # ..................................................................................................................

        #
        y_pred = cross_val_predict(modelnow, X, y, cv=num_cvrepeats)
        #         y_pred_mean = np.mean(y_pred)  # TODO: implement this in more correct way
        #         y_pred_sem = np.std(y_pred, ddof=1) / math.sqrt(len(y_pred)) # TODO: implement this in more correct way
        xbar = np.array(range(0, len(y)), dtype="float")

        # ..................................................................................................................
        # update "results storage" output
        # ..................................................................................................................

        #
        list_results.append({"name_data": datanamenow,
                             "variables_independent": modelivarnow,
                             "variable_dependent": modeldvarnow,
                             "name_mla": modelnamenow,
                             "q": q, "t": t, "y": y, "ypred": y_pred, "metrics": predperf})

        continue

        # ..................................................................................................................
        # compute "crossvalidated predictions" plot: scatter plot
        # ..................................................................................................................

        fig, ax = plt.subplots()
        ax.scatter(y, y_pred, edgecolors=(0, 0, 0))
        ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
        ax.set_xlabel("OBSERVED " + modeldvarnow.upper())
        ax.set_ylabel("PREDICTED " + modeldvarnow.upper())
        ax.set_title(modelnamenow)
        plt.show()

        # ..................................................................................................................
        # compute "crossvalidated predictions" plot: index-series plot
        # ..................................................................................................................

        #
        # NOTE: this plot cannot manage multiple stratifications (i.e., predictions across category combos)
        # TODO: add %change values as separate "line" on the same axes
        fig, ax = plt.subplots()
        ax.plot(xbar, y, "k*", lw=4, label="OBSERVED")
        ax.plot(xbar, y_pred, "b.", lw=4, label="PREDICTED")
        #         ax.errorbar(xbar, y_pred, yerr=y_pred_sem, fmt="b.", lw=1, label="PREDICTED") # TODO: try this later
        ax.set_xlabel("INDEX")
        ax.set_ylabel(modeldvarnow.upper())
        ax.set_title(modelnamenow)
        ax.legend()
        plt.show()

    #         #
    #         time.sleep(3)

    # notify scientist: completed analyses
    print("DONE: EVALMODELS_APPLY!")

    #
    return list_results


#
# TODO: FIX CODE TO ORIGINAL SOLUTION THAT LOOPS BY DATASET RATHER THAN MODEL RESULT TO HANDLE VARIANTS OF THE
#     : SAME DATASET WITH SAME PREFIX (E.G., "REAL" VS "FAUX" DATA INSTANCES)
def evalmodels_applyblind(datastrata, results_modelbuild):
    #
    list_results = []

    #
    for resultsnow in results_modelbuild:

        #
        modeldatanow = resultsnow["name_data"]
        modelivarnow = resultsnow["variables_independent"]
        modeldvarnow = resultsnow["variable_dependent"]
        modelnamenow = resultsnow["name_mla"]
        modelnow = resultsnow["cvresults_modelbest"]["estimator"]
        modelscorenow = np.abs(resultsnow["cvresults_modelbest"][valu_metricpickbestmodel])
        datascalernow = resultsnow["datascaler"]

        #
        templist = [ii["name_data"].replace("_real", "").replace("_faux", "") for ii in datastrata]
        datasetnow = datastrata[templist.index(modeldatanow.replace("_real", "").replace("_faux", ""))]

        #
        # print(datasetnow, modeldatanow, modeldvarnow, modelnamenow, modelscorenow)
        print(modeldatanow, modeldvarnow, modelnamenow, modelscorenow)

        # ..................................................................................................................
        # compute dataset
        # ..................................................................................................................

        # get dataset
        datanamenow = datasetnow["name_data"]
        q = datasetnow["q"]
        X = datasetnow["X"]
        list_ivariables_num = datasetnow["variables_independent_num"]
        t = datasetnow["date"]

        # get column (variable) names
        # note: must preserve list order for the below "variables importance" analysis
        list_ivariables = X.columns.to_list()  # note: includes transformed categorical variables
        list_ivariables_str = list(set(list_ivariables) - set(list_ivariables_num))  # note: see 1-above note
        #         print("dependent variable (aka criterion variable): {}".format(modeldvarnow.upper()))

        # get column (variable) values then optionally transform numerical independent variables
        y = np.full(shape=(len(X), 1), fill_value=np.nan, dtype=np.double)
        if valu_rescaledata == True:
            list_ivariables = list_ivariables_num + list_ivariables_str  # note: align with concat...
            # X1 = RobustScaler().fit_transform(X.loc[:, list_ivariables_num])
            X1 = datascalernow.transform(X.loc[:, list_ivariables_num])
            X2 = X.loc[:, list_ivariables_str]
            X = np.concatenate((X1, X2), axis=1)
        else:
            X = X.values

        # replace missing (e.g., nan) or/and invalid (e.g., infinite) values
        # todo: determine if a need of other imputation conditions or/and techniques
        print("any nan:", np.any(np.isnan(X)), "; ", "all finite:", np.all(np.isfinite(X)))
        X[np.isnan(X)] = -1
        X[~np.isfinite(X)] = -2
        print("any nan:", np.any(np.isnan(X)), "; ", "all finite:", np.all(np.isfinite(X)))

        # ..................................................................................................................
        # compute "estimated predictions" output
        # ..................................................................................................................

        #
        print(X.shape, len(list_ivariables_num))
        y_pred = modelnow.predict(X)

        # ..................................................................................................................
        # update "results storage" output
        # ..................................................................................................................

        #
        list_results.append({"name_data": datanamenow,
                             "variables_independent": modelivarnow,
                             "variable_dependent": modeldvarnow,
                             "name_mla": modelnamenow,
                             "q": q, "t": t, "y": y, "ypred": y_pred, "metrics": None})

    # notify scientist: completed analyses
    print("DONE: EVALMODELS_APPLYBLIND!")

    #
    return list_results


# DEFINE "MAKE TABULATED PREDICTIONS" FUNCTION
def maketable_predictions(results_predictions):
    # note: need this to avoid possible error (e.g., code does not recognize nan values)
    from numpy import nan

    #
    dict_columnsrename_apply1 = {}

    #
    list_columnsfinalsort = ["client", "datatype", "namedepvar",
                             "namemodel"] + list_columnsstratby + list_colstring_ohe + ["date", "ytrue", "ypred"]

    #
    dict_data = {}

    dict_data1 = {
        "client": [],
        "datatype": [],
        "namedepvar": [],
        "namemodel": []}

    dict_data2 = {}
    for ii in list_columnsstratby:
        dict_data2[ii] = []

    dict_data3 = {
        "q": [],
        "date": [],
        "ytrue": [],
        "ypred": []}

    dict_data.update(dict_data1)
    dict_data.update(dict_data2)
    dict_data.update(dict_data3)

    #
    dict_columnsastype_apply1 = {}
    for ii in list(dict_data.keys()):
        if ii in ["ytrue", "ypred"]:
            dict_columnsastype_apply1[ii] = "float"
        else:
            dict_columnsastype_apply1[ii] = "str"

    #
    for ii in results_predictions:

        #
        nvals = len(list(ii["y"]))

        #
        temp = ii["name_data"].replace("(", "").replace(")", "").replace("'", "").replace(" ", "").replace("_", ",")
        if len(list_columnsstratby) == 1:
            list_valsnamedata = temp[:-1].split(",")
        else:
            list_valsnamedata = temp.split(",")

        #
        dict_data["client"].extend([list_valsnamedata[0]] * nvals)
        dict_data["datatype"].extend([list_valsnamedata[1]] * nvals)
        dict_data["namedepvar"].extend([ii["variable_dependent"]] * nvals)
        dict_data["namemodel"].extend([ii["name_mla"]] * nvals)

        for kk, jj in enumerate(list_columnsstratby):
            dict_data[jj].extend([list_valsnamedata[(kk + 2)]] * nvals)

        dict_data["q"].extend(list(ii["q"]))
        dict_data["date"].extend(list(ii["t"]))
        dict_data["ytrue"].extend(list(ii["y"]))
        dict_data["ypred"].extend(list(ii["ypred"]))

    # compute dataframe
    dfT = pd.DataFrame(data=dict_data).astype(dict_columnsastype_apply1). \
        rename(columns=dict_columnsrename_apply1, inplace=False)

    if list_colstring_ohe:
        dfT[list_colstring_ohe] = pd.DataFrame([ast.literal_eval(vv) for vv in dfT["q"]], index=dfT.index)

    dfT = dfT.drop(columns=["q"], inplace=False, errors="ignore").loc[:, list_columnsfinalsort]

    #
    return dfT


# notify scientist: completed analyses
print("DONE: 'STEP 0.1c: Define Custom Functions' analysis")
