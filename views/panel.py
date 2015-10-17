from flask import Blueprint, render_template, url_for, session, request, redirect, flash
from models import Dashboard, Developer
import requests

panel = Blueprint('panel', __name__, url_prefix='/')


@panel.route('/panel')
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