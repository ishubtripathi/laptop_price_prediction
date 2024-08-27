# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import re  # Import the regular expression module

# Load the dataset
df = pd.read_csv('laptop_prices.csv')  # Ensure this dataset is correctly named

# Remove leading/trailing spaces from column names
df.columns = df.columns.str.strip()

# Print column names to debug
print("Columns in the dataset after stripping spaces:", df.columns.tolist())

# Display unique values in the 'Storage' column for debugging
print("Unique values in 'Storage' column before cleaning:", df['Storage'].unique())

# Basic preprocessing
try:
    # Clean 'RAM' column
    df['RAM'] = df['RAM'].str.replace('GB', '').astype(int)

    # Clean 'Storage' column
    df['Storage'] = df['Storage'].apply(lambda x: int(re.search(r'\d+', x).group()) if pd.notna(x) else 0)

    # Map 'Processor' values
    df['Processor'] = df['CPU'].apply(lambda x: 1 if 'i3' in x else (2 if 'i5' in x else 3))  # Example mapping based on CPU

    # Convert 'Price (Euros)' column to float after replacing commas with dots
    df['Price (Euros)'] = df['Price (Euros)'].str.replace(',', '.').astype(float)
except KeyError as e:
    print(f"Column not found: {e}")
    print("Please check if all columns are correctly named and present in the dataset.")
    exit()
except ValueError as e:
    print(f"Value error: {e}")
    print("Please check the data formatting in the columns.")
    exit()

# Print cleaned data for verification
print("Data after cleaning:", df[['RAM', 'Storage', 'Processor', 'Price (Euros)']].head())

# Define features and target
X = df[['RAM', 'Storage', 'Processor']]  # Feature columns
y = df['Price (Euros)']  # Target column

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Save the model to a file
joblib.dump(model, 'laptop_price_model.pkl')

print("Model training complete and saved to laptop_price_model.pkl.")
