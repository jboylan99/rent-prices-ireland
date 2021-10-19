# Import packages.
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt
import time

class Random_Forest_Regression:

    def __init__(self, predict=True):
        start = time.time()

        data = pd.read_csv("../data/artane.csv")
        data.to_numpy()

        train = data.drop(['Value', "Statistic", "Property Type", "Location", "Unit", "Per_Person"], axis = 1)
        train = np.array(train)
        test = np.array(data['Value'])

        kf = KFold(n_splits=10,shuffle=False)

        train_r2_scores, test_r2_scores = [], []
        train_mean_scores, test_mean_scores = [], []
        for train_index, test_index in kf.split(train):

            x_train = train[train_index]
            y_train = test[train_index]

            x_test = train[test_index]
            y_test = test[test_index]

            rf = RandomForestRegressor(n_estimators = 100, criterion = 'mse')
            
            rf.fit(x_train, y_train)

            # # This gives the model a very high accuracy contradicting the r2 score
            # predictions = rf.predict(x_test)
            # errors = abs(predictions - y_test)
            # mape = 100 * (errors / y_test)
            # accuracy = 100 - np.mean(mape)
            # print(f'Accuracy: {accuracy} %')

            train_accuracy = rf.score(x_train, y_train)
            test_accuracy = rf.score(x_test, y_test)

            train_mean = sqrt(mean_squared_error(y_train, rf.predict(x_train)))
            test_mean = sqrt(mean_squared_error(y_test, rf.predict(x_test)))

            # # Used to print each split result
            # print(f"R2: {train_accuracy}")
            # print(f"Mean: {train_mean}")
            # print(f"R2: {test_accuracy}")
            # print(f"Mean: {test_mean}")

            train_r2_scores.append(train_accuracy)
            test_r2_scores.append(test_accuracy)

            train_mean_scores.append(train_mean)
            test_mean_scores.append(test_mean)

        average_train_accuracy = np.mean(train_r2_scores)
        average_test_accuracy = np.mean(test_r2_scores)

        average_train_mean = np.mean(train_mean_scores)
        average_test_mean = np.mean(test_mean_scores)

        print(f"Average training Accuracy: {average_train_accuracy}")
        print(f"Average testing Accuracy: {average_test_accuracy}")

        print(f"Average training Mean: {average_train_mean}")
        print(f"Average testing Mean: {average_test_mean}")

        stop = time.time()
        print(f"Total time: {stop - start}")
        
        #Used for prediction
        if predict:
            quarter = float(input('Enter quarter: '))
            rooms = float(input('Enter rooms: '))
            print(f"The Price will be: €{Random_Forest_Regression.futureprice(rf, quarter, rooms)}")
            print(f"Total time: {stop - start}")

    def future_price(rf, quarter, bedrooms):
        d = {"Quarter": [quarter], "Bedrooms": [bedrooms]}
        df = pd.DataFrame(data=d)
        return rf.predict(df)[0]

def main():
    rf = Random_Forest_Regression(predict=False)

    rf

if __name__ == '__main__':
    main()