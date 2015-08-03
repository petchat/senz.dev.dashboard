# coding: utf-8

from datetime import datetime
from flask import Flask, render_template,request,session,redirect,url_for

# from views.dashboard import dashboard_view


app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is senz dashboard '

from models import Dashboard,Developer
# 动态路由
# app.register_blueprint(dashboard_view, url_prefix='/dashboard')
@app.route('/')
@app.route('/index')
def index():
    error = None
    username = session.get('username')
    return render_template('index.html', username=username)
    # if not username:
    #     return render_template('index.html', username=username)
    # return redirect(url_for('dashboard',username=username))

@app.route('/dashboard/<app_name>')
def dashboard(app_name):
    username = session.get('username')
    session_token = session.get('session_token')

    app_id = request.args.get('app_id')
    if not session_token:
        return redirect(url_for('index'))
    user = Developer()
    user.session_token = session_token
    if user.get_all_application():
        all_application_dict = user.all_application_dict
    else:
        print 'no application  exists'
        all_application_dict ={}
    print 'all_application_dict is : %s' %(str(all_application_dict))
    dashboard = Dashboard()
    new_data_dict = dashboard.get_age_and_gender_data_dict()
    # sorted_frequent_location_percentage = dashboard.get_location_distribution_data_dict()
    # sorted_frequent_motion_percentage=dashboard.get_motion_distribution_data_dict()
    # sorted_frequent_sound_percentage = dashboard.get_sound_distribution_data_dict()
    # event_name = 'event1'
    # application_id = 'application_id'
    # activity_statistics_dict = dashboard.get_event_to_activity_data(application_id,event_name)
    print 'new_data_dict: ' + str(new_data_dict)
    # print 'sorted_frequent_location_percentage: ' +str(sorted_frequent_location_percentage)
    # print 'sorted_frequent_motion_percentage: ' + str(sorted_frequent_motion_percentage)
    # print 'sorted_frequent_sound_percentage: ' + str(sorted_frequent_sound_percentage)
    # print 'sorted_frequent_sound_percentage: ' + str(activity_statistics_dict)
    print 'log comes out !!!!!'
    return render_template('dashboard.html',
                           man_data_list = new_data_dict['man'],
                           woman_data_list = new_data_dict['woman'],
                           username = username,
                           app_name = app_name,
                           all_application_dict = all_application_dict
                           # location_name_list = [str(kv[0]) for kv in sorted_frequent_location_percentage],
                           # location_time_list = [kv[1] for kv in sorted_frequent_location_percentage],
                           # motion_name_list = [str(kv[0]) for kv in sorted_frequent_motion_percentage],
                           # motion_time_list = [kv[1] for kv in sorted_frequent_motion_percentage],
                           # sound_name_list = [str(kv[0]) for kv in sorted_frequent_sound_percentage],
                           # sound_time_list = [kv[1] for kv in sorted_frequent_sound_percentage],
                           # event_name =event_name,
                           # event_to_activity_name_list=[str(key) for key in activity_statistics_dict.keys()],
                           # event_to_activity_count_list=activity_statistics_dict.values()
                           )

@app.route('/login', methods=['GET','POST'])
def login():
    user = Developer()
    error = None
    if request.method == 'POST':
        print 'got the post request'
        print request.form
        # email=request.form['email']
        username = request.form['username']
        password=request.form['password']
        # remember = request.form['remember']
        result = user.login_with_username(username=username,password=password)
        if result:
            print 'redirecting to dashboard'
            session['username'] = username
            session['session_token'] = user.session_token
            return redirect(url_for('console'))
        else:
            return redirect(url_for('login'))
        # if valid_login(request.form['username'],
        #                request.form['password']):
        #     return log_the_user_in(request.form['username'])
        # else:
        #     error = 'Invalid username/password'
    # the code below this is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

@app.route('/signup', methods=['POST'])
def signup():
    username = session.get('username')
    # user_id = session.get('user')
    if  username:
        return redirect(url_for('dashboard',username=username))
    user = Developer()
    error = None
    if request.method == 'POST':
        print request.form
        email=request.form['email']
        username = request.form['username']
        password=request.form['password']
        # remember = request.form['remember']
        if user.signup(email=email,username=username,password=password):
            return redirect(url_for('login',_anchor='signin'))
        else:
            return redirect(url_for('login',_anchor='signup'))


    return render_template('signup.html', error=error)

@app.route('/logout', methods=['POST','GET'])
def logout():
    if session.get('username'):
        session['username'] = None
    return redirect(url_for('index'))


@app.route('/console', methods=['POST','GET'])
def console():
    username = session.get('username')
    session_token = session.get('session_token')

    if not session_token:
        return redirect(url_for('login'))
    error = None
    user = Developer()
    user.session_token = session_token
    if request.method == 'POST':
        print request.form
        app_name=request.form['appname']
        result = user.create_new_app(app_name)
        if not result:
            print 'error when create new app'

        # remember = request.form['remember']
        # if user.signup(email=email,username=username,password=password):
        #     return redirect(url_for('login',_anchor='signin'))
        # else:
        #     return redirect(url_for('login',_anchor='signup'))
    if user.get_all_application():
        all_application_dict = user.all_application_dict
    else:
        print 'no application  exists'
        all_application_dict ={}
    print 'all_application_dict is : %s' %(str(all_application_dict))
    return render_template('console.html', username=username,all_application_dict=all_application_dict)

#
# @app.route('/dashboard')
# def page():
#     return render_template('dashboard.html')
