# coding: utf-8

import datetime
from flask import Flask, render_template,request,session,redirect,url_for,flash,abort,make_response
from flask_wtf.csrf import CsrfProtect
import hashlib
import random
# from views.dashboard import dashboard_view
import config as config
import itsdangerous

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
# CsrfProtect(app)
expiration_days = 30
from models import Dashboard,Developer

def generate_token():
    '''
        Generates a token with randomly salted SHA1. Returns a string.
        '''
    _MAX_CSRF_KEY = long(2 << 63)
    salt = str(random.randrange(0, _MAX_CSRF_KEY)).encode('utf-8')
    return hashlib.sha1(salt).hexdigest()

@app.before_request
def xsrf_protect():
    print request.endpoint
    if request.method == "POST" and request.endpoint not in ['integration','settings']:
        token = session.pop('_xsrf', None)
        print 'token: ' +str(token)
        print 'form xsrf: ' +str(request.form.get('_xsrf'))
        if not token or token != request.form.get('_xsrf'):
            abort(403)

def generate_xsrf_token():
    if '_xsrf' not in session:
        session['_xsrf'] = generate_token()
    return session['_xsrf']
app.jinja_env.globals['_xsrf'] = generate_xsrf_token

# 动态路由
# app.register_blueprint(dashboard_view, url_prefix='/dashboard')
def get_expiration():
    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=expiration_days)
    return expire_date
@app.route('/')
def index():
    error = None
    username = session.get('username')

    return render_template('index.html', username=username)
    # if not username:
    #     return render_template('index.html', username=username)
    # return redirect(url_for('dashboard',username=username))
# 注意现在还没有做user和app_id是否是从属关系的认证

@app.route('/integration',methods=['POST'])
def integration():
    print 'args: '+str(request.args)
    print 'form: '+str(request.form)
    app_id = request.form.get('app_id')
    dashboard = Dashboard()
    dashboard.app_id = app_id
    app_key = dashboard.get_app_key()
    if not app_key:
        app_key = dashboard.get_demo_app_key()
    if not app_key:
        flash('App not exists')
        return render_template('console.html')
    return render_template('integration.html',
                           app_id=app_id,
                           app_key=app_key)
    # app_name = session.get('app_name')
    # app_id = session.get('app_id')
    # username = session.get('username')
    # session_token = session.get('session_token')
    #
    # user = Developer()
    # user.session_token = session_token
    # if user.get_all_application():
    #     all_application_dict = user.all_application_dict
    # else:
    #     print 'no application  exists'
    #     all_application_dict ={}
    # print 'all_application_dict is : %s' %(str(all_application_dict))
    # del all_application_dict[app_name]
    #
    # error = None
    # username = session.get('username')
    #
    # return render_template('integration.html',
    #                        route_link='dashboard',
    #                         username = username,
    #                        app_name = app_name,
    #                        all_application_dict =all_application_dict ,
    #                       )
@app.route('/settings',methods=['POST'])
def settings():
    print 'args: '+str(request.args)
    print 'form: '+str(request.form)
    app_id = request.form.get('app_id')
    dashboard = Dashboard()
    dashboard.app_id = app_id
    app_key = dashboard.get_app_key()
    if not app_key:
        app_key = dashboard.get_demo_app_key()
    if not app_key:
        flash('App not exists')
        return render_template('console.html')
    return render_template('settings.html',
                           app_id=app_id,
                           app_key=app_key)
    # app_name = session.get('app_name')
    # app_id = session.get('app_id')
    # username = session.get('username')
    # session_token = session.get('session_token')
    #
    # user = Developer()
    # user.session_token = session_token
    # if user.get_all_application():
    #     all_application_dict = user.all_application_dict
    # else:
    #     print 'no application  exists'
    #     all_application_dict ={}
    # print 'all_application_dict is : %s' %(str(all_application_dict))
    # del all_application_dict[app_name]
    #
    # error = None
    # username = session.get('username')
    #
    # return render_template('settings.html',
    #                        route_link='dashboard',
    #                         username = username,
    #                        app_name = app_name,
    #                        all_application_dict = all_application_dict,
    #                       )
    # if not username:
    #     return render_template('index.html', username=username)
    # return redirect(url_for('dashboard',username=username))
# 注意现在还没有做user和app_id是否是从属关系的认证

@app.route('/demo',methods=['POST','GET'])
def demo():
    username = session.get('username')
    session_token = session.get('session_token')

    if not session_token:
        return redirect(url_for('index'))
    # app_name = app_name
    # app_id = request.args.get('app_id')
    # print 'the app_id of the app is: %s' %(str(app_id))

    user = Developer()
    user.session_token = session_token
    if user.get_all_demo_application():
        all_demo_application_dict = user.all_demo_application_dict
    else:
        print 'no demo application  exists'
        all_demo_application_dict ={}
    print 'all_demo_application_dict is : %s' %(str(all_demo_application_dict))
    if 'Demo1' in all_demo_application_dict.keys():
        app_name = 'Demo1'
        app_id = all_demo_application_dict[app_name]
    else:
        'Demo not exists'
        app_name = None
        app_id = None
    session['app_name'] = app_name
    session['app_id'] = app_id
    # del all_demo_application_dict[app_name]
    print 'app_name is %s and app_id is %s' %(str(app_name),str(app_id))
    dashboard = Dashboard()
    dashboard.app_id = app_id

    all_app_event = 1

    if request.method == 'POST':
        pass
        # new_data_dict = dashboard.get_demo_age_and_gender_data_dict()
        # if not new_data_dict:
        #     age_data = False
        #     age_category_list = []
        #     man_data_list = []
        #     woman_data_list = []
        # else:
        #     age_data = True
        #     age_category_list = sorted(new_data_dict['man'].keys())
        #     man_data_list = [key[1] for key in sorted(new_data_dict['man'].items(),key=lambda l:l[0])]
        #     woman_data_list = [key[1] for key in sorted(new_data_dict['woman'].items(),key=lambda l:l[0])]
        # print 'data in age_and_gender is display_age_and_gender:%s  age_category_list:%s man_data_list:%s woman_data_list:%s' %(str(age_data),str(age_category_list),str(man_data_list),str(woman_data_list))
        #
        #
        # new_data_dict = dashboard.get_demo_location_distribution_data_dict()
        # del new_data_dict['unknown']
        # if not new_data_dict:
        #     location_data = False
        #     location_category_list = []
        #     location_percentage_list = []
        # else:
        #     location_data = True
        #     location_category_list = [str(key[0]) for key in sorted(new_data_dict.items(),key=lambda l:l[1],reverse=True)]
        #     location_percentage_list = [key[1] for key in sorted(new_data_dict.items(),key=lambda l:l[1],reverse=True)]
        #
        # print 'data in get_location_distribution_data_dict is location_data: %s location_category_list:%s  location_percentage_list:%s ' %(str(location_data),str(location_category_list),str(location_percentage_list))
        # new_data_dict = dashboard.get_demo_event_to_activity_data()
        # print 'new data dict'+str(new_data_dict.values())
        # # if not new_data_dict.values():
        # if not new_data_dict:
        #     event_data = False
        #     event_name = None
        #     activity_category_list = []
        #     activity_count_list = []
        # else:
        #     event_data = True
        #     event_name = new_data_dict.keys()[0]
        #     new_data_dict = new_data_dict.values()[0]
        #     del new_data_dict['others']
        #     activity_category_list = [str(key[0]) for key in sorted(new_data_dict.items(),key=lambda l:l[1],reverse=True)]
        #     activity_count_list = [key[1] for key in sorted(new_data_dict.items(),key=lambda l:l[1],reverse=True)]
        #
        # print 'data in get_event_to_activity_data is event_data: %s event_name:%s  activity_category_list:%s  activity_count_list: %s' %(str(event_data),str(event_name),str(activity_category_list),str(activity_count_list))
    elif request.method == 'GET':
        default_user_profile_category = 'Age&Gender'
        default_path_analysis_category = 'Frequently Location'
        default_event_name = 'Event1'
        default_behavior_recognition_measure = 'Activity'

        user_profile_type = 'age'
        path_analysis_type = 'location'
        event_name_type = 'Event1'
        behavior_recognition_measure_type = 'Activity'



        user_profile_category_list = dashboard.get_user_profile_category_list()    #['Occupation','Tastes']
        path_analysis_measure_list = dashboard.get_path_analysis_measure_list() # ['Frequently Track']
        behavior_recognition_event_list = dashboard.get_behavior_recognition_event_list() #['event2']
        behavior_recognition_measure_list = dashboard.get_behavior_recognition_measure_list() #['Location','Time']


    # sorted_frequent_location_percentage = dashboard.get_location_distribution_data_dict()
    # sorted_frequent_motion_percentage=dashboard.get_motion_distribution_data_dict()
    # sorted_frequent_sound_percentage = dashboard.get_sound_distribution_data_dict()
    # event_name = 'event1'
    # application_id = 'application_id'
    # activity_statistics_dict = dashboard.get_event_to_activity_data(application_id,event_name)
    # print 'new_data_dict: ' + str(new_data_dict)
    # print 'sorted_frequent_location_percentage: ' +str(sorted_frequent_location_percentage)
    # print 'sorted_frequent_motion_percentage: ' + str(sorted_frequent_motion_percentage)
    # print 'sorted_frequent_sound_percentage: ' + str(sorted_frequent_sound_percentage)
    # print 'sorted_frequent_sound_percentage: ' + str(activity_statistics_dict)
    print 'log comes out !!!!!'
    return render_template('demo.html',
                           route_link='dashboard',
                           # sort according to ['16down', '16to35', '35to55', '55up']
                           # discard unknown data
                            username = username,
                           app_name = app_name,
                           app_id =app_id,
                           all_application_dict = {},

                           # age_data = age_data,
                           # age_category_list = age_category_list,
                           # man_data_list = man_data_list,
                           # woman_data_list = woman_data_list,

                           # location_data = location_data,
                           #  location_category_list = location_category_list,
                           #  location_percentage_list = location_percentage_list,
                           #
                           #  event_data=event_data,
                           #   event_name =event_name,
                           # activity_category_list=activity_category_list,
                           # activity_count_list=activity_count_list,

                            default_user_profile_category = default_user_profile_category,
                           default_path_analysis_category = default_path_analysis_category,
                           default_event_name = default_event_name,
                           default_behavior_recognition_measure = default_behavior_recognition_measure,

                           user_profile_type = user_profile_type,
                           path_analysis_type = path_analysis_type,
                            event_name_type = event_name_type,
                            behavior_recognition_measure_type = behavior_recognition_measure_type,

                           user_profile_category_list = user_profile_category_list,
                           path_analysis_measure_list = path_analysis_measure_list,
                           behavior_recognition_event_list = behavior_recognition_event_list,
                           behavior_recognition_measure_list = behavior_recognition_measure_list

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


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    username = session.get('username')
    session_token = session.get('session_token')

    if not session_token:
        return redirect(url_for('index'))
    app_name = request.args.get('app_name')
    app_id = request.args.get('app_id')
    print 'the app_id of the app is: %s' %(str(app_id))

    user = Developer()
    user.session_token = session_token
    if user.get_all_application():
        all_application_dict = user.all_application_dict
    else:
        print 'no application  exists'
        all_application_dict ={}
    print 'all_application_dict is : %s' %(str(all_application_dict))
    if app_name and app_id:
        del all_application_dict[app_name]
    else:
        app_name = all_application_dict.keys()[0]
        app_id = all_application_dict[app_name]
        del all_application_dict[app_name]
    dashboard = Dashboard()
    dashboard.app_id = app_id
    session['app_name'] = app_name
    session['app_id'] = app_id

    new_data_dict = dashboard.get_age_and_gender_data_dict()
    if not new_data_dict:
        age_data = False
        age_category_list = []
        man_data_list = []
        woman_data_list = []
    else:
        age_data = True
        age_category_list = sorted(new_data_dict['man'].keys())
        man_data_list = [key[1] for key in sorted(new_data_dict['man'].items(),key=lambda l:l[0])]
        woman_data_list = [key[1] for key in sorted(new_data_dict['woman'].items(),key=lambda l:l[0])]
    print 'data in age_and_gender is display_age_and_gender:%s  age_category_list:%s man_data_list:%s woman_data_list:%s' %(str(age_data),str(age_category_list),str(man_data_list),str(woman_data_list))


    new_data_dict = dashboard.get_location_distribution_data_dict()


    if not new_data_dict:
        location_data = False
        location_category_list = []
        location_percentage_list = []
    else:
        del new_data_dict['unknown']
        location_data = True
        location_category_list = [str(key[0]) for key in sorted(new_data_dict.items(),key=lambda l:l[1],reverse=True)]
        location_percentage_list = [key[1] for key in sorted(new_data_dict.items(),key=lambda l:l[1],reverse=True)]

    print 'data in get_location_distribution_data_dict is location_data: %s location_category_list:%s  location_percentage_list:%s ' %(str(location_data),str(location_category_list),str(location_percentage_list))
    new_data_dict = dashboard.get_event_to_activity_data()
    if not new_data_dict:
        event_data = False
        event_name = None
        activity_category_list = []
        activity_count_list = []
    else:
        event_data = True
        event_name = new_data_dict.keys()[0]
        new_data_dict = new_data_dict.values()[0]
        del new_data_dict['others']
        activity_category_list = [str(key[0]) for key in sorted(new_data_dict.items(),key=lambda l:l[1],reverse=True)]
        activity_count_list = [key[1] for key in sorted(new_data_dict.items(),key=lambda l:l[1],reverse=True)]

    print 'data in get_event_to_activity_data is event_data: %s event_name:%s  activity_category_list:%s  activity_count_list: %s' %(str(event_data),str(event_name),str(activity_category_list),str(activity_count_list))

    # sorted_frequent_location_percentage = dashboard.get_location_distribution_data_dict()
    # sorted_frequent_motion_percentage=dashboard.get_motion_distribution_data_dict()
    # sorted_frequent_sound_percentage = dashboard.get_sound_distribution_data_dict()
    # event_name = 'event1'
    # application_id = 'application_id'
    # activity_statistics_dict = dashboard.get_event_to_activity_data(application_id,event_name)
    # print 'new_data_dict: ' + str(new_data_dict)
    # print 'sorted_frequent_location_percentage: ' +str(sorted_frequent_location_percentage)
    # print 'sorted_frequent_motion_percentage: ' + str(sorted_frequent_motion_percentage)
    # print 'sorted_frequent_sound_percentage: ' + str(sorted_frequent_sound_percentage)
    # print 'sorted_frequent_sound_percentage: ' + str(activity_statistics_dict)
    print 'log comes out !!!!!'
    return render_template('dashboard.html',
                           route_link='dashboard',
                           # sort according to ['16down', '16to35', '35to55', '55up']
                           # discard unknown data
                            username = username,
                           app_name = app_name,
                           all_application_dict = all_application_dict,
                           age_data = age_data,
                           age_category_list = age_category_list,
                           man_data_list = man_data_list,
                           woman_data_list = woman_data_list,

                           location_data = location_data,
                            location_category_list = location_category_list,
                            location_percentage_list = location_percentage_list,

                            event_data=event_data,
                             event_name =event_name,
                           activity_category_list=activity_category_list,
                           activity_count_list=activity_count_list

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
    username = session.get('username')
    session_token = session.get('session_token')
    # session_token = request.cookies.get('session_token')
    #暂时不验证session_token的有效性
    if  session_token  :
        return redirect(url_for('index'))

    # else:
    #     session_token = request.cookies.get('session_token')
    #     if session_token :
    #         session['session_token'] = session_token
    #         return redirect(url_for('index'))

    # if expiration and expiration > datetime.datetime.now():
    #     return redirect(url_for('index'))
    user = Developer()
    error = None
    if request.method == 'POST':
        print 'got the post request'
        print request.form
        # email=request.form['email']
        username = request.form['username']
        password=request.form['password']
        remember = request.form['remember']
        result = user.login_with_username(username=username,password=password)
        if result:
            print 'redirecting to console'
            session['username'] = username
            session['session_token'] = user.session_token
            resp = make_response(redirect(url_for('console')))
            # resp.set_cookie('expiration',get_expiration())
            expires = get_expiration() if remember == 'on' else None
            resp.set_cookie('_xsrf',generate_xsrf_token())
            resp.set_cookie('session_token',user.session_token,expires=expires)
            return resp
        else:
            return redirect(url_for('login'))
        # if valid_login(request.form['username'],
        #                request.form['password']):
        #     return log_the_user_in(request.form['username'])
        # else:
        #     error = 'Invalid username/password'
    # the code below this is executed if the request method
    # was GET or the credentials were invalid
    resp = make_response(render_template('login.html', error=error))

    # resp.set_cookie('_xsrf',generate_xsrf_token())

    return resp

@app.route('/signup', methods=['POST'])
def signup():
    username = session.get('username')
    print str(request.form)
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
            flash('Successfully sign up,please login in!')
            return redirect(url_for('login',_anchor='signin'))
        else:
            flash('Sign up failed,please try again!')
            return redirect(url_for('login',_anchor='signup'))


    # return render_template('signup.html', error=error)

@app.route('/logout', methods=['POST','GET'])
def logout():
    if session.get('session_token'):
        session['session_token'] = None
    if session.get('username'):
        session['username'] = None

    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset():
    # if session.get('username'):
    #     session['username'] = None
    email = request.form['email']
    print 'request.form is: %s' %(str(request.form))
    return redirect(url_for('index'))

@app.route('/track',methods=['GET','POST'])
def track():
    username = session.get('username')
    session_token = session.get('session_token')

    if not session_token:
        return redirect(url_for('login'))
    error = None
    user = Developer()
    user.session_token = session_token
    if user.get_all_application():
        all_application_dict = user.all_application_dict
    else:
        print 'no application  exists'
        all_application_dict ={}
    app_name = request.args.get('app_name')
    app_id = request.args.get('app_id')
    if app_name and app_id:
        del all_application_dict[app_name]
    else:
        app_name = all_application_dict.keys()[0]
        app_id = all_application_dict[app_name]
        del all_application_dict[app_name]

    if request.method == 'POST':
        print request.form
        tracker_id=request.form['tracker_id']
        app_id = request.form['app_id']

        print 'all_application_dict is : %s' %(str(all_application_dict))


        result = user.connect_new_tracker(tracker_id=tracker_id,app_id=app_id)
        if not result:
            return 'error when connect new tracker'
        else:
            return 'success'
    else:

        if user.get_all_tracker():
            all_tracker_dict = user.all_tracker_dict
        else:
            print 'no application  exists'
            all_tracker_dict ={}
        print 'all_tracker_dict is : %s' %(str(all_tracker_dict))
        return render_template('track.html',
                               route_link='track',
                               username=username,
                               all_tracker_dict=all_tracker_dict,
                               app_name = app_name,
                               app_id = app_id,
                           all_application_dict = all_application_dict)

@app.route('/console', methods=['POST','GET'])
def console():
    username = session.get('username')
    session_token = request.cookies.get('session_token')
    _xsrf = request.cookies.get('_xsrf')
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

@app.errorhandler(403)
def permission_forbidden(e):
    flash('Permission denied!')
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500