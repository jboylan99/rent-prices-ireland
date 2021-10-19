import pandas as pd
import numpy as np
from datetime import datetime

def size(county_id):
	data = pd.read_csv("../data/ireland.csv", parse_dates=["Quarter"], index_col="Quarter")
	data = data.loc[lambda data: data["County ID"] == county_id]
	data = data.drop(["Statistic", "Property Type", "Location", "Unit", "County ID", "Value"], axis = 1)

	dic = {"Quarter": [], "Per Person": []}
	bedrooms = 4
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

	return new_data.size