#!/usr/bin/env python
# coding: utf-8

# ### CONFIGURATION: Import Software Packages, Set Parameters, and Define Custom Functions
#
# This file configures the analyses to build, store, deploy, and apply machine-learning-based predictive models for a
# demo use case of a "weather signals" (aka wxsignals) offering (e.g., building predictive models to estimate sales
# with twc weather data and client data as input) but using simulated (no connection to any actual entity) client data.
# Specifically, this code imports necessary python software packages, predefines variables that correspond to the
# analytics "settings" (aka "parameters") such as constants, and contains custom functions used throughout the code.
#
# This file also contains important pertinent notes of the ensuing analyses (e.g., Problems, Aims, Scope, Significance,
# Solutions, Ideas, Comments, Questions, Hypotheses, Listed Limitations, Listed Needed Improvements, or/and Comments)
#
#
# **Sample Materials, provided under license. <br>
# Licensed Materials - Property of IBM. <br>
# © Copyright IBM Corp. 2019. All Rights Reserved. <br>
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with IBM Corp. <br>**


# ----------------------------------------------------------------------------------------------------------------------
# COMMENTS
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# HYPOTHESES
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# SOLUTIONS
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# TODO
# ----------------------------------------------------------------------------------------------------------------------

# todo: Lord Willing, perhaps applicably update codebase to incorporate a "ml pipeline" implementation.


# ----------------------------------------------------------------------------------------------------------------------
# IMPORT NEEDED LIBRARIES (AKA PACKAGES AKA TOOLBOXES)
# ----------------------------------------------------------------------------------------------------------------------

import datetime
import itertools
#
import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
#
from sklearn.svm import SVR

# notify scientist: completed analyses
print("DONE: 'STEP 0.1a: Import Software Packages' analysis")


# ----------------------------------------------------------------------------------------------------------------------
# MAKE CONSTANTS
# ----------------------------------------------------------------------------------------------------------------------

#
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

list_colpick_nonweather = list_variablesdependent + list_columnsstratby + list_colstring_ohe + list_variablesindependent_time + ["date"]
    
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
valu_adhocthreshold = 45 # todo: change to lower number for demo purposes and to higher number for full purposes
num_permutes = 10 # todo: change back to 100 or make multiple times > 10
num_cvrepeats = 5 # todo: change to higher number if compute power facilitates such
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

# notify scientist: completed analyses
print("DONE: 'STEP 0.1b: Set Parameters' analysis")


# ----------------------------------------------------------------------------------------------------------------------
# MAKE FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------

# DEFINE "MAKE STRATIFIED DATASETS" FUNCTION
def makedatastrata(df, type_dataset, list_keepyears):

    #...........................................................................................................
    # TODO: MAYBE MAKE THIS A SEPARATE FUNCTION???
    #...........................................................................................................

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
    # display(dfM)

    #...........................................................................................................
    # TODO: MAYBE MAKE THIS A SEPARATE FUNCTION???
    #...........................................................................................................

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
        list_columnsdropnow = ["group", "year", "columns_ohe"] + list_columnsstratby + list_colstring_ohe +            list(set(list_variablesdependent) - {name_dvar})

        #
        for jj in list_loop:

            #
            name_dataset = "{}_{}_{}".format(name_client, type_dataset, str(jj)).lower()

            # select certain rows
            # note: yet does not address "np.nan" values in "name_dvar" column for "valu_thresh" value
            bool_pickrows = (
                (dfM["year"].isin(list_keepyears)) &\
                (dfM["group"] == jj) &\
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


# notify scientist: completed analyses
print("DONE: 'STEP 0.1c: Define Custom Functions' analysis")
