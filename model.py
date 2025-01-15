import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load dataset
data = pd.read_csv('flight_fare_data.csv')

# Preprocessing
def preprocess_data(df):
    # Handle missing values
    df = df.dropna()

    # Extract date-related features
    df['Journey_day'] = pd.to_datetime(df['Date_of_Journey']).dt.day
    df['Journey_month'] = pd.to_datetime(df['Date_of_Journey']).dt.month
    df.drop(['Date_of_Journey'], axis=1, inplace=True)

    # Extract departure and arrival time features
    df['Dep_hour'] = pd.to_datetime(df['Dep_Time']).dt.hour
    df['Dep_min'] = pd.to_datetime(df['Dep_Time']).dt.minute
    df.drop(['Dep_Time'], axis=1, inplace=True)

    df['Arrival_hour'] = pd.to_datetime(df['Arrival_Time']).dt.hour
    df['Arrival_min'] = pd.to_datetime(df['Arrival_Time']).dt.minute
    df.drop(['Arrival_Time'], axis=1, inplace=True)

    # Convert duration to minutes
    df['Duration'] = df['Duration'].apply(lambda x: int(x.split()[0][:-1]) * 60 + int(x.split()[1][:-1]) if 'h' in x else int(x.split()[0][:-1]))

    # Encode categorical variables
    df = pd.get_dummies(df, columns=['Airline', 'Source', 'Destination', 'Route', 'Additional_Info'], drop_first=True)

    return df

# Apply preprocessing
data = preprocess_data(data)

# Split data into features and target
X = data.drop('Price', axis=1)
y = data['Price']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"Mean Absolute Error: {mae}")
print(f"Mean Squared Error: {mse}")
print(f"Root Mean Squared Error: {rmse}")

# Save the model
import joblib
joblib.dump(model, 'flight_fare_model.pkl')
