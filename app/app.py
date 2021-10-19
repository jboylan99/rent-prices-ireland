from flask import Flask, render_template, request
# Dictionary of Irish counties mapped to numbers. This is done because the dataset
# has a column of counties which is numeric.
counties = {
	'Carlow': 1,
	'Cavan': 2,
	'Clare': 3,
	'Cork': 4,
	'Donegal': 5,
	'Wicklow': 6,
	'Galway': 7,
	'Kerry': 8,
	'Kildare': 9,
	'Kilkenny': 10,
	'Laois': 11,
	'Leitrim': 12,
	'Limerick': 13,
	'Longford': 14,
	'Louth': 15,
	'Mayo': 16,
	'Meath': 17,
	'Monaghan': 18,
	'Offaly': 19,
	'Roscommon': 20,
	'Sligo': 21,
	'Tipperary': 22,
	'Waterford': 23,
	'Westmeath': 24,
	'Wexford': 25,
	'Dublin': 26,
}
# create the application object
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/countystatistics')
def countystatistics():
	return render_template('countystats.html')

@app.route('/nationalstatistics')
def nationalstatistics():
	legend = 'Monthly Data'
	labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
	values = [10, 9, 8, 7, 6, 4, 7, 8]
	return render_template('nationalstats.html')

@app.route('/countystatistics/<county>')
def county(county):
	return render_template('countytemplate.html', county=county)

@app.route('/result', methods = ['POST'])
def result():
	year = request.form['year']
	quarter = request.form['quarter']
	rooms = request.form['rooms']
	county = request.form['county']

	county_id = counties[county]

	import arima
	year_quart = year + quarter
	price = arima.run(county_id, year_quart, int(rooms))
	price = str('{:0.2f}'.format(price))
	
	return render_template('result.html', price=price, county=county, rooms=rooms, year=year, quarter=quarter)

# start the server with the 'run()' method
if __name__ == '__main__':
	app.run(debug=True)