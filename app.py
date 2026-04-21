from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import pickle

app = Flask(__name__)

# Load your XGBoost model
model = pickle.load(open('xgb.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        quarter = request.form['quarter']
        department = request.form['department']
        day = request.form['day']
        team = request.form['team']
        targeted_productivity = request.form['targeted_productivity']
        smv = request.form['smv']
        over_time = request.form['over_time']
        incentive = request.form['incentive']
        idle_time = request.form['idle_time']
        idle_men = request.form['idle_men']
        no_of_style_change = request.form['no_of_style_change']
        no_of_workers = request.form['no_of_workers']
        month = request.form['month']

        # 2. Convert inputs to float (important for ML models)
        total = [[
            float(quarter), float(department), float(day), float(team), 
            float(targeted_productivity), float(smv), float(over_time), 
            float(incentive), float(idle_time), float(idle_men), 
            float(no_of_style_change), float(no_of_workers), float(month)
        ]]
        
        # 3. Predict
        prediction = model.predict(total)
        
        # 4. Logic for output text
        if prediction <= 0.3:
            text = 'The Employee is averagely productive'
        elif 0.3 < prediction <= 0.8:
            text = 'The Employee is medium productive'
        else:
            text = 'The Employee is highly productive'
            
        return render_template('submit.html', prediction_text=text)
    
    # If it's a GET request, just show the predict page
    return render_template('predict.html')

if __name__ == '__main__':
    app.run(debug=True)