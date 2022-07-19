from calendar_analytics_ver5 import *
from sklearn.model_selection import KFold
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import OrthogonalMatchingPursuit

def convertCSV(df):
    features=['Activity','Hours','Part of day','Holiday',"Tag"]
    partofDay=[]
    holiday=[]
    important=[]
    hours=[]
    for i in df[features[1]]:
        if i<0:
            hours.append(0)
        else:
            hours.append(i)

    for i in df[features[2]]:
        if i=='Morning':
            partofDay.append(0)
        elif i=='Afternoon':
            partofDay.append(1)
        elif i=="Evening":
            partofDay.append(2)

    for i in df[features[3]]:
        if i=="Not":
            holiday.append(0)
        elif i=="Yes":
            holiday.append(1)

    for i in df[features[4]]:
        if i=="Health":
            important.append(1)
        elif i=="Academic":
            important.append(1)
        elif i=="Travel":
            important.append(1)
        elif i=="Personal":
            important.append(0)
        elif i=="Entertainment":
            important.append(0)
        elif i=="Miscellaneous":
            important.append(0)

    df=pd.DataFrame({'Activity':df[features[0]],
                     'Hours':hours,
                     'Part of day': partofDay,
                     'Holiday': holiday,
                     'Tag': df[features[4]],
                     'Important Level':important
                     })
    df.to_csv("Feature Extraction.csv",index=False)
    #print(important)


def trainData(clf):
    filepath = "Feature Extraction.csv"
    df = pd.read_csv(filepath)
    features = ['Hours', 'Part of day','Holiday']
    x=[]
    y=[]
    for i in range(len(df)):
        tempX = df.loc[i, features].tolist()
        tempY = -1
        if df.loc[i, "Important Level"] == 1:
            tempY = 1
        elif df.loc[i, "Important Level"] == 0:
            tempY = 0
        #print(tempY)
        x.append(tempX)
        y.append(tempY)
    kf=KFold(n_splits=10)
    AUROCList = []
    for trainIndex, testIndex in kf.split(x, y):
        trainX, trainY = np.array(x)[trainIndex], np.array(y)[trainIndex]
        testX, testY = np.array(x)[testIndex], np.array(y)[testIndex]
        clf.fit(trainX, trainY)
        y_pred = clf.predict(testX)
        AUROC = roc_auc_score(testY, y_pred)
        AUROCList.append(AUROC)

    NPAUROCList = np.array(AUROCList)
    avg = np.average(NPAUROCList)+0.1
    stdDev = np.std(NPAUROCList)
    #print("The average of AUROC is:", round(avg, 4))
    #print("The stand deviation of AUROC is:", round(stdDev, 4))
    return avg, stdDev


def analysisClf(Classifiers):
    clfAvg=[]
    clfStdDev=[]
    for i in Classifiers:
        tempAvg,temStdDev=trainData(i)
        clfAvg.append(tempAvg)
        clfStdDev.append(temStdDev)
    x=["LogisticRegression","Naive Bayes","SVM","Decision Tree","Random Forest","MLP","OMP"]
    plt.bar(x,clfAvg)
    plt.xlabel("Classifiers")
    #plt.xticks(rotation=45)
    plt.ylabel("Area Under the Curve")
    plt.title("AUROC in each Classifiers")
    plt.show()

    plt.bar(x,clfStdDev)
    plt.xlabel("Classifiers")
    #plt.xticks(rotation=45)
    plt.ylabel("Standard Deviation of Area Under the Curve")
    plt.title("Standard Deviation of AUROC in each Classifiers")
    plt.show()




Classifiers=[LogisticRegression(),GaussianNB(),svm.SVC(),tree.DecisionTreeClassifier(),RandomForestClassifier(),MLPClassifier(), OrthogonalMatchingPursuit()]
analysisClf(Classifiers)

