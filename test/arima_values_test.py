import pandas as pd
import numpy as np
from datetime import datetime

data = pd.read_csv("../data/ireland.csv", parse_dates=["Quarter"], index_col="Quarter")
data = data.loc[lambda data: data["County ID"] == 26]
data = data.drop(["Statistic", "Property Type", "Location", "Unit", "County ID", "Value"], axis = 1)

counties = {1:'Carlow',2:'Cavan',3:'Clare',4:'Cork',5:'Donegal',6:'Wicklow',7:'Galway',8:'Kerry',
			9:'Kildare',10:'Kilkenny',11:'Laois',12:'Leitrim',13:'Limerick',14:'Longford',15:'Louth',
			16:'Mayo',17:'Meath',18:'Monaghan',19:'Offaly',20:'Roscommon',21:'Sligo',22:'Tipperary',
			23:'Waterford',24:'Westmeath',25:'Wexford',26:'Dublin',}

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

log = np.log(new_data)

from statsmodels.tsa.arima_model import ARIMA

models = []
RMSEs = []
for x in range(10):
	for y in range(3):
		for z in range(10):
			try:
				model = ARIMA(log, order=(x,y,z))
				results_ARIMA = model.fit(disp=-1)

				predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
				predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
				predictions_ARIMA_log = pd.Series(log["Per Person"].values, index=log.index)
				predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)

				predictions_ARIMA = np.exp(predictions_ARIMA_log)

				model_name = f"({x},{y},{z})"
				rmse = "RMSE: {:0.4f}".format(np.sqrt(sum((predictions_ARIMA.sub(new_data.squeeze()))**2)/len(new_data)))
				models.append(model_name)
				RMSEs.append(rmse)
			except:
				pass

for i in range(len(models)):
	print(f"{models[i]} {RMSEs[i]}")