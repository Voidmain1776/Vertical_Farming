import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


# Simulated data generation
np.random.seed(42)
num_samples = 1000

temperature = np.random.uniform(20, 35, num_samples)
humidity = np.random.uniform(30, 80, num_samples)
moisture = np.random.uniform(0.1, 0.9, num_samples)
ph = np.random.uniform(5.5, 7.5, num_samples)
light_intensity = np.random.uniform(2000, 8000, num_samples)

# Simulated relationship between environmental variables and crop yield
true_yield = 10 * temperature + 5 * humidity + 3 * moisture + 2 * ph + 0.5 * light_intensity
noise = np.random.normal(0, 10, num_samples)
observed_yield = true_yield + noise

# Simulated crop health categories (0 - Very Poor, 1 - Poor, 2 - Fair, 3 - Good, 4 - Excellent)
crop_health = np.random.randint(0, 5, num_samples)

# Creating a DataFrame
data = pd.DataFrame({
    'temperature': temperature,
    'humidity': humidity,
    'moisture': moisture,
    'phlevel': ph,
    'lux': light_intensity,
    'TrueYield': true_yield,
    'ObservedYield': observed_yield,
    'CropHealth': crop_health
})

# Splitting data into training and testing sets
X = data[['temperature', 'humidity', 'moisture', 'phlevel', 'lux']]
y_yield = data['ObservedYield']
y_health = data['CropHealth']
X_train, X_test, y_train_yield, y_test_yield, y_train_health, y_test_health = train_test_split(
    X, y_yield, y_health, test_size=0.2, random_state=42
)

# Creating and training a linear regression model for yield prediction
yield_model = LinearRegression()
yield_model.fit(X_train, y_train_yield)

# Making yield predictions
y_pred_yield = yield_model.predict(X_test)

# Model evaluation for yield prediction
mse_yield = mean_squared_error(y_test_yield, y_pred_yield)
print(f"Mean Squared Error for Yield Prediction: {mse_yield:.2f}")



# Saving the yield model using joblib
joblib.dump(yield_model, 'yield_model.pkl')





# Creating and training a decision tree classifier for health prediction
health_classifier = DecisionTreeClassifier()
health_classifier.fit(X_train, y_train_health)

# Making health predictions
y_pred_health = health_classifier.predict(X_test)

# Model evaluation for health prediction
accuracy = accuracy_score(y_test_health, y_pred_health)
print(f"Accuracy for Health Prediction: {accuracy:.2f}")

# Saving the health classifier using joblib
joblib.dump(health_classifier, 'health_classifier.pkl')