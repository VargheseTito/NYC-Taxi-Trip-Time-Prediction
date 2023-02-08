
# NYC Taxi Trip Time Prediction


![This is an image](https://thumbs.dreamstime.com/b/new-york-city-taxi-times-square-yellow-cab-34808653.jpg)

Generated a model to predict the total ride duration of taxi trip in New York City.With this model,
the company should be able to estimate the trip duration proactively, which will help
them match the right cabs with the right customers quickly and efficiently.




## Problem Statement

This is our ML Supervised Regression Project.For predicting the trip duration of NYC taxi ride, we will have to analyse the
dataset.Our objectives were to
clean,extract,analyse and to build a
regression model based on the 2016 and to generated a model to predict the total ride duration of taxi trip in New York City.


## Project Description

Taxi cabs in New York are big,
comfortable, clean and even have a
screen where you can play whatever
you like, including a GPS so that you
can verify the taxi's route. The
downside with having an abundance
of cabs results in traffic. Taxicabs are
operated by private companies and
licensed by the New York City Taxi
and Limousine Commission and they
have provided us a dataset that
contain pickup time, drop-off time,
geo- coordinates, number of
passengers, trip duration and other
variables. We shall predict the trip
duration of the taxi for both users and
drivers and make it easier to
understand the trip duration, pricing
range and route to prefer. The dataset
is based on the 2016 NYC Yellow
Cab trip record data made available in
Big Query on Google Cloud Platform.

The data was originally published by
the NYC Taxi and Limousine
Commission (TLC).

ML pipeline to be followed

● Dataset Inspection
● Data Cleaning
● Exploratory Data Analysis
● Feature Engineering
● One Hot Encoding
● Baseline Model with default
parameters
● Performance Metrics
● Optimization of the Model
● Feature Importance
● Hyperparameter Tuning
● Analyze Results

![This is an image](https://38.media.tumblr.com/e82f89b9c3f5a0a1257228edc6b09d05/tumblr_n6k2q1wTtU1rel31wo1_500.gif)

Challenges-

Extracting new features from
existing features were a bit
tedious job to do.

● Handling Outliers in
Independent features was bit
lengthy process.

● There were few irrelevant data
records present in the dataset.

● The Randomised Search cv
took nearly more than a hour to
run ,so it was really time
consuming.
## Demo



![This is an image](https://miro.medium.com/max/846/1*RLVF1R0uIjOCjoAh5J-fDQ.png)
## About the data

Data fields

● id - a unique identifier for each
trip

● vendor_id - a code indicating
the provider associated with the
trip record

● pickup_datetime - date and
time when the meter was
engaged

● dropoff_datetime - date and
time when the meter was
disengaged

● passenger_count - the number
of passengers in the vehicle
(driver entered value)

● pickup_longitude - the
longitude where the meter was
engaged

● pickup_latitude - the latitude
where the meter was engaged

● dropoff_longitude - the
longitude where the meter was
disengaged

● dropoff_latitude - the latitude
where the meter was
disengaged

● store_and_fwd_flag - This flag
indicates whether the trip
record was held in vehicle
memory before sending to the
vendor because the vehicle did
not have a connection to the
server - Y=store and forward;
N=not a store and forward trip

● trip_duration - duration of the
trip in seconds
## Steps Involved


Outlier Treatment
One of the most important steps as
part of data preprocessing is detecting
and treating the outliers as they can
negatively affect the analysis and the
training process of a machine learning
algorithm resulting in lower accuracy.

An outlier may occur due to the
variability in the data, or due to
experimental error/human error.

Box plots are a visual method to
identify outliers. It is a data
visualization plotting function. It
shows the min, max, median, first
quartile, and third quartile

The pickup latitudes and longitudes
should be within the NYC boundary

as defined-
pickup latitude/longitude < 1th

percentile value of the pickup
latitude/longitude and pickup
latitude/longitude > 99.8th percentile
value of the trip duration
tripduration < 1th percentile value of
the trip duration and trip_duration >
99.8th percentile value of the trip
duration
distance between the pickup and
dropoff points is > its 1th percentile
value and < its 99.8th percentile
value.

trip_speed between the pickup and
dropoff points is > its 1th percentile
value and < its 99.8th percentile
value.
We have removed all the records
which were not lies within these
ranges.



Exploratory Data Analysis
We performed univariate and bivariate analyses. This process helped us figure out various aspects and relationships among variables. It gave us a better idea of which feature behaves in which manner.

Encoding of categorical columns
We used One Hot Encoding(converting to dummy variables) to produce binary integers of 0 and 1 to encode our categorical features because categorical features that are in string format cannot be understood by the machine and needs to be converted to the numerical format.

Feature Engineering

We have derived few features from
pickup/dropoff datetime columns after
converting its datatype to datetime.

Few new features derived are-
pickup/dropoff

month,day,weekday,hour,timezone
and date.

We have derived a new feature
(distance and trip_direction) using the
available features in our dataset like
geographical lattitude and longitude, We have also derived new features
like (time_diff_minutes) by
subtracting dropoff_datetime and
pickup_datetime which is highly
correlated with our target variable.

Another important feature derived
trip_speed using trip_distance(km)
and time_diff_minutes features. We
have used 0.621 to convert the trip
distance to miles and 0.00278 to
convert seconds to hour.

Feature Selection

Feature selection is nothing but a
selection of required independent
features. Selecting the important
independent features which have
more relation with the dependent
feature will help to build a good
model.
While building a machine learning
model for real-life dataset, we come
across a lot of features in the dataset
and not all these features are
important every time. Adding
unnecessary features while training
the model leads us to reduce the
overall accuracy of the model,
increase the complexity of the model
and decrease the generalization
capability of the model and makes the
model biased.
Hence, feature selection is one of the
important steps while building a
machine learning model. Its goal is to
find the best possible set of features

for building a machine learning
model. It is a fast and easy procedure
to perform, the results of which allow
you to compare the performance of
machine learning algorithms for your
predictive modelling problem.

Fitting different models
For modeling, we tried various algorithms like:


Linear Regression
Lasso and Ridge Regularization
Decision Tree
Random Forest Classification
XGBoost Classification


Tuning the hyperparameters for better accuracy
It is necessary to tune the hyperparameters of respective algorithms to improve accuracy and avoid overfitting when using tree-based models such as Random Forest Classifier and XGBoost classifier. The best set of hyperparameters was determined using a grid search algorithm.







## Conclusion
1. We can also use stacking algorithm
over here to find the accuracy,but due
to the high computation time we
didn't used it.

2. We got the best model accuracy in
Xgboost model,r2 score of 0.84 in
training set and 0.83 in test data..The
RMSE score of Xgboost model is
0.282

3. Our second best model is Random
Forest based with a r2 score of 0.7485
accuracy in training and 0.7475
accuracy in test data. The RMSE
score of random forest is 0.350

4. Our base model (Linear Regression)
gave us a r2_score of 0.6499 in train
and test data and keep this model
accuracy in reference to compare
other model.

5.The most important variables
other than the distance between the
pickup and dropoff locations, are:

● hour of the day
● weekday
● pickup and dropoff lat lons
● bearing (trip direction)
● even the day of the month

6. We can also do Model
Explainability of random forest and
XGboost model over here using
SHAP, LIME or ELI5.But our team
intention was not to make it lengthier
hence we restricted ourselves till here.
## Future Scope

1. Implement deep learning
models to fit the data. Since we
have millions of taxi trips in
this data we can use multi layer
neural network models to see if
they give better performance compared to the other models
tried in this notebook.

2. Build a simple web application
such that a user can input the
pickup and dropoff latitudes
and longitudes and the web app
will throw out the estimated trip
duration (using our best model).

3. We can also do little more
hyperparameter tuning using
different parameters in
GridSearchCv with a optimal
value of crossvalidation
,inorder to fine tune the model
and to improve the model
accuracy.
## References

● https://www.geeksforgeek
s.org/feature-selection-tec
hniques-in-machine-learn
ing/
● https://scikit-learn.org/sta
ble/index.html
● https://en.wikipedia.org/w
iki/Taxis_of_New_York_C
ity

● https://www.ibm.com/clou
d/learn/random-forest

● https://www.geeksforgeek
s.org/xgboost/
## Contribution

Tito Varghese | Data Science Trainee | Machine Learning |

https://www.linkedin.com/in/tito-varghese