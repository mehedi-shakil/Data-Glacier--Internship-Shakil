from flask import Flask, render_template, request
import pickle
import numpy as np

# Load the trained model
with open('fake_instagram_model.pkl', 'rb') as f:
    rf = pickle.load(f)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Try to grab the input features and convert to float
    try:
        features = [float(x) for x in request.form.values()]
    except ValueError:
        # If there is an error in conversion, return the same template with an error message
        return render_template('index.html', prediction_text="Please enter valid numeric values for all features.")
    
    # Check if the correct number of features is entered (11 features)
    if len(features) != 11:
        return render_template('index.html', prediction_text="Please make sure to enter all 11 features.")
    
    # Convert features to numpy array for prediction
    final_features = np.array(features).reshape(1, -1)

    # Model prediction (0 or 1)
    raw_pred = rf.predict(final_features)[0]

    # Map to friendly text
    if raw_pred == 0:
        message = "The account is Genuine ✅"
    else:
        message = "The account is Fake ❌"

    # Send the result back to the page
    return render_template('index.html', prediction_text=message)

if __name__ == '__main__':
    app.run(debug=True)

