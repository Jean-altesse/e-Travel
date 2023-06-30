from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    agree_terms = db.Column(db.Boolean, nullable=False)

@app.route('/')
def index():
    return render_template('accueil.html')

@app.route('/a_propos') 
def a_propos():
    return render_template('a_propos.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        agree_terms = 'agree_terms' in request.form

        user = User(email=email, phone=phone, password=password, first_name=first_name,
                    last_name=last_name, gender=gender, agree_terms=agree_terms)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('connexion'))
    return render_template('inscription.html')

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user is not None and user.password == password:
            return redirect(url_for('accueil'))
    return render_template('connexion.html')

@app.route('/accueil', methods=['GET', 'POST'])
def accueil():
    email = request.args.get('email')
    return render_template('connexion.html', email=email)

if __name__ == '__main__':
    app.run()
