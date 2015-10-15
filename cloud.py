# coding: utf-8

from leancloud import Engine, Object, Query
from app import app

engine = Engine(app)
TARGET_TABLE =  'MageiaAppStaticInfo'


@engine.define
def hello(**params):
    if 'name' in params:
        return 'Hello, {}!'.format(params['name'])
    else:
        return 'Hello, LeanCloud!'


# static_info_analyzer 从WeightedTrackerInfo中
# 取数据，处理后存入 MageiaAppStaticInfo(临时)
@engine.define
def static_info_analyzer(**params):
    ''' 根据POST来的数据进行计算'''
    targetTable = Object.extend(TARGET_TABLE)
    #target_table = targetTable()

    user_id = params.get('user')
    static_info = params.get('static_info')
    if not user_id or not static_info:    # invalid data
        return  False
    
    # 获取user对应的application 
    # 使用set去重
    # 后期需要解绑class

    user = Object.extend('_User').create_without_data(user_id)
    query = Query(Object.extend('BindingInstallation'))
    query.equal_to('user', user)
    query.select('application')
    install_list = query.find()
    app_obj = install_list[0].get('application')

    query = Query(targetTable)
    query.equal_to('app', app_obj)
    record = query.find()[0]


    # age and gender
    gender = 'unknown' if not static_info.get('gender') else 'man' if static_info.get('gender') > 0 else 'woman'
    age =  static_info.get('age')
    if age:
        age = age.keys()[0]
    else:
        age = 'unknown'
    age_and_gender = record.get('age_and_gender')
    if gender == 'unknown':
        try:
            age_and_gender[gender] += 1
        except:
            age_and_gender[gender] = 1
    else:
        try:
            age_and_gender[gender][age] += 1
        except:
            age_and_gender[gender][age] = 1
    record.set('age_and_gender', age_and_gender)

    # sport
    sport_dict = record.get('sport')
    sport = static_info.get('sport')
    if sport:
        sport = sport.keys()[0]
        try:
            sport_dict[sport] += 1
        except:
            sport_dict[sport] = 1
        record.set('sport', sport_dict)

    # occupation
    occupation_dict = record.get('occupation')
    occupation = static_info.get('occupation')
    if occupation:
        occupation = occupation.keys()[0]
        try:
            occupation_dict[occupation] += 1
        except:
            occupation_dict[occupation] = 1
        record.set('occupation', occupation_dict)

    # consumption
    consumption_dict = record.get('consumption')
    consumption = static_info.get('consumption')
    if consumption:
        consumption = consumption.keys()[0]
        try:
            consumption_dict[consumption] += 1
        except:
            consumption_dict[consumption] = 1
        record.set('consumption', consumption_dict)

    # field
    field_dict = record.get('field')
    field = static_info.get('field')
    if field:
        field = field.keys()[0]
        try:
            field_dict[field] += 1
        except:
            field_dict[field] = 1
        record.set('field', field_dict)

    record.save()
    return True


@engine.define
def custom_event_analyer(**params):
    pass
