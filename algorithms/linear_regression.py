# Import packages.
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,mean_squared_error
from math import sqrt
import time

# Linear regression class.
class Linear_Regression:

	def __init__(self):
		# Time how long it takes for the algorithm to run.
		start = time.time()

		# Read the data as a pandas dataframe.
		data = pd.read_csv("../data/artane.csv")
		# Remove unecessary columns.
		data = data.drop(["Statistic", "Property Type", "Location", "Unit"], axis=1)

		reg = LinearRegression()

		# Test data reads in Value column.
		test = data["Value"]
		conv_dates = [1 if values < 2016.3 else 0 for values in data.Quarter]
		data["Quarter"] = conv_dates
		# Training data.
		train = data.drop(["Value"], axis=1)

		# Defin x and y train, x and y test.
		x_train, x_test, y_train, y_test = train_test_split(train, test, test_size=0.10, random_state=10, shuffle = False)
		# Fit the data and print the root mean square error and R2 score.
		reg.fit(x_train,y_train)
		print("Mean: " + str(sqrt(mean_squared_error(y_test, reg.predict(x_test)))))
		print("R2 score: " + str(r2_score(y_test, reg.predict(x_test))))

		stop = time.time()
		print(f"Time to run: {stop - start}")

def main():
	lr = Linear_Regression()

	lr

if __name__ == '__main__':
	main()