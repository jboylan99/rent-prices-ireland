#Prevents runtime error
import matplotlib
matplotlib.use('Agg')

#Importing packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA

#Run the main function
def run(county_id, year_quart, rooms):
	#Read in data from csv
	data = pd.read_csv("../data/ireland.csv", parse_dates=["Quarter"], index_col="Quarter")

	#Only return data for the users chosen county
	data = data.loc[lambda data: data["County ID"] == county_id]

	# Drop unecessary columns from the dataset
	data = data.drop(["Statistic", "Property Type", "Location", "Unit", "County ID", "Value"], axis = 1)

	#Dictionary that links county names to county id
	counties = {1:'Carlow',2:'Cavan',3:'Clare',4:'Cork',5:'Donegal',6:'Wicklow',7:'Galway',8:'Kerry',
				9:'Kildare',10:'Kilkenny',11:'Laois',12:'Leitrim',13:'Limerick',14:'Longford',15:'Louth',
				16:'Mayo',17:'Meath',18:'Monaghan',19:'Offaly',20:'Roscommon',21:'Sligo',22:'Tipperary',
				23:'Waterford',24:'Westmeath',25:'Wexford',26:'Dublin',}

	#Empty dictionary that will later make up a DataFrame
	dic = {"Quarter": [], "Per Person": []}

	#User selected number of bedrooms
	bedrooms = rooms

	#Moving yearly from 2008 to 2020
	for x in range(8,21):
		if x < 10:
			x = f"0{x}"
		else:
			x = str(x)

		if int(x) < 20:
			#Moving each Quarter [01, 04, 07, 10]
			for y in range(1,11,3):
				if y != 10:
					y = f"0{y}"
				else:
					y = str(y)

				#Only return data for the users chosen number of bedrooms
				df = data.loc[lambda data: data["Bedrooms"] == bedrooms]
				beds = df['Per_Person']

				#Get the mean price for each Quarter
				price = beds[f"20{x}-{y}-01"].sum() / len(beds[f"20{x}-{y}-01"])

				#Add the values to the dictionary
				dic["Quarter"].append(f"20{x}-{y}-01")
				dic["Per Person"].append(price)
		else:
			#Moving each Quarter [01, 04, 07] as 2020 only goes to the third yearly Quarter
			for y in range(1,8,3):
				y = f"0{y}"

				#Only return data for the users chosen number of bedrooms
				df = data.loc[lambda data: data["Bedrooms"] == bedrooms]
				beds = df['Per_Person']

				#Get the mean price for each Quarter
				price = beds[f"20{x}-{y}-01"].sum() / len(beds[f"20{x}-{y}-01"])

				#Add the values to the dictionary
				dic["Quarter"].append(f"20{x}-{y}-01")
				dic["Per Person"].append(price)

	#Create a DataFrame from the dictionary
	new_data = pd.DataFrame.from_dict(dic)
	new_data = new_data.set_index("Quarter")

	#Calculate the log of the data to reduce the effects of trends and seasonality
	log = np.log(new_data)

	#Create an ARIMA model using p, d, q values calculated during testing
	model = ARIMA(log, order=(4,1,0))
	results_ARIMA = model.fit(disp=-1)

	#Forcast prices until the end of 2022
	results = results_ARIMA.forecast(steps=9)[0]
	results = np.exp(results)

	#Add dates to correspond to the forecast
	future_dates = ["2020-10-01", "2021-01-01", "2021-04-01", "2021-07-01",
					"2021-10-01", "2022-01-01", "2022-04-01", "2022-07-01",
					"2022-10-01"]
	pred_dict = {"Quarter": future_dates, "Per Person": results}

	#Create a DataFrame for plotting on graphs
	pred_data = pd.DataFrame.from_dict(pred_dict)
	pred_data = pred_data.set_index("Quarter")

	#Print the Root Mean Squared Error
	#print('RMSE: %.4f'% np.sqrt(sum((predictions_ARIMA.sub(new_data.squeeze()))**2)/len(new_data)))

	#Draw graph function
	def draw_graph(data, predictions, county_dict, county_id):
		#Ensure the graph is cleared
		plt.clf()

		#Change colour to grey
		colour = 'grey'
		plt.rcParams['text.color'] = colour
		plt.rcParams['axes.labelcolor'] = colour
		plt.rcParams['xtick.color'] = colour
		plt.rcParams['ytick.color'] = colour

		#Label the axes
		plt.xlabel('Quarter')
		plt.ylabel('Monthly Price Per Person (€)')
		
		#Plot the data
		plt.plot(data, label="Actual Data", color = "#66b3ff")
		plt.plot(predictions, label="Predicted Data", color = "#ff9999")
		plt.title(f"Price Per Person in {county_dict[county_id]}: 2008-01-01 to 2022-10-01")

		#Hide graph outlines
		ax = plt.axes()
		ax.spines['top'].set_visible(False)
		ax.spines['right'].set_visible(False)
		ax.spines['left'].set_visible(False)
		ax.spines['bottom'].set_visible(False)

		#Rotate x-axis labels to inprove readability
		plt.xticks(rotation=270)
		plt.subplots_adjust(right=1, bottom=0.12, top=0.89)
		plt.legend()

		# Keeps every 4th label so to only display first quarter of every year
		nth_tick = 4
		[y.set_visible(False) for (x,y) in enumerate(ax.xaxis.get_ticklabels()) if x % nth_tick != 0]

		#Save figure to graph folder
		plt.savefig(f"static/graphs/{county_dict[county_id]}.png", transparent=True, bbox_inches="tight")

	#Call draw graph function
	draw_graph(new_data, pred_data, counties, county_id)

	#Return the predicted price
	return pred_data.loc[year_quart][0]
