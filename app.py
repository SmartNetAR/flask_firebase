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
            # print(auth.current_user)
            # print(auth.current_user)
            uid = user['localId']
            sorteos = db.child("sorteos").child(uid).get()
            sor = sorteos.val()
            return render_template('dashboard.html', s=sor.values(), u=user)
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
            print(auth.current_user)
            return render_template('register.html', us=unsuccessful)

    return render_template('register.html')

@app.route('/sorteo', methods=['GET', 'POST'])
def store():
    if request.method == 'POST':
        # user = auth.get_account_info(id_token)
        # user = auth.sign_in_with_email_and_password('jonathan@smartnet.com.ar', '123456')
        # print('id_token: ' + request.id_token)
        # print('request token: ' + request.form['token'])
        token = request.form['token']
        account_info = auth.get_account_info(token)
        #user = account_info['users']
        user = auth.current_user
        date = request.form['date']
        premio = request.form['premio']
        numbers = request.form['numbers']
        price = request.form['price']
        # uid = user[0]['localId']
        uid = user['localId']
        sorteo = {'date':date, 'premio':premio, 'numbers':numbers, 'price':price}
        db.child('sorteos').child(uid).push(sorteo, user['idToken'])
        sorteos = db.child("sorteos").child(uid).get()
        sor = sorteos.val()
        return render_template('dashboard.html', s=sor.values(), u=user)

    user = auth.sign_in_with_email_and_password('leonardo@smartnet.com.ar', 'SAeempdm0036')
    uid = user['localId']
    sorteos = db.child("sorteos").child(uid).get()
    sor = sorteos.val()
    return render_template('dashboard.html', s=sor.values(), u=user)



if __name__ == '__main__':
    app.run(debug=True) 