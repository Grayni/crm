from flask import Flask, flash, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ums.sqlite"
app.config['SECRET_KEY'] = "1a874f6bd0c7166d732b5acd"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# User Class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    edu = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f'User("{self.id}", "{self.lname}", "{self.fname}", "{self.email}", "{self.email}", "{self.username}", "{self.edu}", "{self.status}")'


# create table
with app.app_context():
    # create table
    db.create_all()


# main index
@app.route('/')
def index():
    return render_template('index.html', title='test2')


# admin login
@app.route('/admin/')
def adminIndex():
    return render_template('admin/index.html', title='Admin Login')


# --------------- user area -----------------------

# user login
@app.route('/user/')
def userIndex():
    return render_template('user/index.html', title='User Login')


# user registration
@app.route('/user/signup', methods=['POST', 'GET'])
def userSignup():
    if request.method == 'POST':
        # get all input field name
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        username = request.form.get('username')
        edu = request.form.get('edu')
        password = request.form.get('password')

        # check all the field is filled are not
        if fname == "" or lname == "" or email == "" or password == "" or username == "" or edu == "":
            flash('Please fill all the field', 'danger')
            return redirect('/user/signup')
        else:
            is_email = User.query.filter_by(email=email).first()
            if is_email:
                flash('Email already Exist', 'danger')
                return redirect('/user/signup')
            else:
                hash_password = bcrypt.generate_password_hash(password, 10)
                user = User(fname=fname, lname=lname, email=email, password=hash_password, edu=edu, username=username)
                db.session.add(user)
                db.session.commit()
                flash('Account Create Successfully Admin Will approve your account in 10 to 30 minutes', 'success')
                return redirect('/user/')
    else:
        return render_template('user/signup.html', title='User Signup')


if __name__ == "__main__":
    app.run(debug=True)
