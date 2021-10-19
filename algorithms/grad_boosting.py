# Import packages.
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from math import sqrt
from sklearn.ensemble import GradientBoostingRegressor
import time

# Gradient boosting regression class.
class Grad_Boosting:

	def __init__(self):
		# Time how long it takes for the algorithm to run.
		start = time.time()

		# Read the data as a pandas dataframe.
		data = pd.read_csv("../data/artane.csv")

		# Drop unecessary columns from the dataset.
		data = data.drop(["Statistic", "Property Type", "Location", "Unit", "Per_Person"], axis=1)

		# Define testing and training data.
		test = data["Value"]
		train = data.drop(["Value"], axis=1)

		# Define x and y train, x and y test.
		x_train, x_test, y_train, y_test = train_test_split(train, test, test_size=0.20, random_state=10, shuffle=False)

		# Fit the data with x and y train.
		reg = GradientBoostingRegressor(n_estimators=15, max_depth=5, min_samples_split=2, learning_rate=0.1, loss="ls")
		reg.fit(x_train, y_train)

		# Calculate R2 score and root mean square error.
		# print(f"R2: {r2_score(x_train, y_train)}")
		print(f"Mean: {sqrt(mean_squared_error(y_train, reg.predict(x_train)))}")
		# print(f"R2: {r2_score(x_test, y_test)}")
		print(f"Mean: {sqrt(mean_squared_error(y_test, reg.predict(x_test)))}")

		stop = time.time()
		print(f"Total time: {stop - start}")
		
		quarter = float(input('Enter quarter: '))
		rooms = float(input('Enter rooms: '))
		print(f"The Price will be: €{Grad_Boosting.futureprice(reg, quarter, rooms)}")


	# # Method to predict future rent price.
	# def futureprice(reg, quarter, rooms):
	# 	new = np.array([quarter, rooms]).reshape(1, 2)
	# 	return reg.predict(new)[0]

def main():
	gb = Grad_Boosting()

	gb

if __name__ == '__main__':
	main()