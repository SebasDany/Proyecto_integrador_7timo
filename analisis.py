import numpy as np
import pandas as pd
from sklearn.model_selection import KFold,LeaveOneOut, train_test_split
from sklearn import datasets
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn import model_selection
from sklearn.metrics import r2_score
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
url="aggregate.csv"
dataset = pd.read_csv(url)
print(dataset.head())

dataset.columns

print(dataset.count())

print(type(dataset))
print(dataset.head())
print(dataset)
m=np.matrix(dataset)
nombre=dataset.get("Nombre")
print("·$%&/()(&%$$%&/)(/&%")
print(nombre)

##dataset.corr(method="pearson")
#print(dataset.corr())
area=m[:,5]
periodyear=m[:,6]
periodtype=m[:,7]
period=m[:,9]
corrmat = dataset.corr()
plt.plot(area,period)
sns.heatmap(corrmat, vmax=.8, square=True);
'''
print("ertyuioytdfghjkl")
#https://data.colorado.gov/Labor-Employment/Hours-Worked-by-Employees-in-Colorado/pt2g-89wc
#stateabbrv=dataset.get('suppheallwrkr')
st=dataset.get('suppheallwrkr')
sta=dataset.get('suppheallwrkr')
area=m[:,5]
print(area)
periodyear=m[:,6]
periodtype=m[:,7]
period=m[:,9]
prelim=m[:,15]
empces=m[:,16]
supprecord=m[:,22]
supphe=m[:,23]
supppw=m[:,24]
suppfem=m[:,25]
suppheallwrkr=m[:,29]
xx=np.array(st,sta)
print(xx)
print(len(area),len(periodtype),len(periodyear))
X1 = np.array(list(zip(area,periodyear,periodtype,period,prelim,empces,supprecord,supphe,supppw,suppfem,suppheallwrkr))).reshape(len(area),11)
X=pd.DataFrame(X1)
print(type(X))
print(X.corr())
print(pd.DataFrame(X))
print("################################333")
RESUL=np.matrix
print("==================================================")


dataset.dropna()
print(dataset.dropna())
dataset.corr(method="pearson")
print(dataset.corr())

def scatterplot(x, y, x_title, y_title):
 plt.plot(x, y, 'b.')
 plt.xlabel(x_title)
 plt.ylabel(y_title)
 plt.xlim(min(x)-1, max(x)+1)
 plt.ylim(min(y)-1, max(y)+1)
 plt.show()
scatterplot(area, supprecord, "DEP_TIME",
"ARR_DELAY_NEW")
#LL=np.insert(RESUL, RESUL.shape[1], np.array(area), 1)
#n=pd.DataFrame()
#print(LL)
iris = datasets.load_iris()
#print(iris.data[:, :4])
#print(iris.target)
x=iris.data[:100]
y=iris.target[:100]
#dataframe = pd.read_csv(r"usuarios_win_mac_lin.csv")
#dataframe.head()
#print(dataframe.groupby('clase').size())
#url = 'Deber_7.csv'
#dcsv = pd.read_csv(url)
#print(dcsv)
#dcsv.head()
print("====Holdout method====")
size=int(input("ingrese el porcentaje de para training ejemplo 70. \n"))
#X_train,  X_test,Y_train ,Y_test =train_test_split(x, y, test_size=size)
train=iris.data[:size,:]
print(train)
ytr=iris.target[0:size]
print(ytr)
test=iris.data[size:100,:]
yt=iris.target[size:100]
print("VALORES DE REALES DE Y DEL TEST ",yt)
model = linear_model.LogisticRegression()
model.fit(train,ytr)
predictions = model.predict(test)
print("VALORES DE Y ESTIMADA",predictions)
score=model.score(test,yt)
print("Precisión media de las predicciones",score)
print()
print("====K-Fold Cross-Validation====")
k=int(input("Ingrese el numero de iteraciones  \n"))

regr=linear_model.LinearRegression()
#regr.fit(x_train,y_train)
   # y_pred=regr.predict(x_test)

#print("Error: ",mean_squared_error(y_test,y_pred)*100)

'''
