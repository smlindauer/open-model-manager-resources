import math
import numpy
import pandas
import pickle
import settings

_pFile = open(settings.pickle_path + "hmeq_xgboost.pickle", "rb")
_thisModelFit = pickle.load(_pFile)
_pFile.close()

def scoreHMEQXGBoostModel (JOB, REASON, CLAGE, CLNO, DEBTINC, DELINQ, DEROG, NINQ, YOJ):
    "Output: EM_EVENTPROBABILITY, EM_CLASSIFICATION"

    # Impute the overall median for missing values
    if (CLAGE == None or math.isnan(CLAGE)):
        CLAGE = 173.46666666666600

    if (CLNO == None or math.isnan(CLNO)):
        CLNO = 20.0

    if (DEBTINC == None or math.isnan(DEBTINC)):
        DEBTINC = 34.81826181858690

    if (YOJ == None or math.isnan(YOJ)):
        YOJ = 7.0

    # Impute the overall mode for missing values
    if (DELINQ == None or math.isnan(DELINQ)):
        DELINQ = 0.0

    if (DEROG == None or math.isnan(DEROG)):
        DEROG = 0.0

    if (NINQ == None or math.isnan(NINQ)):
        NINQ = 0.0

    if (JOB == None):
        cStr = "Other"
    else:
        cStr = JOB.strip()
        if (not cStr):
            cStr = "Other"

    JOB_Mgr = numpy.where(cStr == "Mgr", 1.0, 0.0)
    JOB_Office = numpy.where(cStr == "Office", 1.0, 0.0)
    JOB_Other = numpy.where(cStr == "Other", 1.0, 0.0)
    JOB_ProfExe = numpy.where(cStr == "ProfExe", 1.0, 0.0)
    JOB_Sales = numpy.where(cStr == "Sales", 1.0, 0.0)
    JOB_Self = numpy.where(cStr == "Self", 1.0, 0.0)

    if (REASON == None):
        cStr = "DebtCon"
    else:
        cStr = REASON.strip()
        if (not cStr):
            cStr = "DebtCon"
 
    REASON_DebtCon = numpy.where(cStr == "DebtCon", 1.0, 0.0)

    # Construct the input array for scoring
    input_array = pandas.DataFrame([[JOB_Mgr, JOB_Office, JOB_Other, JOB_ProfExe, JOB_Sales, JOB_Self, \
                                     REASON_DebtCon, CLAGE, CLNO, DEBTINC, DELINQ, DEROG, NINQ, YOJ]],
        columns = ["JOB_Mgr", "JOB_Office", "JOB_Other", "JOB_ProfExe", "JOB_Sales", "JOB_Self", \
                   "REASON_DebtCon", "CLAGE", "CLNO", "DEBTINC", "DELINQ", "DEROG", "NINQ", "YOJ"],
        dtype = float)

    # Calculate the predicted probabilities 
    _predProb = _thisModelFit.predict_proba(input_array).astype(numpy.float64)

    # Retrieve the event probability
    EM_EVENTPROBABILITY = float(_predProb[:,1])

    # Determine the predicted target category
    if (EM_EVENTPROBABILITY >= 0.08941485864562787):
        EM_CLASSIFICATION = "1"
    else:
        EM_CLASSIFICATION = "0"

    return(EM_EVENTPROBABILITY, EM_CLASSIFICATION)
