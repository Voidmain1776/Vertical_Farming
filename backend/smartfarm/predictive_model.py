# preprocess_train.py

import pandas as pd
from sklearn.linear_model import LinearRegression
import os
import django
import joblib




# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartfarm.settings')  # Replace with your project's settings module
django.setup()


from backend.models import SensorData  # Import your Django model



# Fetch historical data from the Django model
data = SensorData.objects.all().order_by('timestamp')  # Assuming timestamp is the time column
df = pd.DataFrame(list(data.values()))
print(df.columns)
# Assuming columns: timestamp, temperature, humidity, moisture, pH
# df.drop(['id'],axis=1, inplace=True)
# Create time-based features if needed (e.g., hour of day, day of week)

# Prepare data for training (X: features, y: target)
X = df.drop(['timestamp', 'temperature', 'humidity', 'moisture', 'phlevel','lux'], axis=1)
y_temp = df['temperature']
y_humidity = df['humidity']
y_moisture = df['moisture']
y_pH = df['phlevel']
y_lux = df['lux']


# Train models for each variable
model_temp = LinearRegression()
model_temp.fit(X, y_temp)

model_humidity = LinearRegression()
model_humidity.fit(X, y_humidity)

model_moisture = LinearRegression()
model_moisture.fit(X, y_moisture)

model_pH = LinearRegression()
model_pH.fit(X, y_pH)

model_lux = LinearRegression()
model_lux.fit(X, y_lux)

# Save the trained models
joblib.dump(model_temp, 'model_temp.pkl')
joblib.dump(model_humidity, 'model_humidity.pkl')
joblib.dump(model_moisture, 'model_moisture.pkl')
joblib.dump(model_pH, 'model_pH.pkl')
joblib.dump(model_pH, 'model_lux.pkl')