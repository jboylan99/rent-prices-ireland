# Import packages.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor as KNN
from sklearn.metrics import mean_squared_error
from math import sqrt
import time

# K-nearest neighbour class.
class K_Nearest_Neighbour:

	def __init__(self):
		# Time how long it takes for the algorithm to run.
		start = time.time()

		# Read the data as a pandas dataframe.
		data = pd.read_csv("../data/artane.csv")

		# Drop unecessary columns from the dataset.
		train = data.drop(["Statistic", "Property Type", "Location", "Unit", "Value", "Per_Person"], axis=1)
		test = data["Value"]

		# Scale and fit the data.
		scaler = MinMaxScaler()
		x_scaled = scaler.fit_transform(train)

		train = pd.DataFrame(x_scaled)

		# Set the values for x and y train, x and y test.
		x_train, x_test, y_train, y_test = train_test_split(train, test, test_size=0.2, random_state=27, shuffle=False)

		# Set value of k to 5.
		reg = KNN(n_neighbors=5)

		# Fit x and y train using KNN.
		reg.fit(x_train, y_train)


		print(f"R2 score is: {reg.score(x_train, y_train)}")
		print(f"Mean: {sqrt(mean_squared_error(y_train, reg.predict(x_train)))}")
		print(f"R2 score is: {reg.score(x_test, y_test)}")
		print(f"Mean: {sqrt(mean_squared_error(y_test, reg.predict(x_test)))}")

		stop = time.time()
		print(f"Total time: {stop - start}")
		
		quarter = float(input('Enter quarter: '))
		rooms = float(input('Enter rooms: '))
		print(f"The Price will be: €{K_Nearest_Neighbour.futureprice(reg, quarter, rooms)}")


		# K_Nearest_Neighbour.test_k_values(x_train, x_test, y_train, y_test)

	# Method to calulate future price.
	def futureprice(reg, quarter, rooms):
		new = np.array([quarter, rooms]).reshape(1, 2)
		return reg.predict(new)[0]

	# Method to plot an elbow curve for KNN.
	# This will determine the best value for k.
	def test_k_values(x_train, x_test, y_train, y_test):
		rmse = []

		for k in range(20):

			k += 1
			model = KNN(n_neighbors = k)

			model.fit(x_train, y_train)
			pred = model.predict(x_test)
			error = sqrt(mean_squared_error(y_test, pred))
			rmse.append(error)
			# print("RMSE value for k = ", k, " is: ", error)

		# Plot the curve graph.
		curve = pd.DataFrame(rmse)
		curve.plot()
		plt.show()

def main():
	knn = K_Nearest_Neighbour()

	knn

if __name__ == '__main__':
	main()