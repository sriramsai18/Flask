from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import pickle
import os # Added for path handling

app = Flask(__name__)

# --- CRITICAL CHANGE FOR VERCEL ---
# This finds the xgb.pkl file regardless of where the script runs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, '../xgb.pkl') 
model = pickle.load(open(model_path, 'rb'))
# ----------------------------------

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # (Your existing logic is perfect)
        total = [[
            float(request.form['quarter']), float(request.form['department']), 
            float(request.form['day']), float(request.form['team']), 
            float(request.form['targeted_productivity']), float(request.form['smv']), 
            float(request.form['over_time']), float(request.form['incentive']), 
            float(request.form['idle_time']), float(request.form['idle_men']), 
            float(request.form['no_of_style_change']), float(request.form['no_of_workers']), 
            float(request.form['month'])
        ]]
        
        prediction = model.predict(total)
        
        if prediction <= 0.3:
            text = 'The Employee is averagely productive'
        elif 0.3 < prediction <= 0.8:
            text = 'The Employee is medium productive'
        else:
            text = 'The Employee is highly productive'
            
        return render_template('submit.html', prediction_text=text)
    
    return render_template('predict.html')

# Vercel doesn't use app.run(), but keeping this won't hurt local testing
if __name__ == '__main__':
    app.run(debug=True)
