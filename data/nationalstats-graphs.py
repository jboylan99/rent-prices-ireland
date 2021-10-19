import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read data and drop unecessary columns.
df = pd.read_csv("ireland.csv")
df = df.drop(["Statistic", "Property Type", "Location", "Unit", "Value", "Bedrooms"], axis=1)

# Uses data from 2020 - present.
df = df.iloc[102860:]

# List counties by province so they can be graphed.
counties = ['Carlow','Cavan','Clare','Cork','Donegal','Wicklow','Galway','Kerry','Kildare','Kilkenny','Laois','Leitrim','Limerick','Longford','Louth',
			'Mayo','Meath','Monaghan','Offaly','Roscommon','Sligo','Tipperary','Waterford','Westmeath','Wexford','Dublin']

ulster = ['Cavan', 'Donegal', 'Monaghan']
munster = ['Clare', 'Cork', 'Kerry', 'Limerick', 'Tipperary', 'Waterford']
connacht = ['Galway', 'Leitrim', 'Mayo', 'Roscommon', 'Sligo']
leinster = ['Carlow', 'Wicklow', 'Kildare', 'Kilkenny', 'Laois', 'Longford', 'Louth', 'Meath', 'Offaly', 'Westmeath', 'Wexford', 'Dublin']

ulster_id = [2, 5, 18]
munster_id = [3,4,8,13,22,23]
connacht_id = [7,12,16,20,21]
leinster_id = [1,6,9,10,11,14,15,17,19,24,25,26]

# Function to graph the mean and medium price per month of each county.
def counties_mean_median():
	median = []
	mean = []

	i = 1
	while i <= 26:
		if i in connacht_id:
			county_data = df.loc[df['County ID'] == i]
	 
			median.append(float("{:0.2f}".format(county_data["Per_Person"].median())))
			mean.append(float("{:0.2f}".format(county_data["Per_Person"].mean())))

		i += 1

	x_axis = np.arange(len(connacht))

	# Set text colour to grey so it can be seen in both light and dark mode.
	colour = 'grey'
	plt.rcParams['text.color'] = colour
	plt.rcParams['axes.labelcolor'] = colour
	plt.rcParams['xtick.color'] = colour
	plt.rcParams['ytick.color'] = colour

	plt.xticks(x_axis, connacht)
	plt.bar(x_axis - 0.2, median, width = 0.4, label="Median", color = "#66b3ff")
	plt.bar(x_axis + 0.2, mean, width = 0.4, label="Mean", color = '#ff9999')
	plt.title('CONNACHT: County Vs Monthly Price Per Person (€) (2020 Q1 - Q3)')
	plt.xlabel('County')
	plt.ylabel('Monthly Price Per Person (€)')
	# plt.xticks(rotation=270)

	# Hide the borders around the graphs.
	ax = plt.axes()
	ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.spines['left'].set_visible(False)
	ax.spines['bottom'].set_visible(False)

	plt.subplots_adjust(right=1)
	plt.legend()
	plt.savefig('../app/static/graphs/connacht.png', transparent=True, bbox_inches='tight')
	# plt.show()

# Function to create a pie chart showing the counties with the most properties.
def counties_pie_chart():
	# List that contains the no. of properties in each county.
	num_properties = []
	# These were the top five.
	top_five = ['Cork','Galway','Kildare','Limerick','Dublin']

	# While loop that calculates the no. of properties in each county.
	i = 1
	while i <= 26:
		county_data = df.loc[df['County ID'] == i]
		num_properties.append((len(county_data)))
		i += 1

	# Adds the top 5 counties' property numbers to chosen list.
	chosen = []
	i = 0
	while i <= len(num_properties):
		if i in [4,7,9,13,26]:
			chosen.append(num_properties[i - 1])
		i += 1

	# explodes the largest percentage of data (Dublin).
	explode = [0,0,0,0,0.1]
	# Set text colour to grey so it can be seen in both light and dark mode.
	colour = 'grey'
	plt.rcParams['text.color'] = colour
	# Create pie chart
	plt.pie(chosen, labels = chosen, explode = explode)

	colour = 'grey'
	plt.rcParams['text.color'] = colour
	plt.axis('equal')  
	plt.tight_layout()
	plt.title('Number of properties to rent per county in 2020 (Top 5)')
	plt.legend(labels = top_five)
	plt.subplots_adjust(top = 0.96, bottom = 0.22)
	# plt.savefig('../app/static/graphs/piechart.png', transparent=True, bbox_inches='tight')
	# plt.show()
def main():
	counties_mean_median()
	# counties_pie_chart()

if __name__ == '__main__':
	main()