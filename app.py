import pyrebase
from flask import Flask, request, render_template

config = {
    "apiKey": "AIzaSyB9M98Yk7DpPAyaZ72ShIeEySbn1evp64g",
    "authDomain": "rifas-934aa.firebaseapp.com",
    "databaseURL": "https://rifas-934aa.firebaseio.com",
    "projectId": "rifas-934aa",
    "storageBucket": "rifas-934aa.appspot.com",
    "messagingSenderId": "722084525985"
}
app = Flask(__name__)

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def index():
    unsuccessful = 'Please check yours credentias'
    # success = 'Login successful'
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            # print(user)
            return render_template('dashboard.html', u=user)
        except:
            return render_template('login.html', us=unsuccessful)
            
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    unsuccessful = 'Please check yours credentias'
    success = 'The account has been created successful'
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # passwordConfirm = request.form['passwordConfirm']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            auth.send_email_verification(user['idToken'])
            # print(user)
            # userToken = auth.get_account_info(user['idToken'])
            # success = success+ ' ' + userToken['email']
            # print(userToken)
            return render_template('register.html', s=success)
        except:
            return render_template('register.html', us=unsuccessful)

    return render_template('register.html')

@app.route('/sorteo', methods=['GET', 'POST'])
def store():
    if request.method == 'POST':
        date = request.form['date']
        premio = request.form['premio']
        numbers = request.form['numbers']
        price = request.form['price']

        # db.child('sorteos').push({'date':'date'})
        # db.child('sorteos').push({'premio':'premio'})
        # db.child('sorteos').push({'numbers':'numbers'})
        # db.child('sorteos').push({'price':'price'})
        db.child('sorteos').push({'date':date, 'premio':premio, 'numbers':numbers, 'price':price})
        sorteo = db.child("sorteos").get()
        sor = sorteo.val()
        return render_template('dashboard.html', s=sor.values())

    sorteo = db.child("sorteos").get()
    sor = sorteo.val()
    return render_template('dashboard.html', s=sor.values())



if __name__ == '__main__':
    app.run(debug=True) 