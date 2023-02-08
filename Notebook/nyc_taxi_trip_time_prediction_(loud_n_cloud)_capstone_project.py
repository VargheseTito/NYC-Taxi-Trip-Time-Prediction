# -*- coding: utf-8 -*-
"""NYC Taxi Trip Time Prediction (Loud n Cloud)- Capstone Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1s5yUjUbJ3Kq0s2rxnnwtRI2F9so_tfko

# <b><u> Project Title : Taxi trip time Prediction : Predicting total ride duration of taxi trips in New York City</u></b>

## <b> Problem Description </b>

### Your task is to build a model that predicts the total ride duration of taxi trips in New York City. Your primary dataset is one released by the NYC Taxi and Limousine Commission, which includes pickup time, geo-coordinates, number of passengers, and several other variables.

## <b> Data Description </b>

### The dataset is based on the 2016 NYC Yellow Cab trip record data made available in Big Query on Google Cloud Platform. The data was originally published by the NYC Taxi and Limousine Commission (TLC). The data was sampled and cleaned for the purposes of this project. Based on individual trip attributes, you should predict the duration of each trip in the test set.

### <b>NYC Taxi Data.csv</b> - the training set (contains 1458644 trip records)


### Data fields
* #### id - a unique identifier for each trip
* #### vendor_id - a code indicating the provider associated with the trip record
* #### pickup_datetime - date and time when the meter was engaged
* #### dropoff_datetime - date and time when the meter was disengaged
* #### passenger_count - the number of passengers in the vehicle (driver entered value)
* #### pickup_longitude - the longitude where the meter was engaged
* #### pickup_latitude - the latitude where the meter was engaged
* #### dropoff_longitude - the longitude where the meter was disengaged
* #### dropoff_latitude - the latitude where the meter was disengaged
* #### store_and_fwd_flag - This flag indicates whether the trip record was held in vehicle memory before sending to the vendor because the vehicle did not have a connection to the server - Y=store and forward; N=not a store and forward trip
* #### trip_duration - duration of the trip in seconds

#Introduction
This is our Regression Capstone Project,hence we will be looking into multiple regression models and try to come up with a best model at the end of this project. We are only focussing on all that algorithm which has been taught to us till now in our class. 
SVM,Time Series, Clustering and many more algos. still yet to be taught to us.

#ML Pipeline to be followed 

1. Basic  Dataset Understanding(Dimensionality,records,Data Types,5-point summary)
2.Data Preprocessing
3. Data Cleaning
4. Exploratory Data Analysis
5. Feature Engineering
6. Feature Selection
7. Model Buliding
8. Evaluation
9. Hyperparameter tuning/cross Validation
10.Conclusions
"""

# Commented out IPython magic to ensure Python compatibility.
#Importing all the required libraries
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import math
# %matplotlib inline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime
import datetime

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV

#Mounting the Drive inorder to load the dataset
from google.colab import drive
drive.mount('/content/drive')

#Reading the csv dataset
df=pd.read_csv('/content/drive/MyDrive/NYC Taxi Trip (Supervised ML Regression)-Tito Varghese/NYC Taxi Data.csv')

"""#1.Basic Dataset Understanding(Dimensionality,records,Data Types,5-point summary)"""

df.info()

"""The dataset info tells us that the dataset contains 1458644 records and 11 columns.Out of 11 columns,4 columns are object datatype ,4 columns are float datatype and remaing 3 columns are integer datatype.

The dataset doesn't contain any null values in any of the columns.
"""

df.describe()

"""The describe function gives us a five - point summary of our numerical columns present in our dataset(min,25%,50%,75% and max details)

Apart from that,it tells the mean and standard deviation values of all respective numerical columns
"""

df.shape

df.head()

df.dtypes

df.nunique()

"""We see that id has 1458644 unique values which are equal to the number of rows in our dataset.

There are 2 unique vendor ids.

There are 10 unique passenger counts.

There are 2 unique values for store_and_fwd_flag, that we also saw in the description of the variables, which are Y and N.

#2.Data Preprocessing

Next we will add some features to the dataset and at the same time also remove the outliers

#Converting the datatype of pickup date time and dropoff date time to datetime datatype
"""

df['pickup_datetime']= pd.to_datetime(df['pickup_datetime'])
df['dropoff_datetime']= pd.to_datetime(df['dropoff_datetime'])

"""#Adding few new Features  into the dataset

#Now, let us extract and create new features from this datetime features we just created
"""

#Extract hour from pickup and dropoff datetime columns
df['pickup_hour']=df['pickup_datetime'].dt.hour
df['dropoff_hour']=df['dropoff_datetime'].dt.hour

#Extract day from pickup and dropoff datetime columns
df['pickup_day']=df['pickup_datetime'].dt.day_name()
df['dropoff_day']=df['dropoff_datetime'].dt.day_name()

#Extract date from pickup and dropoff datetime columns
df['pickup_date']=pd.DatetimeIndex(df['pickup_datetime']).day
df['dropoff_date']=pd.DatetimeIndex(df['dropoff_datetime']).day

#Extract month from pickup and dropoff datetime columns
df['pickup_month']=df['pickup_datetime'].dt.month
df['dropoff_month']=df['dropoff_datetime'].dt.month

#Extract weekday from pickup and dropoff datetime columns
df['pickup_weekday']=df['pickup_datetime'].dt.weekday
df['dropoff_weekday']=df['dropoff_datetime'].dt.weekday

"""pickup_day and dropoff_day which will contain the name of the day on which the ride was taken. 

pickup_weekday and dropoff_weekday which will contain the day number instead of characters with Monday=0 and Sunday=6. 

pickup_hour and dropoff_hour with an hour of the day in the 24-hour format. 

pickup_date and dropoff_date will provide the date of the trip.

pickup_month and dropoff_month with month number with January=1 and December=12. Next, I have

#New feature created time_zone
Defined a function that lets us determine what time of the day the ride was taken. I have created 4 time zones ‘Morning’ (from 6:00 am to 11:59 pm), ‘Afternoon’ (from 12 noon to 3:59 pm), ‘Evening’ (from 4:00 pm to 9:59 pm), and ‘Late Night’ (from 10:00 pm to 5:59 am)
"""

def time_zone(x):
    if x in range(6,12):
        return 'Morning'
    elif x in range(12,16):
        return 'Afternoon'
    elif x in range(16,22):
        return 'Evening'
    else:
        return 'Late night'

df['pickup_timezone']=df['pickup_hour'].apply(time_zone)
df['dropoff_timezone']=df['dropoff_hour'].apply(time_zone)

"""#New feature Created distance

We also saw during dataset exploration that we have coordinates in the form of longitude and latitude for pickup and dropoff. But, we can’t really gather any insights or draw conclusions from that.
So, the most obvious feature that we can extract from this is distance. Let us do that.

Importing the library which lets us calculate distance from geographical coordinates.
"""

from geopy.distance import great_circle

def cal_distance(pickup_lat,pickup_long,dropoff_lat,dropoff_long):
 
 start_coordinates=(pickup_lat,pickup_long)
 stop_coordinates=(dropoff_lat,dropoff_long)
 
 return great_circle(start_coordinates,stop_coordinates).km

df['distance'] = df.apply(lambda x: cal_distance(x['pickup_latitude'],x['pickup_longitude'],x['dropoff_latitude'],x['dropoff_longitude'] ), axis=1)

"""#New feature created trip direction 

It was observed, especially for the airport trips, that the direction of the trip also has some effect on the trip duration.

Let's add the bearing of each trip which simply means the overall direction in which the taxi travelled from the pickup point to the dropoff point.

The convention followed here is such the North is denoted as 0 degrees, East as 90 degrees, South as 180 degrees and circle back to North as 360 degrees.
"""

import math
def get_bearing(lat1, long1, lat2, long2):
    dLon = (long2 - long1)
    x = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
    y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dLon))
    brng = np.arctan2(x,y)
    brng = np.degrees(brng)
    if brng < 0:
      brng = 360 + brng
      return brng
    else:
      return brng

df['trip_direction'] = df.apply(lambda x: get_bearing(x['pickup_latitude'],x['pickup_longitude'],x['dropoff_latitude'], 
                       x['dropoff_longitude']), axis = 1)

"""#New Feature created trip_speed"""

df['time_diff_minutes']= df['dropoff_datetime']- df['pickup_datetime']
df['time_diff_minutes']= df['time_diff_minutes']/np.timedelta64(1,'m')

#The trip_speed unit will be mph
def speed(x,y):
  z = (x*0.621)/(y*0.016667)
  return z

df['trip_speed']= df.apply(lambda x: speed(x['distance'],x['time_diff_minutes']),axis=1)

"""#Thus, we successfully created some new features which we will analyze in univariate and bivariate analysis."""

df.head()

"""#3.Data Cleaning"""

#Checking Missing Values
df.isnull().sum()

#Checking Duplicated Rows
df.duplicated().sum()

"""#Handling Outliers

The pickup  latitudes and longitudes should be within the NYC boundary defined as
pickup latitude/longitude < 1th percentile value of the pickup latitude/longitude and pickup latitude/longitude > 99.8th percentile value of the trip duration

tripduration < 1th percentile value of the trip duration and trip_duration > 99.8th percentile value of the trip duration

distance  between the pickup and dropoff points is > its 1th percentile value and < its 99.8th percentile value.

trip_speed  between the pickup and dropoff points is > its 1th percentile value and < its 99.8th percentile value.

Removing Outliers from Pickup_latitude

Over here we will be take to consideration data records which lies between 99% and 1% range and consider records outside this range as outliers .Hence we will drop records which are outside the range from the dataset
"""

percentile_speed = [1, 25, 50, 75, 95, 99, 99.8]
print("Total number of trips = {:,}".format(len(df)))
for i in percentile_speed:
    print("{}% of the latitude were below {:.2f} degree".format(i, np.percentile(df.pickup_latitude, i)))

df = df[df['pickup_latitude'] <=np.percentile(df.pickup_latitude,99.8) ] #filtering records 
df = df[df['pickup_latitude']>=np.percentile(df.pickup_latitude,1) ]

df.shape

"""Removing Outliers from pickup_longitude and pickup latitude"""

percentile_speed = [1, 25, 50, 75, 95, 99, 99.8]
print("Total number of trips = {:,}".format(len(df)))
for i in percentile_speed:
    print("{}% of the longitude were below {:.2f} degree".format(i, np.percentile(df.pickup_longitude, i)))

df = df[df['pickup_longitude'] <=np.percentile(df.pickup_longitude,99.8) ] #filtering records 
df = df[df['pickup_longitude']>=np.percentile(df.pickup_longitude,1) ]

df.shape

"""Removing Outliers from trip_duration"""

percentile_trip_duration = [1, 25, 50, 75, 95, 99, 99.8]
print("Total number of trips = {:,}".format(len(df)))
for i in percentile_trip_duration:
    print("{}% of the trips were below {:.2f} seconds".format(i, np.percentile(df.trip_duration, i)))

df = df[df['trip_duration'] <= np.percentile(df.trip_duration,99.8)] #filtering records 
df = df[df['trip_duration'] >=np.percentile(df.trip_duration,1) ]

df.shape

"""Removing Outliers from distance"""

percentile_trip_duration = [1, 25, 50, 75, 95, 99, 99.8]
print("Total number of trips = {:,}".format(len(df)))
for i in percentile_trip_duration:
    print("{}% of the distance were below {:.2f} km".format(i, np.percentile(df.distance, i)))

df = df[df['distance'] <= np.percentile(df.distance,99.8)] #filtering records 
df = df[df['distance'] >= np.percentile(df.distance,1)]

df.shape

"""Removing Outliers from trip_speed"""

percentile_trip_duration = [1, 25, 50, 75, 95, 99, 99.8]
print("Total number of trips = {:,}".format(len(df)))
for i in percentile_trip_duration:
    print("{}% of the speed were below {:.2f} mph".format(i, np.percentile(df.trip_speed, i)))

df.trip_speed.min()

df.trip_speed.max() #practically not possible in nyc busy city roads ,its a outlier

df = df[df['trip_speed'] <= np.percentile(df.trip_speed,99.8)] #filtering records 
df = df[df['trip_speed'] >= np.percentile(df.trip_speed,1)]

df.shape

df.drop(labels='id',inplace=True,axis=1)

categorical_features=df.describe(include='object').columns

categorical_features

for col in categorical_features:
    fig = plt.figure(figsize=(9, 6))
    ax = fig.gca()
    df.boxplot(column ='trip_duration', by = col, ax = ax)
    ax.set_title('Label by ' + col)
    ax.set_ylabel("trip_duration")
plt.show()

"""Intially we had 1,458,644 records and after data cleaning by removing outliers we finally left with 1,373,783 records and added few additional features. Nearly 84,861 records were irrelavent to our problem statement and after data cleaning now we can start with our exploratory data analysis part .

#4.Exploratory Data Analysis

##Univariate Analysis

##Passenger count feature
"""

ax = sns.countplot(x = df['passenger_count'])
plt.title(' Dist of passenger count')

for p in ax.patches:
    height = p.get_height()
    ax.text(x = p.get_x() + (p.get_width()/2),
    y = height+0.2, ha = 'center', s = '{:.0f}'.format(height))
plt.show()

df=df[df['passenger_count']!=0]  #remove the rows which have 0 or 7 or 9 passenger count.
df=df[df['passenger_count']<=6]

"""The above plot tells us that the mostly  the taxi trip passengers count is one.

It depicts that taxi are mostly prefered by those who likes to travel alone.

##pickup/dropoff day
"""

figure, ax = plt.subplots(nrows = 1, ncols=2, figsize = (15,10))
sns.countplot(x = 'pickup_day', data = df, ax = ax[0])
ax[0].set_title(' no of pickups done on each day of the week')

sns.countplot(x = 'dropoff_day', data = df, ax = ax[1])
ax[1].set_title(' no of dropoffs done on each day of the week')

#plt.tight_layout()

"""The plot tells us that mostly on friday's we can see a high demand for taxi trip and the least number of taxi trip demand on Monday.

##pickup_timezone
"""

ax = sns.countplot(x=df['pickup_timezone']);
plt.title('Distribution of pickup_timezone')
for p in ax.patches:
    height = p.get_height()
    ax.text(x = p.get_x()+(p.get_width()/2), # x-coordinate position of data label, padded to be in the middle of the bar
    y = height+0.2, ha = 'center',s = '{:.0f}'.format(height)) # data label, formatted to ignore decimals
    #ha = ‘center’) # sets horizontal alignment (ha) to center
plt.xticks(rotation = 'vertical')    
plt.show()

"""1. The high demand for taxi trip is in the evening timezone.
2. The least demand for taxi trip is in the afternoon timezone

##pickup_hour and drop off hour
"""

figure, ax = plt.subplots(nrows = 1, ncols=2, figsize = (10,5))


df.pickup_hour.hist(bins = 24, ax = ax[0])
ax[0].set_title(' pickup hrs')


df.dropoff_hour.hist(bins = 24, ax = ax[1])
ax[1].set_title('dropoff hours')



plt.tight_layout()

df['pickup_hour'].replace(to_replace=0,value=24,inplace=True) #replacing 0 hr with 24 hr

ax = sns.countplot(x = df['pickup_hour'])
plt.title('total pickup_hour')

for p in ax.patches:
    height = p.get_height()
    ax.text(x = p.get_x() + (p.get_width()/2),
    y = height+0.2, ha = 'center', s = '{:.0f}'.format(height))
plt.show()

"""We see the busiest hours are 6:00 pm to 7:00 pm and that makes sense as this is the time when people return from their offices.

1. The most busy hours  for taxi trip were between evening 18-22 hr
2. The least busy hours were between early morning 2-5 hr

##pickup/dropoff_month
"""

ax = sns.countplot(x = df['pickup_month'])
plt.title(' Distribution of  pick month')

for p in ax.patches:
    height = p.get_height()
    ax.text(x = p.get_x() + (p.get_width()/2),
    y = height+0.2, ha = 'center', s = '{:.0f}'.format(height))
plt.show()

ax = sns.countplot(x = df['dropoff_month'])
plt.title(' Distribution of total dropoff month')

for p in ax.patches:
    height = p.get_height()
    ax.text(x = p.get_x() + (p.get_width()/2),
    y = height+0.2, ha = 'center', s = '{:.0f}'.format(height))
plt.show()

"""1.The month of March has received the highest number of trips followed by April for both pickup/dropoff.

2.The least number of trips done in the month of January and July.

##Bivariate  Data Analysis

##Passenger Count and Vendor id
"""

sns.barplot(y='passenger_count',x='vendor_id',data=df)

"""This shows that vendor 2 generally carries 2 passengers while vendor 1 carries 1 passenger rides.

##Trip Duration per time zone
"""

sns.lineplot(x='pickup_timezone',y='trip_duration',data=df)

"""From the above lineplot we can say that, trip duration is the maximum in the afternoon and lowest between late night and morning.

##Trip Duration per different days
"""

sns.lineplot(x='pickup_day',y='trip_duration',data=df)

"""From the above line plot we can say that,the trip duration is the maximum in Wednesday and lowest on Sunday

##Number of trips per day
"""

df.groupby(df.pickup_datetime.dt.date).size().plot()
plt.title('Count of rides per day')
plt.ylabel('Count of rides per day')

"""The number of rides per day is cyclical with a dip in the rides during the night time.

The sudden dip in the taxi rides between the 20th and 26th Jan was because of the heavy snow that was observed during that period.

##Plotting average trip duration for each hour over the entire year and the average number of rides per hour
"""

#Plotting average trip duration for each hour over the entire year
ax1 = plt.subplot(211)
df.groupby(df.pickup_hour)['trip_duration'].mean().plot(ax = ax1, figsize=(10,6))
plt.ylabel('Trip duration in seconds')
plt.xticks(df.pickup_hour.unique())
plt.title('Trip duration in seconds averaged over hours in the year of 2016')

# Plotting the average number of rides per hour
ax2 = plt.subplot(212)
df.groupby(['pickup_date', 
                    'pickup_hour']).count()['vendor_id'].groupby('pickup_hour').mean().plot(ax = ax2, figsize=(10,6))
plt.ylabel('Average count of pickups per hour')
plt.xticks(df.pickup_hour.unique())
plt.title('Average count of pickups per hour in the year of 2016')
plt.tight_layout()

"""Note: Please notice that the y-axis doesn't start at 0.

As one would expect the trip duration and the number of rides are higher in the evening time. As the number of rides go up in a certain area one can expect the resulting traffic to slow down the traffic increasing the trip duration time.

From the 2nd plot we can see how the pickup rides increase steadily from 5am to 8am only to flatten out between 8am to 4pm and then again steeply increase from 4pm to 6pm to fall down later.

The average trip duration is around 15 minutes during the evening time.

## Finding correlation in variables (both dependent and independent, Visualizations on data using Heat Map
"""

df.corr()



## Correlation
plt.figure(figsize=(15,8))
correlation=df.corr()
sns.heatmap(abs(correlation), annot=True, cmap='coolwarm')

"""1. We can see a high correlation between pickup_month and dropoff_month,pickup_date and dropoff_date,pickup_weekday and dropoff_weekday.
2. Our target variable shows 0.78 percent correalation with distance.
3. pickup_hour and dropoff hour shows a correaltion of 0.68.
4. we drop time_diff_minutes since its highly correalted with trip_duration.
5. In all highly correalted features  we can only keep the pickup details and drop the dropoff details to remove multicollinearity.
"""



#Multicollinearity
from statsmodels.stats.outliers_influence import variance_inflation_factor
def calc_vif(X):

    # Calculating VIF
    vif = pd.DataFrame()
    vif["variables"] = X.columns
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

    return(vif)

calc_vif(df[[i for i in df.describe().columns if i  in [
 'passenger_count',
 'pickup_weekday',
 'pickup_hour',
 'pickup_month',
 'pickup_date','distance',
 'trip_direction']]])

"""#5.Feature Engineering

# Multivariate Normality Distribution check and Handling Skewness
"""

#  Check the distribution and handle the skewnwss if present
# Trip_Duration (Target Variable)
plt.figure(figsize=(10,15))
sns.distplot(df['trip_duration'])
plt.xlabel('trip_duration')

#Using log transform to bring it to normal distribution
plt.figure(figsize=(10,15))
sns.distplot(np.log(df['trip_duration']))
plt.xlabel('trip_duration')

numeric_features=df.describe().columns

numeric_features

# plot a bar plot for each numerical features

for col in numeric_features:
  fig = plt.figure(figsize=(9, 6))
  ax = fig.gca()
  feature = df[col]
  feature.hist(bins=50, ax = ax)
  ax.axvline(feature.mean(), color='magenta', linestyle='dashed', linewidth=2)
  ax.axvline(feature.median(), color='cyan', linestyle='dashed', linewidth=2)    
  ax.set_title(col)
plt.show()

"""Treating the skewness in the distance feature using log transform.

trip_speed,time_diff_minutes features are highly in correaltion with our target variable and it may result in data leakage and getting high accuracy near to 100 percentage hence we will not handle the skewness in these features and directly drop these features before model buliding
"""

plt.figure(figsize=(10,15))
sns.distplot(np.log(df['distance']))
plt.xlabel('distance')

"""# Check for Linearity"""

for col in numeric_features[:]:
    fig = plt.figure(figsize=(9, 6))
    ax = fig.gca()
    feature = df[col]
    label = df['trip_duration']
    correlation = feature.corr(label)
    plt.scatter(x=feature, y=label)
    plt.xlabel(col)
    plt.ylabel('trip_duration')
    ax.set_title('trip_duration vs ' + col + '- correlation: ' + str(correlation))
    z = np.polyfit(df[col], df['trip_duration'], 1)
    y_hat = np.poly1d(z)(df[col])

    plt.plot(df[col], y_hat, "r--", lw=1)

plt.show()

"""From above plot we can conclude that only trip_distance and trip_speed were having a linear relationship with trip_duration

# Encoding Categorical Features
"""

df_copy = df.copy()

df_copy.drop(labels=['dropoff_timezone','store_and_fwd_flag',],axis=1,inplace=True)

# One hot encoding on pickup_timezone feature
df_copy = pd.get_dummies(df_copy,columns=["pickup_timezone"],prefix=["pickup_timezone"])

df_copy.head()

"""Handling Skewness in numerical features using log Transform"""

df_copy['distance'] = df_copy['distance'].map(lambda x : np.log(x) if x != 0 else 0)

df_copy['pickup_month'] = df_copy['pickup_month'].map(lambda x : np.log(x) if x != 0 else 0)
df_copy['pickup_hour'] = df_copy['pickup_hour'].map(lambda x : np.log(x) if x != 0 else 0)
df_copy['passenger_count'] = df_copy['passenger_count'].map(lambda x : np.sqrt(x) if x != 0 else 0)

df_copy.shape

"""#6.Feature Selection

We cannot use all the columns from the dataframe because some of them are datetime and some of them were calculated based on the target variable such as trip_speed_mph.

So, we will use only the following columns:
cols_to_use = ['vendorid', 'passenger_count', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'pickup_month', 'pickup_weekday', 'pickup_hour', 'distance, 'trip_direction',  'trip_duration']
"""

features = ['vendor_id',
 'passenger_count',
 'pickup_longitude',
 'pickup_latitude',
 'dropoff_longitude',
 'dropoff_latitude',
 'pickup_weekday',
 'pickup_hour',
 'pickup_month',
 'pickup_date','distance',
 'trip_direction']

features.extend(['pickup_timezone_Afternoon', 'pickup_timezone_Evening',
       'pickup_timezone_Late night', 'pickup_timezone_Morning'])

features

X = df_copy[features] #Independent features
y = np.log(df_copy['trip_duration'])  #Dependent features

X.shape

"""**Lets split the data into train and test data**"""

from sklearn.model_selection import train_test_split 
X_train, X_test, y_train, y_test = train_test_split( X,y , test_size = 0.2, random_state = 42) 
print(X_train.shape)
print(X_test.shape)

from sklearn.preprocessing import StandardScaler
sc= StandardScaler()
X_train[features]=sc.fit_transform(X_train[features])
X_test[features]=sc.transform(X_test[features])

"""#Buliding a base model using Linear Regression 
We have many variables such as the pickup/dropoff month, weekday, hour of the day, trip direction which are not linear variables and can be difficult for a linear regression (LR) algorithm to model without first converting these variables to appropriate forms that can be fed to the LR models and understood by it. And, we also need to scale the data to prevent the dominance of larger magnitude variables in LR models.

Another alternative is we can use non-linear methods such as decision trees to fit the data. Decision tree doesn’t require us to convert the variables because it can split across any values of the variables and also, we don’t need to scale the data when using trees because each variable is considered separately for calculating the gain at each branching.

But before moving onto decision trees or random forest let’s check the performance of LR using only few significant variables which have vif values below 5,hence there will be no multicollinearirty 

We have to satisfy linear regression assumption inorder to use a linear regression model.

"""



calc_vif(df[[i for i in df.describe().columns if i  in [
 'passenger_count',
 'pickup_weekday',
 'pickup_hour',
 'pickup_month',
 'pickup_date','distance',
 'trip_direction']]])

features1= [
 'passenger_count',
 'pickup_weekday',
 'pickup_hour',
 'pickup_month',
 'pickup_date','distance','trip_direction'
 ]

features1

X1 = df_copy[features1] #Independent features
y1 = np.log(df_copy['trip_duration'])  #Dependent features

"""#7.Model Buliding
Linear regression (with only few variables), Decision Tree, Random Forest and XGBoost were fit on the NYC taxi trip data with additional features added from the EDA notebook. For training, only a small sample (500,000) of the ~4.2M trips was used but the best model was tested on the entire dataset to verify that the training sample was selected randomly and represents the entire dataset indeed.





"""

from sklearn.model_selection import train_test_split 
X1_train, X1_test, y1_train, y1_test = train_test_split( X1,y1 , test_size = 0.2, random_state = 42) 
print(X1_train.shape)
print(X1_test.shape)

from sklearn.preprocessing import StandardScaler
sc= StandardScaler()
X1_train[features1]=sc.fit_transform(X_train[features1])
X1_test[features1]=sc.transform(X_test[features1])

reg = LinearRegression().fit(X1_train, y1_train)

reg.score(X1_train, y1_train)

reg.coef_

reg.intercept_

# Predicting the Test set results using training data
y_pred_train = reg.predict(X1_train)

y_pred_train

"""## 8.**Regression Evaluation Metrics**

---



Comparing these metrics:

MAE is the easiest to understand, because it's the average error.
<br>MSE is more popular than MAE, because MSE "punishes" larger errors, which tends to be useful in the real world.
<br>RMSE is even more popular than MSE, because RMSE is interpretable in the "y" units.
<br>All of these are loss functions, because we want to minimize them.
"""

# Predicting the Test set results using test data
y_pred_test = reg.predict(X1_test)

y_pred_test

# Test performance using Evaluation metrics
MSE  = mean_squared_error((y_test), (y_pred_test))
print("MSE :" , MSE)

MAE=mean_absolute_error((y_test), (y_pred_test))
print("MAE :" ,MAE)

RMSE = np.sqrt(MSE)
print("RMSE :" ,RMSE)

r2 = r2_score((y_test), (y_pred_test))
print("R2 :" ,r2)
print("Adjusted R2 : ",1-(1-r2_score((y_test), (y_pred_test)))*((X_test.shape[0]-1)/(X_test.shape[0]-X_test.shape[1]-1)))

"""#Plotting a Scatter plot on Actual vs Predicted trip duration Values"""

plt.scatter((y_test), (y_pred_test))
plt.xlabel('Actual trip duration')
plt.ylabel('Predicted trip duration')

plt.figure(figsize=(15,10))
plt.plot((y_pred_test))
plt.plot(np.array((y_test)))
plt.legend(["Predicted","Actual"])
plt.xlabel('No of Test Data')
plt.show()

"""If we see above graph our prediction is quiet good.

# **Residuals:**

---
A residual is the vertical distance between a data point and the regression line. Each data point has one residual. They are positive if they are above the regression line and negative if they are below the regression line
"""

fig=plt.figure(figsize=(8,8))
  
sns.distplot(((y_test)- (y_pred_test)),bins=20)

#Plot Label
fig.suptitle('Residual Analysis', fontsize = 20)

### Heteroscadacity
plt.scatter((y_pred_test),(y_test)-(y_pred_test))
plt.xlabel('Predicted trip_duration')
plt.ylabel('residuals')

"""## **Implementing Lasso regression**

---
Lasso regression is a type of linear regression that uses shrinkage. Shrinkage is where data values are shrunk towards a central point, like the mean. The lasso procedure encourages simple, sparse models (i.e. models with fewer parameters).
"""

from sklearn.linear_model import Lasso
lasso  = Lasso(alpha=0.005 , max_iter= 3000)

lasso.fit(X_train, y_train)

lasso.score(X_train, y_train)

y_pred_l = lasso.predict(X_test)

MSE  = mean_squared_error((y_test), (y_pred_l))
print("MSE :" , MSE)

MAE=mean_absolute_error((y_test), (y_pred_l))
print("MAE :" ,MAE)

RMSE = np.sqrt(MSE)
print("RMSE :" ,RMSE)

r2 = r2_score((y_test), (y_pred_l))
print("R2 :" ,r2)
print("Adjusted R2 : ",1-(1-r2_score((y_test), (y_pred_l)))*((X_test.shape[0]-1)/(X_test.shape[0]-X_test.shape[1]-1)))

plt.scatter((y_test), (y_pred_l))
plt.xlabel('Actual trip duration')
plt.ylabel('Predicted trip duration')

plt.figure(figsize=(15,10))
plt.plot((y_pred_l))
plt.plot(np.array((y_test)))
plt.legend(["Predicted","Actual"])
plt.show()

#Resuldual Analysis
fig=plt.figure(figsize=(8,8))
  
sns.distplot(((y_test)- (y_pred_l)),bins=20,color='r')

#Plot Label
fig.suptitle('Residual Analysis', fontsize = 20)

### Heteroscadacity
plt.scatter((y_pred_l),(y_test)-(y_pred_l),c='r')
plt.xlabel('Predicted trip duration')
plt.ylabel('residuals')

"""#Ridge"""

from sklearn.linear_model import Ridge

ridge  = Ridge(alpha=0.1)

ridge.fit(X_train,y_train)

ridge.score(X_train, y_train)

y_pred_r = ridge.predict(X_test)

MSE  = mean_squared_error((y_test), (y_pred_r))
print("MSE :" , MSE)

MAE=mean_absolute_error((y_test), (y_pred_r))
print("MAE :" ,MAE)

RMSE = np.sqrt(MSE)
print("RMSE :" ,RMSE)

r2 = r2_score((y_test), (y_pred_r))
print("R2 :" ,r2)
print("Adjusted R2 : ",1-(1-r2_score((y_test), (y_pred_r)))*((X_test.shape[0]-1)/(X_test.shape[0]-X_test.shape[1]-1)))

plt.scatter((y_test), (y_pred_r))
plt.xlabel('Actual trip duration')
plt.ylabel('Predicted trip duration')

plt.figure(figsize=(12,8))
plt.plot((y_pred_r))
plt.plot((np.array(y_test)))
plt.legend(["Predicted","Actual"])
plt.show()

#Resuldual Analysis
fig=plt.figure(figsize=(8,8))
  
sns.distplot(((y_test)- (y_pred_r)),bins=20,color='r')

#Plot Label
fig.suptitle('Residual Analysis', fontsize = 20)

### Heteroscadacity
plt.scatter((y_pred_r),(y_test)-(y_pred_r),c='r')
plt.xlabel('Predicted trip duration')
plt.ylabel('residuals')

"""#Decision Tree"""

from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score

des_regressor = DecisionTreeRegressor(random_state=10)
cross_val_score(des_regressor, X_train, y_train, cv=5).mean()

des_regressor.fit(X_train,y_train)

y_pred_des = des_regressor.predict(X_test)

#Evaluating the model using regression metrics
MSE  = mean_squared_error((y_test), (y_pred_des))
print("MSE :" , MSE)

MAE=mean_absolute_error((y_test), (y_pred_des))
print("MAE :" ,MAE)

RMSE = np.sqrt(MSE)
print("RMSE :" ,RMSE)

r2 = r2_score((y_test), (y_pred_des))
print("R2 :" ,r2)
print("Adjusted R2 : ",1-(1-r2_score((y_test), (y_pred_des)))*((X_test.shape[0]-1)/(X_test.shape[0]-X_test.shape[1]-1)))

#Scatter plot vs Actual & Predicted trip duration Values
plt.scatter((y_test), (y_pred_des))
plt.xlabel('Actual trip duration')
plt.ylabel('Predicted trip duration')

plt.figure(figsize=(12,8))
plt.plot((y_pred_des))
plt.plot((np.array(y_test)))
plt.legend(["Predicted","Actual"])
plt.show()

"""We have used RandomForest Ensemble Algo (bagging) and Xgboost Ensemble Algo(boosting) techniques

#Random Forest
Using RandomForest Ensemble technique to predict the trip_duration after applying hyperparameter tuning with help of RandomSearchcv (cross-validation technique)
Max depth and n estimator were the parameters we have selected with crossvalidation value 3 because if we add more parameters it will take  high computation time. 

It nearly took us 1.5hrs to run this Randomizedsearchcv hyperparameter tunning,so adding more parameters and cv value will increase time complexity.

So this hyperparameter tunning can be improved with adding more parameters and crossvalidation score to 5 or more to get a more refined model.We can also use Gridsearchcv for hyperparameter tunning
"""

#importing reqd libraries
from sklearn.ensemble import RandomForestRegressor

rf= RandomForestRegressor()

#Setting various parameter for hyperparameter tuning
param_dict_rf = {
    'max_depth': [4, 6, 8],
 'n_estimators': [80, 100]
  }

rf_random = RandomizedSearchCV(estimator=rf,
                       param_distributions = param_dict_rf,
                       cv = 3, verbose=2)

"""Fitting the model to train data"""

rf_random.fit(X_train,y_train)

# print the best parameters after cross validation
print(rf_random.best_params_)

print('Train  neg_mean_squared_error score : ', rf_random.best_estimator_.score(X_train,y_train))
print('Test neg_mean_squared_error score: ', rf_random.best_estimator_.score(X_test,y_test))

y_pred_rf = rf_random.predict(X_test)

#Evaluating the model using regression metrics
MSE  = mean_squared_error((y_test), (y_pred_rf))
print("MSE :" , MSE)

MAE=mean_absolute_error((y_test), (y_pred_rf))
print("MAE :" ,MAE)

RMSE = np.sqrt(MSE)
print("RMSE :" ,RMSE)

r2 = r2_score((y_test), (y_pred_rf))
print("R2 :" ,r2)
print("Adjusted R2 : ",1-(1-r2_score((y_test), (y_pred_rf)))*((X_test.shape[0]-1)/(X_test.shape[0]-X_test.shape[1]-1)))

"""#XGBOOST

Using XGboost Ensemble technique to predict the trip_duration after applying hyperparameter tuning with help of RandomSearchcv (cross-validation technique)
"""

#importing reqd libraries
import xgboost as xg

xgb = xg.XGBRegressor()

#Setting various parameter for hyperparameter tuning
param_dict_xgb = {
    'max_depth': [4, 6, 8],
 'n_estimators': [60, 100]
  }

xgb_random = RandomizedSearchCV(estimator=xgb,
                       param_distributions = param_dict_xgb,
                       cv = 5, verbose=2)

xgb_random.fit(X_train,y_train)

# print the best parameters after cross validation
xgb_random.best_params_

print('Train neg_mean_squared_error score score : ', xgb_random.best_estimator_.score(X_train,y_train))
print('Test neg_mean_squared_error score score : ', xgb_random.best_estimator_.score(X_test,y_test))

y_pred_xg = xgb_random.predict(X_test)

#Evaluating the model using regression metrics
MSE  = mean_squared_error((y_test), (y_pred_xg))
print("MSE :" , MSE)

MAE=mean_absolute_error((y_test), (y_pred_xg))
print("MAE :" ,MAE)

RMSE = np.sqrt(MSE)
print("RMSE :" ,RMSE)

r2 = r2_score((y_test), (y_pred_xg))
print("R2 :" ,r2)
print("Adjusted R2 : ",1-(1-r2_score((y_test), (y_pred_xg)))*((X_test.shape[0]-1)/(X_test.shape[0]-X_test.shape[1]-1)))

"""#Comparing negative mean square error in different models """

from numpy import mean
from numpy import std
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from sklearn.datasets import make_regression
from matplotlib import pyplot
 
# get the dataset
def get_dataset():
	X, y = make_regression(n_samples=1000, n_features=10, n_informative=15, random_state=1)
	return X, y
 
# get a list of models to evaluate
def get_models():
	models = dict()
	models['Ridge'] = Ridge()
	models['Lasso'] = Lasso()
	models['DecisionTree'] = DecisionTreeRegressor()
	models['Random_forest'] = RandomForestRegressor()
	models['XGBoost'] = xg.XGBRegressor()

	return models
 
# evaluate a given model using cross-validation
def evaluate_model(model, X, y):
	cv =  RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
	scores = cross_val_score(model, X, y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1, error_score='raise')
	return scores
 
# define dataset
X, y = get_dataset()
# get the models to evaluate
models = get_models()
# evaluate the models and store results
results, names = list(), list()
for name, model in models.items():
	scores = evaluate_model(model, X, y)
	results.append(scores)
	names.append(name)
	print('>%s %.3f (%.3f)' % (name, mean(scores), std(scores)))
# plot model performance for comparison
pyplot.boxplot(results, labels=names, showmeans=True)
pyplot.show()

"""# . Conclusion



1.Our base model (Linear Regression) gave us a r2_score of 0.67 in train and test data and keep this model accuracy in reference to compare other model.

2.We got the best model accuracy in Xgboost model,r2 score of 0.84 in training set and 0.83 in test data..The RMSE score of Xgboost model is 0.282

3.Our second best model is  RandomForestbased with a r2 score of 0.7485 accuracy in training and 0.7475 accuracy in test data. The RMSE score of random forest is 0.350

4.Decision Tree has given us least score in evaluation compared to all other algorithms based on negative mean absloute error and r2 score.


5.We just used ensemble techniques over here to demonstrate various other options for these kind of regression problems and to make the project little bit more informative.

6.We can also do Model Explainability  of random forest and Xgboost model over here using SHAP or LIME .But our team intention was not to make it more lengthy hence we restricted ourseleves till here. 

7.results in ridge and lasso regularized linear regression algorithm based on negative mean absoulte error is good compared to other models

"""