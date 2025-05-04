from flask import Flask, render_template, request, jsonify
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
        return render_template('index.html', prediction_text="Please enter valid numeric values for all features.")
    
    if len(features) != 11:
        return render_template('index.html', prediction_text="Please make sure to enter all 11 features.")
    
    final_features = np.array(features).reshape(1, -1)
    raw_pred = rf.predict(final_features)[0]
    message = "The account is Genuine ✅" if raw_pred == 0 else "The account is Fake ❌"
    
    return render_template('index.html', prediction_text=message)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        data = request.get_json(force=True)
        features = [float(data[f]) for f in sorted(data.keys())]
        prediction = rf.predict([features])[0]
        result = "Genuine ✅" if prediction == 0 else "Fake ❌"
        return jsonify({'prediction': result})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
