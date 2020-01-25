import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
import seaborn as sns


matplotlib.use('Agg')
matplotlib.rcParams['figure.figsize'] = (9.0, 6.0)

autos = pd.read_csv("auto-mpg.data-original", delim_whitespace = True, header=None,
names=['MPG', 'Cylinders', 'Displacement', 'Horse_Power','Weight', 'Acceleration', 'Model_Year', 'Origin', 'Car_Name'])
autos['maker'] = autos.Car_Name.map(lambda x: x.split()[0])
autos.Origin = autos.Origin.map({1: 'America', 2: 'Europe', 3: 'Asia'})
autos=autos.applymap(lambda x: np.nan if x == '?' else x).dropna()
autos['Horse_Power'] = autos.Horse_Power.astype(float)
autos.sample()
sns.heatmap(autos.corr(), square=True, annot=True)