from flask import Flask, request, render_template
import firebase_admin
from firebase_admin import credentials, db
import pickle
import numpy as np

app = Flask(__name__)

# Initialize Firebase app
cred = credentials.Certificate("loan-approval-d0a30-firebase-adminsdk-js1cf-e1fef925d0.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://loan-approval-d0a30-default-rtdb.firebaseio.com/'
})
ref = db.reference('contactForm')

model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Save data to Firebase
        new_message_ref = ref.push({
            'name': name,
            'email': email,
            'message': message
        })

        return render_template('contact.html', success=True)
    else:
        return render_template('contact.html', success=False)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method ==  'POST':
        # Extracting form data
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        credit = float(request.form['credit'])
        area = request.form['area']
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])

        # Preprocessing form data
        # gender
        if gender == "Male":
            male = 1
        else:
            male = 0
        
        # married
        if married == "Yes":
            married_yes = 1
        else:
            married_yes = 0

        # dependents
        if dependents == '1':
            dependents_1 = 1
            dependents_2 = 0
            dependents_3 = 0
        elif dependents == '2':
            dependents_1 = 0
            dependents_2 = 1
            dependents_3 = 0
        elif dependents == "3+":
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 1
        else:
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 0  

        # education
        if education == "Not Graduate":
            not_graduate = 1
        else:
            not_graduate = 0

        # employed
        if employed == "Yes":
            employed_yes = 1
        else:
            employed_yes = 0

        # property area
        if area == "Semiurban":
            semiurban = 1
            urban = 0
        elif area == "Urban":
            semiurban = 0
            urban = 1
        else:
            semiurban = 0
            urban = 0

        ApplicantIncomelog = np.log(ApplicantIncome)
        totalincomelog = np.log(ApplicantIncome + CoapplicantIncome)
        LoanAmountlog = np.log(LoanAmount)
        Loan_Amount_Termlog = np.log(Loan_Amount_Term)

        prediction = model.predict([[credit, ApplicantIncomelog, LoanAmountlog, Loan_Amount_Termlog, 
                                      totalincomelog, male, married_yes, dependents_1, dependents_2, 
                                      dependents_3, not_graduate, employed_yes, semiurban, urban]])

        if prediction == "N":
            prediction = "No"
        else:
            prediction = "Yes"

        return render_template("prediction.html", prediction_text="Loan status is {}".format(prediction))

    else:
        return render_template("prediction.html")

if __name__ == "__main__":
    app.run(debug=True)
