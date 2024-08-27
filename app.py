from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import pandas as pd

# Load the trained model
model = joblib.load('laptop_price_model.pkl')

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Extract values from JSON
        brand = data['brand']
        ram = int(data['ram'])
        storage = int(data['storage'])
        processor = int(data['processor'])
        gpu = data['gpu']
        os = data['os']

        # Prepare the input data for prediction in DataFrame format
        input_data = pd.DataFrame([[brand, ram, storage, processor, gpu, os]], 
                                  columns=['Brand', 'RAM', 'Storage', 'Processor', 'GPU', 'Operating System'])

        # Note: Ensure that the columns are consistent with the model's training data

        # Predict using the model
        prediction = model.predict(input_data)[0]

        # Return the result as JSON
        return jsonify({'prediction': round(prediction, 2)})
    except Exception as e:
        print("Error during prediction:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
