# coding: utf-8

import datetime
from flask import Flask, render_template,request,session,redirect,url_for,flash,abort,make_response,jsonify
import hashlib
import random
# from views.dashboard import dashboard_view
import config as config
import itsdangerous
DEMO_APP_NAME = 'Demo'
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
    print 'The endpoint of the request is: '+str(request.endpoint)
    if request.method == "POST" and request.endpoint not in ['integration','settings','ajax_demo','demo','dash','console','delete','dashboard']:
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
    # app_id = request.form.get('app_id')
    app_name = session.get('app_name')
    app_id = session.get('app_id')

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
    # app_id = request.form.get('app_id')
    app_name = session.get('app_name')
    app_id = session.get('app_id')

    dashboard = Dashboard()
    dashboard.app_id = app_id
    app_key = dashboard.get_app_key()
    if not app_key:
        app_key = dashboard.get_demo_app_key()
    if not app_key:
        flash('App not exists')
        return render_template('console.html')
    if app_name == DEMO_APP_NAME:
        disabled= True
    else:
        disabled = False
    return render_template('settings.html',
                           app_id=app_id,
                           app_key=app_key,
                           disabled=disabled)
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

@app.route('/dash/<param>',methods=['GET','POST'])
def dash(param):


    username = session.get('username')
    session_token = session.get('session_token')

    if not session_token:
        return redirect(url_for('index'))
    # app_name = request.args.get('app_name')
    # app_id = request.args.get('app_id')
    app_name = session.get('app_name')
    app_id = session.get('app_id')
    print 'the app_name is %s and the app_id  is: %s' %(str(app_name), str(app_id))

    user = Developer()
    user.session_token = session_token
    print 'Param is %s' %(str(param))
    if param == 'dashboard':
        if user.get_all_application():
            all_application_dict = user.all_application_dict                #一旦上一步执行成功，会给user添加一个成员变量 all_demo_application_dict
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
    elif param == 'demo':

        if user.get_all_demo_application():
            all_demo_application_dict = user.all_demo_application_dict   #一旦上一步执行成功，会给user添加一个成员变量 all_demo_application_dict
        else:
            print 'no demo application  exists'
            all_demo_application_dict ={}
        print 'all_demo_application_dict is : %s' %(str(all_demo_application_dict))
        all_application_dict = {}
        if DEMO_APP_NAME in all_demo_application_dict.keys():
            app_name = DEMO_APP_NAME
            app_id = all_demo_application_dict[app_name]
        else:
            'Demo not exists'
            app_name = None
            app_id = None
    else:
        print 'Param is %s' %(str(param))
        all_application_dict = {}


    session['app_name'] = app_name
    session['app_id'] = app_id
    # del all_demo_application_dict[app_name]
    print 'app_name is %s and app_id is %s' %(str(app_name),str(app_id))
    dashboard = Dashboard()
    dashboard.app_id = app_id
    all_app_event = 1
    if request.method == 'POST':
        is_xhr = True
    else:
        is_xhr = False
    print 'last all_application_dict is : %s' %(str(all_application_dict))

    default_user_profile_category = 'Age&Gender'
    default_path_analysis_category = 'Frequently Location'
    default_event_name = 'Event1'
    default_behavior_recognition_measure = 'Activity'

    user_profile_type = 'age'
    path_analysis_type = 'location'
    event_name_type = 'Event1'
    behavior_recognition_measure_type = 'activity'



    user_profile_category_dict = dashboard.get_user_profile_category_dict()    #['Occupation','Tastes']
    path_analysis_measure_dict = dashboard.get_path_analysis_measure_dict() # ['Frequently Track']
    behavior_recognition_event_dict = dashboard.get_behavior_recognition_event_dict() #['event2']
    behavior_recognition_measure_dict = dashboard.get_behavior_recognition_measure_dict() #['Location','Time']

    del user_profile_category_dict[user_profile_type]
    del path_analysis_measure_dict[path_analysis_type]
    del behavior_recognition_event_dict[event_name_type]
    del behavior_recognition_measure_dict[behavior_recognition_measure_type]


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
    return render_template('shared/dash.html',
                           is_xhr = is_xhr,
                           # dashboard_link = dashboard_link,
                           route_link='dashboard',
                           # sort according to ['16down', '16to35', '35to55', '55up']
                           # discard unknown data
                            username = username,
                           app_name = app_name,
                           app_id =app_id,
                           all_application_dict = all_application_dict,

                           # age_data = age_data,
                           # age_category_list = age_category_list,
                           # man_data_list = man_data_list,
                           # woman_data_list = woman_data_list,
                           #
                           # location_data = location_data,
                           #  location_category_list = location_category_list,
                           #  location_percentage_list = location_percentage_list,

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

                           user_profile_category_dict = user_profile_category_dict,
                           path_analysis_measure_dict = path_analysis_measure_dict,
                           behavior_recognition_event_dict = behavior_recognition_event_dict,
                           behavior_recognition_measure_dict = behavior_recognition_measure_dict

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

@app.route('/demo',methods=['GET','POST'])
def demo():

    username = session.get('username')
    session_token = session.get('session_token')
    if not session_token:
        return redirect(url_for('index'))


    user = Developer()
    user.session_token = session_token
    if user.get_all_demo_application():
        all_demo_application_dict = user.all_demo_application_dict   #一旦上一步执行成功，会给user添加一个成员变量 all_demo_application_dict
    else:
        print 'no demo application  exists'
        all_demo_application_dict ={}
    print 'all_demo_application_dict is : %s' %(str(all_demo_application_dict))
    if DEMO_APP_NAME in all_demo_application_dict.keys():
        app_name = DEMO_APP_NAME
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
        is_xhr = True
    else:
        is_xhr = False
    dashboard_link = '/demo'

    # default_user_profile_category = 'Age&Gender'
    # default_path_analysis_category = 'Frequently Location'
    # default_event_name = 'Event1'
    # default_behavior_recognition_measure = 'Activity'
    #
    # user_profile_type = 'age'
    # path_analysis_type = 'location'
    # event_name_type = 'Event1'
    # behavior_recognition_measure_type = 'activity'
    #
    #
    #
    # user_profile_category_dict = dashboard.get_user_profile_category_dict()    #['Occupation','Tastes']
    # path_analysis_measure_dict = dashboard.get_path_analysis_measure_dict() # ['Frequently Track']
    # behavior_recognition_event_dict = dashboard.get_behavior_recognition_event_dict() #['event2']
    # behavior_recognition_measure_dict = dashboard.get_behavior_recognition_measure_dict() #['Location','Time']
    #
    # del user_profile_category_dict[user_profile_type]
    # del path_analysis_measure_dict[path_analysis_type]
    # del behavior_recognition_event_dict[event_name_type]
    # del behavior_recognition_measure_dict[behavior_recognition_measure_type]


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
                           is_xhr = is_xhr,
                           dashboard_link = dashboard_link,
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
                           #
                           # location_data = location_data,
                           #  location_category_list = location_category_list,
                           #  location_percentage_list = location_percentage_list,

                           #  event_data=event_data,
                           #   event_name =event_name,
                           # activity_category_list=activity_category_list,
                           # activity_count_list=activity_count_list,

                           #  default_user_profile_category = default_user_profile_category,
                           # default_path_analysis_category = default_path_analysis_category,
                           # default_event_name = default_event_name,
                           # default_behavior_recognition_measure = default_behavior_recognition_measure,
                           #
                           # user_profile_type = user_profile_type,
                           # path_analysis_type = path_analysis_type,
                           #  event_name_type = event_name_type,
                           #  behavior_recognition_measure_type = behavior_recognition_measure_type,
                           #
                           # user_profile_category_dict = user_profile_category_dict,
                           # path_analysis_measure_dict = path_analysis_measure_dict,
                           # behavior_recognition_event_dict = behavior_recognition_event_dict,
                           # behavior_recognition_measure_dict = behavior_recognition_measure_dict

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

@app.route('/ajax/demo/<param>',methods=['GET','POST'])
def ajax_demo(param):
    username = session.get('username')
    session_token = session.get('session_token')

    if not session_token:
        print 'session_token not exists!'
        return None

    # app_name = app_name
    # app_id = request.args.get('app_id')
    # print 'the app_id of the app is: %s' %(str(app_id))

    user = Developer()
    user.session_token = session_token
    print 'The form is: %s' %(str(request.form))
    print 'Param is: %s' %(str(param))
    _xsrf = request.form.get('_xsrf')
    app_id = request.form.get('app_id')

    dashboard = Dashboard()
    dashboard.app_id = app_id

    if param == 'profile':
        category = request.form.get('category')
        print 'before get_profile_option'
        option = dashboard.get_profile_option(category=category)
        print 'Option is: %s' %(str(option))
        return jsonify(option)
        pass
    elif param == 'path':
        category = request.form.get('category')
        option = dashboard.get_path_option(category=category)
        return jsonify(option)
        pass
    elif param == 'behavior':
        event_name = request.form.get('event')
        category = request.form.get('category')
        option = dashboard.get_event_option(event_name=event_name,category=category)
        print 'after get_event_option'
        print 'Option is: %s' %(str(option))
        return jsonify(option)
        pass
    else:
        return None
        pass

@app.route('/ajax/dashboard/<param>',methods=['GET','POST'])
def ajax_dashboard(param):
    username = session.get('username')
    session_token = session.get('session_token')

    if not session_token:
        print 'session_token not exists!'
        return None

    # app_name = app_name
    # app_id = request.args.get('app_id')
    # print 'the app_id of the app is: %s' %(str(app_id))

    user = Developer()
    user.session_token = session_token
    print 'The form is: %s' %(str(request.form))
    print 'Param is: %s' %(str(param))
    _xsrf = request.form.get('_xsrf')
    app_id = request.form.get('app_id')

    dashboard = Dashboard()
    dashboard.app_id = app_id

    if param == 'profile':
        category = request.form.get('category')
        print 'before get_profile_option'
        option = dashboard.get_profile_option(category=category,kind=None)
        print 'Option is: %s' %(str(option))
        return jsonify(option)
        pass
    elif param == 'path':
        category = request.form.get('category')
        option = dashboard.get_path_option(category=category,kind=None)
        return jsonify(option)
        pass
    elif param == 'behavior':
        event_name = request.form.get('event')
        category = request.form.get('category')
        option = dashboard.get_event_option(event_name=event_name,category=category,kind=None)
        print 'after get_event_option'
        print 'Option is: %s' %(str(option))
        return jsonify(option)
        pass
    else:
        return None
        pass


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

    # 存到session中是为了在dash中使用
    session['app_name'] = app_name
    session['app_id'] = app_id


    if request.method == 'POST':
        is_xhr = True
    else:
        is_xhr = False
    dashboard_link = '/dashboard'

    # default_user_profile_category = 'Age&Gender'
    # default_path_analysis_category = 'Frequently Location'
    # default_event_name = 'Event1'
    # default_behavior_recognition_measure = 'Activity'
    #
    # user_profile_type = 'age'
    # path_analysis_type = 'location'
    # event_name_type = 'Event1'
    # behavior_recognition_measure_type = 'activity'
    #
    #
    #
    # user_profile_category_dict = dashboard.get_user_profile_category_dict()    #['Occupation','Tastes']
    # path_analysis_measure_dict = dashboard.get_path_analysis_measure_dict() # ['Frequently Track']
    # behavior_recognition_event_dict = dashboard.get_behavior_recognition_event_dict() #['event2']
    # behavior_recognition_measure_dict = dashboard.get_behavior_recognition_measure_dict() #['Location','Time']
    #
    # del user_profile_category_dict[user_profile_type]
    # del path_analysis_measure_dict[path_analysis_type]
    # del behavior_recognition_event_dict[event_name_type]
    # del behavior_recognition_measure_dict[behavior_recognition_measure_type]


    print 'log comes out !!!!!'


    return render_template('dashboard.html',
                           is_xhr = is_xhr,
                           dashboard_link = dashboard_link,
                           route_link='dashboard',
                           # sort according to ['16down', '16to35', '35to55', '55up']
                           # discard unknown data
                            username = username,
                           app_name = app_name,
                           app_id =app_id,

                           all_application_dict = all_application_dict,

                           #  default_user_profile_category = default_user_profile_category,
                           # default_path_analysis_category = default_path_analysis_category,
                           # default_event_name = default_event_name,
                           # default_behavior_recognition_measure = default_behavior_recognition_measure,
                           #
                           # user_profile_type = user_profile_type,
                           # path_analysis_type = path_analysis_type,
                           #  event_name_type = event_name_type,
                           #  behavior_recognition_measure_type = behavior_recognition_measure_type,
                           #
                           # user_profile_category_dict = user_profile_category_dict,
                           # path_analysis_measure_dict = path_analysis_measure_dict,
                           # behavior_recognition_event_dict = behavior_recognition_event_dict,
                           # behavior_recognition_measure_dict = behavior_recognition_measure_dict
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
        remember = request.form.get('remember')
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

@app.route('/delete',methods=['GET','POST'])
def delete():
    username = session.get('username')
    session_token = session.get('session_token')

    if not session_token:
        print 'session_token not exists!'
        return None

    # app_name = app_name
    # app_id = request.args.get('app_id')
    # print 'the app_id of the app is: %s' %(str(app_id))

    user = Developer()
    user.session_token = session_token
    print 'The form is: %s' %(str(request.form))
    _xsrf = request.form.get('_xsrf')
    app_id = request.form.get('app_id')

    dashboard = Dashboard()
    dashboard.app_id = app_id

    res = user.delete_app(app_id=app_id,kind=None)
    if res == 0:
        response_json = {'delete':'success'}
        return jsonify(response_json)
    else:
        response_json = {'delete':'failed'}
        return jsonify(response_json)




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