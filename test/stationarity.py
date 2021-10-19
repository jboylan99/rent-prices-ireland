import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from statsmodels.tsa.stattools import adfuller
from statsmodels.tools.eval_measures import rmse, aic

data = pd.read_csv("../data/ireland.csv", parse_dates=["Quarter"], index_col="Quarter")
data = data.loc[lambda data: data["County ID"] == 4]
data = data.drop(["Statistic", "Property Type", "Location", "Unit", "County ID", "Value"], axis = 1)

counties = {1:'Carlow',2:'Cavan',3:'Clare',4:'Cork',5:'Donegal',6:'Wicklow',7:'Galway',8:'Kerry',
			9:'Kildare',10:'Kilkenny',11:'Laois',12:'Leitrim',13:'Limerick',14:'Longford',15:'Louth',
			16:'Mayo',17:'Meath',18:'Monaghan',19:'Offaly',20:'Roscommon',21:'Sligo',22:'Tipperary',
			23:'Waterford',24:'Westmeath',25:'Wexford',26:'Dublin'}

dic = {"Quarter": [], "Per Person": []}
bedrooms = 3
for x in range(8,21):
	if x < 10:
		x = f"0{x}"
	else:
		x = str(x)

	if int(x) < 20:
		for y in range(1,11,3):
			if y != 10:
				y = f"0{y}"
			else:
				y = str(y)

			df = data.loc[lambda data: data["Bedrooms"] == bedrooms]
			beds = df['Per_Person']
			price = beds[f"20{x}-{y}-01"].sum() / len(beds[f"20{x}-{y}-01"])
			dic["Quarter"].append(f"20{x}-{y}-01")
			dic["Per Person"].append(price)
	else:
		for y in range(1,8,3):
			y = f"0{y}"

			df = data.loc[lambda data: data["Bedrooms"] == bedrooms]
			beds = df['Per_Person']
			price = beds[f"20{x}-{y}-01"].sum() / len(beds[f"20{x}-{y}-01"])
			dic["Quarter"].append(f"20{x}-{y}-01")
			dic["Per Person"].append(price)

new_data = pd.DataFrame.from_dict(dic)
new_data = new_data.set_index("Quarter")

from statsmodels.tsa.stattools import adfuller
def rolling_statistics(data):
	#Determing rolling statistics
	rolmean = data.rolling(10).mean()
	rolstd = data.rolling(10).std()

	#Plot rolling statistics:
	colour = 'grey'
	plt.rcParams['text.color'] = colour
	plt.rcParams['axes.labelcolor'] = colour
	plt.rcParams['xtick.color'] = colour
	plt.rcParams['ytick.color'] = colour

	original = plt.plot(data, color="#66b3ff",label="Original")
	mean = plt.plot(rolmean, color="#99ff99", label="Rolling Mean")
	std = plt.plot(rolstd, color="orange", label = "Rolling Std")
	# plt.legend(loc="best")
	plt.title("Rolling Mean & Standard Deviation")

	ax = plt.axes()
	ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.spines['left'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	plt.xticks(rotation=270)
	plt.subplots_adjust(bottom=0.14, top=0.91)
	plt.legend()

	nth_tick = 4 # Keeps every 4th label so to only display first quarter of every year.
	[y.set_visible(False) for (x,y) in enumerate(ax.xaxis.get_ticklabels()) if x % nth_tick != 0]

	plt.show()

def dickey_fuller(data):
	#Perform Dickey-Fuller test:
	print("Dickey-Fuller Test:")
	dftest = adfuller(data, autolag="AIC")
	output = pd.Series(dftest[0:4], index=["Test Statistic","p-value","Lags Used","Number of Observations Used"])
	for key, value in dftest[4].items():
		output[f"Critical Value ({key})"] = value
	print(output)

rolling_statistics(new_data)
dickey_fuller(new_data)

#Differencing
log = np.log(new_data)
log_dif = log - log.shift()
log_dif.dropna(inplace=True)

rolling_statistics(log_dif)
dickey_fuller(log_dif)
