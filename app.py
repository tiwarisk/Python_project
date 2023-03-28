from flask import Flask, render_template, request, flash, redirect
import pickle
import numpy as np


app = Flask(__name__)

model = pickle.load(open("randForest.pkl", "rb"))

model3 = pickle.load(open("adaBoost.pkl", "rb"))

model2 = pickle.load(open("xgBoost.pkl", 'rb'))

def predict_default(features):

    features1 = np.array(features).astype(np.float64).reshape(1,-1)
    
    if(request.form.get('MODEL')== 1):
        prediction = model3.predict(features1)
        probability = model3.predict_proba(features1)
    elif(request.form.get('MODEL')== 2):
        prediction = model.predict(features)
        probability = model.predict_proba(features1)
    else:
        prediction = model.predict(features1)
        probability = model.predict_proba(features1)
    

    return prediction, probability

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/form", methods = ['GET','POST'])
def form():

    education_status = ["GRADUATE", "UNIVERSITY", "HIGH SCHOOL", "OTHERS", "DONT WANT TO SPECIFY"]
    marital_status = ["MARRIED","SINGLE"]

    payment_status = [
        "PAYED 1 MONTH AHEAD",
        "PAYED DULY",
        "PAYMENT DELAY FOR 1 MONTHS",
        "PAYMENT DELAY FOR 2 MONTHS",
        "PAYMENT DELAY FOR 3 MONTHS",
        "PAYMENT DELAY FOR 4 MONTHS",
        "PAYMENT DELAY FOR 5 MONTHS",
        "PAYMENT DELAY FOR 6 MONTHS",
        "PAYMENT DELAY FOR 7 MONTHS",
        "PAYMENT DELAY FOR 8 MONTHS",   
    ]

    alert_message = False
    success_message = False

    if request.method == 'POST':

        features = request.form.to_dict()
        features['EDUCATION'] = education_status.index(features['EDUCATION']) + 1
        features['MARRIAGE'] = marital_status.index(features['MARRIAGE']) + 1
        features['PAY_0'] = payment_status.index(features['PAY_0']) - 1
        features['PAY_2'] = payment_status.index(features['PAY_2']) - 1
        features['PAY_3'] = payment_status.index(features['PAY_3']) - 1
        features['PAY_4'] = payment_status.index(features['PAY_4']) - 1
        features['PAY_5'] = payment_status.index(features['PAY_5']) - 1
        features['PAY_6'] = payment_status.index(features['PAY_6']) - 1

        actual_feature_names = ['LIMIT_BAL', 'EDUCATION', 'MARRIAGE', 'AGE', 'GENDER', 'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6','BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']
        feature_values = [features[i] for i in actual_feature_names]
        data = [int(i) for i in feature_values]
        print(data)

        prediction, probability = predict_default(feature_values)
        print(prediction)
        if prediction[0] == 1:
            alert_message = "This account will be defaulted with a probability of {}%.".format(round(np.max(probability)*100, 2))
        else:
            success_message = "This account will not be defaulted with a probability of {}%.".format(round(np.max(probability)*100, 2))

    return render_template("form.html", education_status = education_status, marital_status = marital_status, payment_status = payment_status, alert_message = alert_message, success_message = success_message)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port =8080)