# Import packages.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# Moving Average class.
class Moving_Average:

	def __init__(self):
		# Time how long it takes for the algorithm to run.
		start = time.time()


		pd.options.mode.chained_assignment = None

		# Read the data as a pandas dataframe.
		df = pd.read_csv("../data/artane.csv")

		# Sort the data and remove unecessary columns.
		data = df.sort_index(ascending=True, axis=0)
		data = data.drop(["Statistic", "Property Type", "Bedrooms", "Location", "Unit", "Per_Person"], axis=1)

		# Splitting into training: 2008Q1 - 2017Q4.
		# Testing: 2018Q1 - 2020Q3.
		test = data[204:]
		train = data[:204]

		# Create a predictions array.
		predictions = []
		for i in range(0,test.shape[0]):
		    a = train["Value"][len(train)-53+i:].sum() + sum(predictions)
		    b = a/53
		    predictions.append(b)

		# Calculate the root mean square error.
		rmse = np.sqrt(np.mean(np.power((np.array(test["Value"])-predictions),2)))

		stop = time.time()
		total_time = stop - start
		print(f"RMSE: {rmse}")
		print(f"Total time: {total_time}")

		# # Plot the data on a graph.
		# Moving_Average.plot(train, test, predictions)

	# Graph the data using matplotlib.
	def plot(train, test, predictions):
		test['Predictions'] = predictions
		plt.plot(train['Value'])
		plt.plot(test[['Value', 'Predictions']])
		plt.title('Moving Average (Artane)')
		plt.xlabel('Value, Prediction')
		plt.ylabel('Value')
		plt.show()

def main():
	ma = Moving_Average()

	ma

if __name__ == '__main__':
	main()