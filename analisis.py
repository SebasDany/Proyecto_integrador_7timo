import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
url="HWbyEmColorado.csv"
dataset = pd.read_csv(url)
print(type(dataset))
print(dataset)
m=np.matrix(dataset)
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
LL=np.insert(RESUL, RESUL.shape[1], np.array(area), 1)
n=pd.DataFrame()
print(LL)

n.corr(method="pearson")
print(n.corr())

