# coding: utf-8

import datetime
from flask import Flask, render_template,request,session,redirect,url_for,flash,abort,make_response,jsonify
import hashlib
#import json
import requests
import random
# from views.dashboard import dashboard_view
import config as config
#import itsdangerous
from leancloud import  Object, Query

DEMO_APP_NAME = 'Demo'
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
# CsrfProtect(app)
expiration_days = 30
from models import Dashboard,Developer


def generate_token():
    """Generates a token with randomly salted SHA1. Returns a string.
    """
    _MAX_CSRF_KEY = long(2 << 63)
    salt = str(random.randrange(0, _MAX_CSRF_KEY)).encode('utf-8')
    return hashlib.sha1(salt).hexdigest()


@app.before_request
def xsrf_protect():
    print 'The endpoint of the request is: ' + str(request.endpoint)
    if request.method == "POST" and request.endpoint not in \
            ['panel', 'integration', 'settings', 'ajax_dashboard', 
             'ajax_demo', 'demo', 'dash', 'console', 'delete', 
             'dashboard', 'update_static_info']:
        token = session.pop('_xsrf', None)
        print 'token: ' + str(token)
        print 'form xsrf: ' + str(request.form.get('_xsrf'))
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
    username = session.get('username')
    return render_template('index.html', username=username)


@app.route('/integration',methods=['POST'])
def integration():
    #print 'args: '+str(request.args)
    #print 'form: '+str(request.form)
    # app_id = request.form.get('app_id')
    #app_name = session.get('app_name')
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
            all_application_dict = user.all_application_dict                #一旦上一步执行成功，会给user添加一个成员变量 all_application_dict
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
    #all_app_event = 1
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
                            behavior_recognition_measure_dict = behavior_recognition_measure_dict)


@app.route('/demo',methods=['GET', 'POST'])
def demo():

    username = session.get('username')
    session_token = session.get('session_token')
    if not session_token:
        return redirect(url_for('index'))


    user = Developer()
    user.session_token = session_token
    if user.get_all_demo_application():
        all_demo_application_dict = user.all_demo_application_dict   # 一旦上一步执行成功，会给user添加一个成员变量 all_demo_application_dict
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
    #all_app_event = 1
    if request.method == 'POST':
        is_xhr = True
    else:
        is_xhr = False
    dashboard_link = '/demo'

    return render_template('demo.html',
                           is_xhr = is_xhr,
                           dashboard_link = dashboard_link,
                           route_link='dashboard',
                           # sort according to ['16down', '16to35', '35to55', '55up']
                           # discard unknown data
                           username = username,
                           app_name = app_name,
                           app_id =app_id,
                           all_application_dict = {})

@app.route('/ajax/demo/<param>',methods=['GET','POST'])
def ajax_demo(param):
    #username = session.get('username')
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
    #_xsrf = request.form.get('_xsrf')
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
    #username = session.get('username')
    session_token = session.get('session_token')

    if not session_token:
        print 'session_token not exists!'
        return None

    # app_name = app_name
    # app_id = request.args.get('app_id')
    # print 'the app_id of the app is: %s' %(str(app_id))

    user = Developer()
    user.session_token = session_token
    #print 'The form is: %s' %(str(request.form))
    #print 'Param is: %s' %(str(param))
    #_xsrf = request.form.get('_xsrf')
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
    print username
    print "session_token+", session_token

    #if not session_token:
    #    return redirect(url_for('index'))

    # change app_name & app_id as demo for test
    app_name = request.args.get('app_name')
    app_id = request.args.get('app_id')
    app_id = 'demo55bc5d8e00b0cb9c40dec37b'
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
    dashboard_link = '/dashboard/'

    return render_template('dashboard.html',
                           is_xhr=is_xhr,
                           dashboard_link=dashboard_link,
                           route_link='dashboard',
                           # sort according to ['16down', '16to35', '35to55', '55up']
                           # discard unknown data
                            username = username,
                           app_name = app_name,
                           app_id =app_id,
                           all_application_dict = all_application_dict)


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
    #email = request.form['email']
    #print 'request.form is: %s' %(str(request.form))
    return redirect(url_for('index'))


@app.route('/panel', methods=['GET', 'POST'])
def panel():
    location1_list = ['home','dining','scenic_spot','traffic', 'exhibition',
                      'entertainment','healthcare', 'estate','life_service','hotel',
                      'work_office','finance', 'education','government','infrastructure',
                      'auto_related','shopping','sports']
    location2_list = [
        ['home'],
        ['chinese_restaurant', 'japan_korea_restaurant','japan_restaurant','korea_restaurant', 'western_restaurant', 'bbq', 'chafing_dish', 'seafood_restaurant', 'vegetarian_diet', 'muslim_dish', 'buffet', 'dessert', 'cooler_store', 'snack_bar','vegetarian_diet'],
        ['scenic_spot'],
        ['traffic','bus_stop','subway','highway_service_area','railway_station','airport','coach_station','traffic_place','bus_route','subway_track'],
        ['museum', 'exhibition_hall', 'science_museum', 'library', 'gallery', 'convention_center'],
        ['bath_sauna', 'ktv', 'bar', 'coffee', 'night_club', 'cinema', 'odeum', 'resort', 'outdoor', 'game_room', 'internet_bar','botanic_garden','music_hall','movie','playground','temple','aquarium','cultural_venues','fishing_garden','picking_garden','cultural_palace', 'memorial_hall','park','zoo','chess_room','bathing_beach','theater'],
        ['hospital', 'clinic', 'emergency_center', 'drugstore','special_hospital'],
        ['residence', 'business_building','community_center'],
        ['travel_agency', 'ticket_agent','ticket_agent_plane', 'ticket_agent_train','post_office', 'telecom_offices' ,'telecom_offices_unicom', 'telecom_offices_netcom','newstand', 'water_supply_office', 'electricity_office', 'photographic_studio', 'laundry', 'talent_market', 'lottery_station', 'housekeeping','housekeeping_lock','housekeeping_hour','housekeeping_water_deliver', 'intermediary', 'pet_service', 'salvage_station', 'welfare_house', 'barbershop','laundry','ticket_agent_coach','housekeeping_nanny','housekeeping_house_moving', 'telecom_offices_tietong','ticket_agent_bus','telecom_offices_mobile','housekeeping_alliance_repair','telecom_offices_telecom'],
        ['motel', 'hotel', 'economy_hotel', 'guest_house', 'hostel','farm_house','villa','dormitory','other_hotel','apartment_hotel','inn','holiday_village'],
        ['work_office'],
        ['bank', 'atm', 'insurance_company', 'security_company'],
        ['university', 'high_school', 'primary_school', 'kinder_garten', 'training_institutions', 'technical_school', 'adult_education','scientific_research_institution','driving_school'],
        ['agriculture_forestry_and_fishing_base','foreign_institutional','government_agency','minor_institutions','tax_authorities'],
        ['public_utilities', 'toll_station', 'other_infrastructure','public_phone','factory' ,'city_square','refuge','public_toilet','church','industrial_area'],
        ['gas_station', 'parking_plot', 'auto_sale', 'auto_repair', 'motorcycle', 'car_maintenance', 'car_wash','motorcycle_service','motorcycle_repair'],
        ['comprehensive_market', 'convenience_store', 'supermarket', 'digital_store', 'pet_market', 'furniture_store', 'farmers_market', 'commodity_market', 'flea_market', 'sports_store', 'clothing_store', 'video_store', 'glass_store', 'mother_store', 'jewelry_store', 'cosmetics_store', 'gift_store', 'pawnshop', 'antique_store', 'bike_store', 'cigarette_store', 'stationer','motorcycle_sell','sports_store','shopping_street'],
        ['golf','skiing','sports_venues','football_field','tennis_court','horsemanship','race_course','basketball_court'],
    ]
    motion_dict = {'sitting': 0, 'walking': 3, 'running': 4, 'ridding': 2, 'driving': 1, 'unknown': -1}
    event_list = ['attend_concert', 'go_outing', 'dining_in_restaurant', 'watch_movie', 
                  'study_in_class', 'visit_sights', 'work_in_office', 'exercise_outdoor', 
                  'shopping_in_mall', 'exercise_indoor']
    status_dict = {"unknown": -1, "arriving_home":0, "leaving_home":1, "arriving_office": 2, "leaving_office": 3, "going_home":4, "going_office":5, "user_home_office_not_yet_defined": 6}

    session_token = session.get('session_token')
    if not session_token:
        return redirect(url_for('login'))
    user = Developer()
    user.session_token = session_token

    app_id = request.form.get('app_id')
    dashboard = Dashboard()
    dashboard.app_id = app_id
    app_key = dashboard.get_app_key()
    if not app_key:
        app_key = dashboard.get_demo_app_key()
    if not app_key:
        flash('App not exists')
        return render_template('console.html')

    type = request.form.get('type')
    val = request.form.get('val')
    if type and val:
        if user.get_tracker_of_app(app_id):
            tracker_list = user.tracker_list
        headers = {"X-AVOSCloud-Application-Id": "qTFUwcnM3U3us8B3ArenyJbm", "X-AVOSCloud-Application-Key": "ksfJtp9tIEriApWmbtOrQs5F"}
        payload = {"type": type, "val": val}
        #for tracker in tracker_list:
        requests.post("https://leancloud.cn/1.1/functions/notify_new_details",  headers = headers, data = payload)
    return render_template('panel.html', 
                           location1_list = location1_list,
                           location2_list = location2_list,
                           motion_dict = motion_dict,
                           event_list = event_list,
                           status_dict= status_dict)




@app.route('/track',methods=['GET','POST'])
def track():
    username = session.get('username')
    session_token = session.get('session_token')

    if not session_token:
        return redirect(url_for('login'))
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
    #_xsrf = request.cookies.get('_xsrf')
    if not session_token:
        return redirect(url_for('login'))
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
    #username = session.get('username')
    session_token = session.get('session_token')

    if not session_token:
        print 'session_token not exists!'
        return None

    # app_name = app_name
    # app_id = request.args.get('app_id')
    # print 'the app_id of the app is: %s' %(str(app_id))

    user = Developer()
    user.session_token = session_token
    #print 'The form is: %s' %(str(request.form))
    #_xsrf = request.form.get('_xsrf')
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


@app.route('/v1/StaticInfo', methods=['POST'])
def update_static_info():
    user_id = request.json.get('user_id')
    if not user_id:
       return make_response('Error')
    staticInfo = request.json.get('staticInfo')
    
    parse_dict = parse_static_info(staticInfo=staticInfo)
    # get user Object
    query =Query(Object.extend('_User'))
    query.equal_to('objectId', user_id)
    user = query.find()[0]

    # get app Object
    query = Query(Object.extend('BindingInstallation'))
    query.equal_to('user', user)
    result_list = query.find()
    app_set = set()
    for result in result_list:
        app_set.add(result.attributes['application'].id)
    app_id_list = list(app_set)

    for app_id in app_id_list:
        query =Query(Object.extend('Application'))
        query.equal_to('objectId', app_id)
        app = query.find()[0]

        DashboardSource = Object.extend('DashboardSource')
        query = Query(DashboardSource)
        query.equal_to('app', app)
        query.equal_to('user', user)
        dst_table =query.find()
        if not dst_table:
            dst_table = DashboardSource()
        else: 
            dst_table = dst_table[0]

        dst_table.set('app', app)
        dst_table.set('user', user)
        for key, value in parse_dict.items():
            if value:
                dst_table.set(key, value)
        dst_table.save()
    return make_response('OK')


def parse_static_info(staticInfo={}):
    ret_dict = {}
    age = ''
    if staticInfo.has_key('age'):
        age_dict = staticInfo.get('age')
        age = sorted(age_dict.items(), key=lambda age_dict: -age_dict[1])[0][0]
    ret_dict['age'] = age

    gender = ''
    if staticInfo.has_key('gender'):
        gender = 'male' if staticInfo.get('gender') > 0 else 'female'
    ret_dict['gender'] = gender

    consumption = ''
    if staticInfo.has_key('consumption'):
        consumption_dict = staticInfo.get('consumption')
        consumption = sorted(consumption_dict.items(), 
                             key=lambda consumption_dict: -consumption_dict[1])[0][0]
    ret_dict['consumption'] = consumption

    marriage = ''
    if staticInfo.has_key('marriage'):
        marriage = 'yes' if staticInfo.get('marriage') > 0 else 'no'
    ret_dict['marriage'] = marriage

    has_pet = ''
    if staticInfo.has_key('has_pet'):
        has_pet = 'yes' if staticInfo.get('has_pet') > 0 else 'no'
    ret_dict['has_pet'] = has_pet

    has_car = ''
    if staticInfo.has_key('has_car'):
        has_car = 'yes' if staticInfo.get('has_car') > 0 else 'no'
    ret_dict['has_car'] = has_car

    pregnant = ''
    if staticInfo.has_key('pregnant'):
        pregnant = 'yes' if staticInfo.get('pregnant') > 0 else 'no'
    ret_dict['pregnant'] = pregnant

    occupation = ''
    if staticInfo.has_key('occupation'):
        occupation_dict = staticInfo.get('occupation')
        occupation = sorted(occupation_dict.items(),
                            key=lambda occupation_dict: -occupation_dict[1])[0][0]
    ret_dict['occupation'] = occupation
            
    field = ''
    if staticInfo.has_key('field'):
        field_dict = staticInfo.get('field')
        field = sorted(field_dict.items(),
                            key=lambda field_dict: -field_dict[1])[0][0]
    ret_dict['field'] = field

    sport = ''
    if staticInfo.has_key('sport'):
        sport_dict = staticInfo.get('sport')
        sport = sorted(sport_dict.items(),
                            key=lambda sport_dict: -sport_dict[1])[0][0]
    ret_dict['sport'] = sport

    social = ''
    if staticInfo.has_key('social'):
        social = 'yes' if staticInfo.get('social') > 0 else 'no'
    ret_dict['social'] = social

    indoorsman = ''
    if staticInfo.has_key('indoorsman'):
        indoorsman = 'yes' if staticInfo.get('indoorsman') > 0 else 'no'
    ret_dict['indoorsman'] = indoorsman

    acg = ''
    if staticInfo.has_key('acg'):
        acg = 'yes' if staticInfo.get('acg') > 0 else 'no'
    ret_dict['acg'] = acg

    tvseries_show = ''
    if staticInfo.has_key('tvseries_show'):
        tvseries_show = 'yes' if staticInfo.get('tvseries_show') > 0 else 'no'
    ret_dict['tvseries_show'] = tvseries_show

    variety_show = ''
    if staticInfo.has_key('variety_show'):
        variety_show = 'yes' if staticInfo.get('variety_show') > 0 else 'no'
    ret_dict['variety_show'] = variety_show

    game_show = ''
    if staticInfo.has_key('game_show'):
        game_show = 'yes' if staticInfo.get('game_show') > 0 else 'no'
    ret_dict['game_show'] = game_show

    sports_show = ''
    if staticInfo.has_key('sports_show'):
        sports_show = 'yes' if staticInfo.get('sports_show') > 0 else 'no'
    ret_dict['sports_show'] = sports_show

    health = ''
    if staticInfo.has_key('health'):
        health = 'yes' if staticInfo.get('health') > 0 else 'no'
    ret_dict['health'] = health

    gamer = ''
    if staticInfo.has_key('gamer'):
        gamer = 'yes' if staticInfo.get('gamer') > 0 else 'no'
    ret_dict['gamer'] = gamer

    study = ''
    if staticInfo.has_key('study'):
        study = 'yes' if staticInfo.get('study') > 0 else 'no'
    ret_dict['study'] = study

    game_news = ''
    if staticInfo.has_key('game_news'):
        game_news = 'yes' if staticInfo.get('game_news') > 0 else 'no'
    ret_dict['game_news'] = game_news

    sports_news = ''
    if staticInfo.has_key('sports_news'):
        sports_news = 'yes' if staticInfo.get('sports_news') > 0 else 'no'
    ret_dict['sports_news'] = sports_news

    business_news = ''
    if staticInfo.has_key('business_news'):
        business_news = 'yes' if staticInfo.get('business_news') > 0 else 'no'
    ret_dict['business_news'] = business_news

    current_news = ''
    if staticInfo.has_key('current_news'):
        current_news = 'yes' if staticInfo.get('current_news') > 0 else 'no'
    ret_dict['current_news'] = current_news

    entertainment_news = ''
    if staticInfo.has_key('entertainment_news'):
        entertainment_news = 'yes' if staticInfo.get('entertainment_news') > 0 else 'no'
    ret_dict['entertainment_news'] = entertainment_news

    tech_news = ''
    if staticInfo.has_key('tech_news'):
        tech_news = 'yes' if staticInfo.get('tech_news') > 0 else 'no'
    ret_dict['tech_news'] = tech_news

    offline_shopping = ''
    if staticInfo.has_key('offline_shopping'):
        offline_shopping = 'yes' if staticInfo.get('offline_shopping') > 0 else 'no'
    ret_dict['offline_shopping'] = offline_shopping

    online_shopping = ''
    if staticInfo.has_key('online_shopping'):
        online_shopping = 'yes' if staticInfo.get('online_shopping') > 0 else 'no'
    ret_dict['online_shopping'] = online_shopping
    return ret_dict


@app.errorhandler(403)
def permission_forbidden(e):
    flash('Permission denied!')
    # return redirect(url_for('index'))
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500
