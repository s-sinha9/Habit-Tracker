import datetime

from flask import Flask, render_template, request, session, make_response

from src.common.database import Database
from src.models.dailys import Daily
from src.models.goals import Goal
from src.models.hours import Hour
from src.models.user import User

app = Flask(__name__)
app.secret_key="shubham"

@app.route('/')
def home_template():
    return render_template('home.html')


@app.route('/login')
def login_template():
    return render_template('login.html')


@app.route('/register')
def register_template():
    return render_template('register.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None
        return render_template("login.html", text="Wrong Username or Password")


    return render_template("profile.html", email=session['email'])


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)

    return render_template("profile.html", email=session['email'])

@app.route('/profile')
def user_profile():
    return render_template("profile.html", email=session['email'])

@app.route('/daily')
def user_dailys(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    dailys = user.get_daily(user._id)

    return render_template("dailys.html", dailys=dailys, email=user.email)


@app.route('/daily/new', methods=['POST', 'GET'])
def create_new_daily():
    if request.method == 'GET':
        return render_template('dailys.html')
    else:

        user = User.get_by_email(session['email'])

        new_daily = Daily(user._id)
        new_daily.save_to_mongo()

        return make_response(user_dailys(user._id))


@app.route('/hours/<string:daily_id>')
def daily_hours(daily_id):
    daily = Daily.from_mongo(daily_id)
    hours = Hour.from_daily(daily_id)

    return render_template('hours.html', hour=hours, daily=daily)


@app.route('/hours/new/<string:daily_id>', methods=['POST', 'GET'])
def create_new_hour(daily_id):
    if request.method == 'GET':
        return render_template('new_hour.html', daily_id=daily_id)
    else:
        start = request.form['start']
        end = request.form['end']
        content = request.form['action']

        new_hour = Hour(daily_id, start, end, content)
        new_hour.save_to_mongo()

        return make_response(daily_hours(daily_id))

@app.route('/goals')
def user_goals(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    goals = user.get_goal(user._id)

    return render_template("goals.html", goals=goals, email=user.email)


@app.route('/goals/new', methods=['POST', 'GET'])
def create_new_goal():
    if request.method == 'GET':
        return render_template('new_goal.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])

        new_goal = Goal(user._id, title, description)
        new_goal.save_to_mongo()

        return make_response(user_goals(user._id))




if __name__ == '__main__':
    app.run(port=4995, debug=True)


