# Test Results

Tests were run on the *artane.csv* data subset in order to collect the root mean square error (RMSE). The lower the RMSE is, the more accurate the algorithm is. These are the results of the RMSE and the time it took to run, rounded to 5 significant decimal points.


**Moving Average**
RMSE: 266.87726
Total time: 0.024895 seconds

**Linear Regression**
RMSE: 87.75139
Time to run: 0.091101 seconds

**K-Nearest Neighbour**
RMSE: 155.65892
Total time: 0.023467 seconds

**Gradient Boosting Regression**
RMSE: 199.46174
Total time: 0.016954 seconds

**Long Short Term Memory**
We were unable to get long short term memory running successfully with our database.

**Random Forest**
RMSE: 49.57617
Total time: 1.65228 seconds

**ARIMA**
RMSE: 47.56068
Total time: 2.49112 seconds

# User Test Results

We created and distributed it and asked for feedback on our project. These were the questions.

How would you rate the usability of the web application?

Did you think it was easy to navigate the site and achieve what you wanted to do?

Do you think the rent prices shown in your area are an accurate reflection of the current prices in your area?

Would you continue to use this website if it was made available permanently?

Are there any improvements you would like to see implemented?

The results were very positive with 15 replies. The major improvements that were requested were an improved dark mode and a feature to compare counties.

We also asked them if there were any noticeable bugs present. There were two that stood out. The first was the flash of incorrect theme on dark mode.
This occurred because the page loaded the default CSS before the javascript file set it to the user's preference. This causes a momentary flash on some user's slower PCs but we didn't have time to fix this.

The second issue was that our Submit button had a loading spinner but if the form was entered incorrectly then it woudn't stop spinning, but clicking it again to reload would stop it, causing the button's functionality to reverse.

Thanks to user testing, we were able to notice this bug and in the end we removed the loading spinner.