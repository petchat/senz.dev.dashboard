# -*- coding: utf-8 -*-
from leancloud import Object
from leancloud import LeanCloudError
from leancloud import Query
from leancloud import User


from wsgi import signer

import copy

#not_binary_label_dict = {'field':['field__manufacture', 'field__financial', 'field__infotech', 'field__law', 'field__agriculture', 'field__human_resource', 'field__commerce', 'field__natural', 'field__service', 'field__humanities', 'field__medical', 'field__architecture', 'field__athlete'], 'age':['age__16to35', 'age__35to55', 'age__55up', 'age__16down'], 'sport':['sport__basketball', 'sport__bicycling', 'sport__tabel_tennis', 'sport__football', 'sport__jogging', 'sport__badminton', 'sport__fitness'],'consumption': ['consumption__10000to20000', 'consumption__20000up', 'consumption__5000to10000', 'consumption__5000down'], 'occupation':['occupation__freelancer', 'occupation__supervisor', 'occupation__student', 'occupation__others', 'occupation__official', 'occupation__salesman', 'occupation__teacher', 'occupation__soldier', 'occupation__engineer']}
#binary_label_list = [u'ACG', u'indoorsman', u'game_show', u'has_car', u'game_news', u'entertainment_news', u'health', u'online_shopping', u'variety_show', u'business_news', u'tvseries_show', u'current_news', u'sports_news', u'tech_news', u'offline_shopping', u'pregnant', u'gender', u'study', u'married', u'sports_show', u'gamer', u'social', u'has_pet']
query_limit = 1000
APPLICATION_CLASS = 'BindingApplication'
STATIC_INFO_TABLE = 'MageiaAppStaticInfo'

user_profile_base_option = {
    'title' : {
        'textStyle':{
        'fontSize': 24,
        'fontWeight': 'bolder',
        # 'color': '#5f7d8c'
        'color': '#079d9e'

        } ,
        'subtextStyle':{
        'fontSize': 12,
        'fontWeight': 'normal',
        'color': '#079d9e'
        } ,
        'text': ''
    },
    'tooltip': {
        'trigger': 'axis'
    },
    'legend': {
        'x': 'right',
        'itemWidth': 40,
        'itemHeight': 24,
        'data': ''
    },

    'xAxis': [
        {
            'nameTextStyle':{
            'fontSize':14,
            'fontWeight':'bold'
            },
            'name': '',
            'type': 'category',
            'data' : ''
        }
    ],
    'yAxis' : [
        {   'nameTextStyle':{
            'fontSize':14,
            'fontWeight':'bold'
        },
            'name':'',
            'type': 'value'
        }
    ],
    'series': [
        {
            'barGap':'5%',
            'name':'man',
            'type':'bar',
            'itemStyle':{
                'normal':{
                    'color':'#7bcce7',
                    'barBorderRadius':4
                }

            },
            'data':''
        },
        {
            'barGap':'5%',
            'name':'woman',
            'type':'bar',
            'itemStyle':{
                'normal':{
                    'color':'#ffb200',
                    'barBorderRadius':4
                }

            },
            'data':''


        }
    ]
}


path_analysis_base_option = {
    'title': {
        'textStyle':{
        'fontSize': 24,
        'fontWeight': 'bolder',
        'color': '#079d9e'
} ,
        'subtextStyle':{
        'fontSize': 12,
        'fontWeight': 'normal',
        'color': '#079d9e'
} ,

        'text': 'Location percentage'
    },
    'tooltip ': {
        'trigger': 'axis'
    },
    'legend': {
        'x': 'right',
        'itemWidth': 40,
        'itemHeight': 24,
        'data': ['Location']
    },

    'xAxis' : [
        {
            'nameTextStyle':{
            'fontSize':14,
            'fontWeight':'bold'
            },
            'name': 'Name',
            'type': 'category',
            'data': '',

             'axisLabel':{
            'interval':0,
            'rotate':5
}
        }
    ],
    'yAxis': [
        {   'nameTextStyle':{
            'fontSize':14,
            'fontWeight':'bold'
        },
            'name':'Time Percentage',
            'type': 'value'
        }
    ],
'series': [
        {
            'name':'Location',
            'type':'bar',
            'itemStyle':{
                'normal':{
                    'color':'#69f0ae',
                    'barBorderRadius':4
                }

            },
            'data':''

        }

    ]
}


event_recognition_base_option= {
    'title': {
        'textStyle':{
        'fontSize': 24,
        'fontWeight': 'bolder',
        'color': '#079d9e'
} ,
        'subtextStyle':{
        'fontSize': 12,
        'fontWeight': 'normal',
        'color': '#079d9e'
} ,

        'text': 'Custom event statistics'
    },
    'tooltip': {
        'trigger': 'axis'
    },
    'legend': {
        'x': 'right',
        'itemWidth': 40,
        'itemHeight': 24,
        'data': [{
            'name': ''
        }]
    },
    'xAxis': [
        {
            'nameTextStyle':{
            'fontSize':10,
            'fontWeight':'bold'
            },
            'name': 'Activity',
            'type': 'category',
            'data':'',

             'axisLabel':{
            'interval':0,
            'rotate':5
}
        }
    ],
    'yAxis': [
        {   'nameTextStyle':{
            'fontSize':14,
            'fontWeight':'bold'

        },
            'name':'Times',
            'type': 'value'
        }
    ],
'series': [
        {

            'name':'',
            'type':'bar',
            'itemStyle':{
                'normal':{
                    'color':'#e11f78',
                    'barBorderRadius':4
                }
            },
            'data':''

        }

    ]
}



class Dashboard:
    def __init__(self):
        self.app_id = None
        pass

    def get_app_key(self,app_table=APPLICATION_CLASS):
        try:
            Application = Object.extend(app_table)
            query = Query(Application)
            query.equal_to('app_id',self.app_id)
            result_list = query.find()
            length = len(result_list)
            if length==0:
                print 'error: application not exists in table Applicaiton'
                return 0
            elif length != 1:
                print 'error: multi application exists in table Applicaiton'
                return 0
            else:
                app_key = result_list[0].get('app_key')
        except LeanCloudError, e:

             raise e
        return app_key

    def get_demo_app_key(self,app_table=APPLICATION_CLASS):
        return self.get_app_key(app_table=app_table)

    def get_the_app(self,app_table=APPLICATION_CLASS,kind=None):
        try:
            if kind == 'demo':
                Application = Object.extend('DemoApplication')
            else:
                Application = Object.extend(APPLICATION_CLASS)
            query = Query(Application)
            query.equal_to('app_id',self.app_id)
            result_list = query.find()
            length = len(result_list)
            if length==0:
                print 'error: application not exists in table Application'
                return 0
            elif length != 1:
                print 'error: multi application exists in table Application'
                return 0
            else:
                app = result_list[0]
        except LeanCloudError, e:

             raise e
        return app

    def get_age_and_gender_data_dict(self,app_table=APPLICATION_CLASS,field_name = 'app',kind=None):
        # print app_table
        age_and_gender_dict={}
        try:
            app = self.get_the_app(kind=kind)
            static_info_table=STATIC_INFO_TABLE
            DbTable = Object.extend(static_info_table)
            query = Query(DbTable)
            query.equal_to(field_name,app)
            query.exists('age_and_gender')
            result_list = query.find()
            length = len(result_list)
            if length==0:
                print 'error: application not exists in table %s' %(str(static_info_table))
                return {}
            elif length > 1:
                print 'error: multi application  exists in table %s' %(str(static_info_table))
                # return 0

            app_static_info = result_list[0]
            age_and_gender_dict = app_static_info.get('age_and_gender')
            # return age_and_gender_dict

        except LeanCloudError, e:

             raise e
        return age_and_gender_dict

    # def get_demo_age_and_gender_data_dict(self,app_table='DemoApplication',field_name = 'app'):
    #     return self.get_age_and_gender_data_dict(app_table=app_table)

    def get_occupation_data_dict(self,app_table=APPLICATION_CLASS,field_name = 'app',kind=None):
        try:
            app = self.get_the_app(kind=kind)
            static_info_table=STATIC_INFO_TABLE
            DbTable = Object.extend(static_info_table)
            query = Query(DbTable)
            query.equal_to(field_name,app)
            query.exists('occupation')
            result_list = query.find()
            length = len(result_list)
            if length==0:
                print 'error: application not exists in table %s' %(str(static_info_table))
                return {}
            elif length > 1:
                print 'error: multi application  exists in table %s' %(str(static_info_table))
                # return 0

            app_static_info = result_list[0]
            occupation_dict = app_static_info.get('occupation')
            # return age_and_gender_dict

        except LeanCloudError, e:

             raise e
        return occupation_dict

    def get_sport_data_dict(self,app_table=APPLICATION_CLASS,field_name = 'app',kind=None):
        try:
            field = 'sport'
            app = self.get_the_app(kind=kind)
            static_info_table=STATIC_INFO_TABLE
            DbTable = Object.extend(static_info_table)
            query = Query(DbTable)
            query.equal_to(field_name,app)
            query.exists(field)
            result_list = query.find()
            length = len(result_list)
            if length==0:
                print 'error: application not exists in table %s' %(str(static_info_table))
                return {}
            elif length > 1:
                print 'error: multi application  exists in table %s' %(str(static_info_table))
                # return 0

            app_static_info = result_list[0]
            data_dict = app_static_info.get(field)
            # return age_and_gender_dict

        except LeanCloudError, e:

             raise e
        return data_dict


    def get_consumption_data_dict(self,app_table=APPLICATION_CLASS,field_name = 'app',kind=None):
        try:
            field = 'consumption'
            app = self.get_the_app(kind=kind)
            static_info_table=STATIC_INFO_TABLE
            DbTable = Object.extend(static_info_table)
            query = Query(DbTable)
            query.equal_to(field_name,app)
            query.exists(field)
            result_list = query.find()
            length = len(result_list)
            if length==0:
                print 'error: application not exists in table %s' %(str(static_info_table))
                return {}
            elif length > 1:
                print 'error: multi application  exists in table %s' %(str(static_info_table))
                # return 0
            app_static_info = result_list[0]
            data_dict = app_static_info.get(field)
            # return age_and_gender_dict
        except LeanCloudError, e:

             raise e
        return data_dict


    def get_field_data_dict(self,app_table=APPLICATION_CLASS,field_name = 'app',kind=None):
        try:
            field = 'field'
            app = self.get_the_app(kind=kind)
            static_info_table=STATIC_INFO_TABLE
            DbTable = Object.extend(static_info_table)
            query = Query(DbTable)
            query.equal_to(field_name,app)
            query.exists(field)
            result_list = query.find()
            length = len(result_list)
            if length==0:
                print 'error: application not exists in table %s' %(str(static_info_table))
                return {}
            elif length > 1:
                print 'error: multi application  exists in table %s' %(str(static_info_table))
                # return 0
            app_static_info = result_list[0]
            data_dict = app_static_info.get(field)
            # return age_and_gender_dict
        except LeanCloudError, e:

             raise e
        return data_dict

    # def get_demo_occupation_data_dict(self,app_table='DemoApplication',field_name='app'):
    #     return self.get_occupation_data_dict(app_table=app_table)

#下面三个函数的代码可以优化合并
    def get_location_distribution_data_dict(self,app_table=APPLICATION_CLASS,field_name = 'app',kind=None):
        try:

            app = self.get_the_app(kind=kind)
            static_info_table=STATIC_INFO_TABLE
            DbTable = Object.extend(static_info_table)
            query = Query(DbTable)
            query.equal_to(field_name,app)
            query.exists('location_percentage')
            result_list = query.find()
            length = len(result_list)
            if length==0:
                print 'error: application not exists in table %s' %(str(static_info_table))
                return {}
            elif length > 1:
                print 'error: multi application  exists in table %s' %(str(static_info_table))
            app_static_info = result_list[0]
            location_percentage_dict = app_static_info.get('location_percentage')
            # return location_percentage_dict

        except LeanCloudError, e:

             raise e
        return location_percentage_dict

    # def get_demo_location_distribution_data_dict(self,app_table='DemoApplication',field_name = 'app'):
    #     return self.get_location_distribution_data_dict(app_table=app_table)



    def get_motion_distribution_data_dict(self):
        field = 'motion'
        k = 5
        unknown = 'unknown'
        try:
            WeightedStaticInfo = Object.extend('WeightedUserContext')
            query = Query(WeightedStaticInfo)
            query.exists('objectId')
            query.select(field)
            # 这个地方后面需要做根据applicationid查询
            #另外也需要分组查询
            resultList = query.find()
            seen_location_dict = {}
            user_count = len(resultList)

            for result in resultList:
                location_dict = result.get(field)
                for key, valu in location_dict.items():
                    if key in seen_location_dict.keys():
                        seen_location_dict[key] += location_dict[key]
                    else:
                        seen_location_dict[key] = location_dict[key]
            total_unknown_location_value = seen_location_dict.get(unknown)
            #如果seen_location_dict中含有unknown字段的话，就删掉
            if total_unknown_location_value:
                del seen_location_dict[unknown]

            sorted_seen_location = sorted(seen_location_dict.items(), key=lambda l: l[1], reverse=True)
            sorted_frequent_location = sorted_seen_location[0:k]
            total_known_time = user_count - total_unknown_location_value
            sorted_frequent_location_percentage = [(str(kv[0]),(kv[1]/total_known_time)) for kv in sorted_frequent_location]
            sorted_frequent_location_percentage.append(('others',1-sum([kv[1] for kv in sorted_frequent_location_percentage])))



        except LeanCloudError, e:

             raise e
        return sorted_frequent_location_percentage

    def get_sound_distribution_data_dict(self):
        field = 'sound'
        k = 5
        unknown = 'unknown'
        try:
            WeightedStaticInfo = Object.extend('WeightedUserContext')
            query = Query(WeightedStaticInfo)
            query.exists('objectId')
            query.select(field)
            # 这个地方后面需要做根据applicationid查询
            #另外也需要分组查询
            resultList = query.find()
            seen_location_dict = {}
            user_count = len(resultList)

            for result in resultList:
                location_dict = result.get(field)
                for key, valu in location_dict.items():
                    if key in seen_location_dict.keys():
                        seen_location_dict[key] += location_dict[key]
                    else:
                        seen_location_dict[key] = location_dict[key]
            total_unknown_location_value = seen_location_dict.get(unknown)
            #如果seen_location_dict中含有unknown字段的话，就删掉
            if total_unknown_location_value:
                del seen_location_dict[unknown]

            sorted_seen_location = sorted(seen_location_dict.items(), key=lambda l: l[1], reverse=True)
            sorted_frequent_location = sorted_seen_location[0:k]
            total_known_time = user_count - total_unknown_location_value
            sorted_frequent_location_percentage = [(str(kv[0]),(kv[1]/total_known_time)) for kv in sorted_frequent_location]
            sorted_frequent_location_percentage.append(('others',1-sum([kv[1] for kv in sorted_frequent_location_percentage])))

        except LeanCloudError, e:

             raise e
        return sorted_frequent_location_percentage

    def get_event_to_activity_data(self,event_name=None,app_table=APPLICATION_CLASS,kind=None):

        # print app_table
        try:
            app = self.get_the_app(kind=kind)
            db_name = 'FakeEventActivity'
            DbTable  = Object.extend(db_name)
            query = Query(DbTable)
            #这里只是测试知道是少于1K条的
            query.equal_to('application',app)
            query.exists('activity_dict')
            if event_name:
                query.equal_to('event_name',event_name)
            # query.equal_to('application_id',application_id)
            query.descending('createdAt')
            query.limit(1)
            result_list = query.find()
            if result_list:
                # event_name = result_list[0].get('event_name')
                # activity_statistics_dict = {result_list[0].get('event_name'):result_list[0].get('activity_dict')}
                activity_statistics_dict = result_list[0].get('activity_dict')
            else:
                activity_statistics_dict=[]
        except LeanCloudError, e:

             raise e
        return activity_statistics_dict

    def get_event_to_location_data(self,event_name=None,app_table=APPLICATION_CLASS,kind=None):

        # print app_table
        try:

            app = self.get_the_app(kind=kind)
            db_name = 'FakeEventActivity'
            DbTable  = Object.extend(db_name)
            query = Query(DbTable)
            #这里只是测试知道是少于1K条的
            query.equal_to('application',app)
            query.exists('location_dict')
            if event_name:
                query.equal_to('event_name',event_name)
            # query.equal_to('application_id',application_id)
            query.descending('createdAt')
            query.limit(1)
            result_list = query.find()
            if result_list:
                # event_name = result_list[0].get('event_name')
                # activity_statistics_dict = {result_list[0].get('event_name'):result_list[0].get('activity_dict')}
                statistics_dict = result_list[0].get('location_dict')
            else:
                statistics_dict=[]
        except LeanCloudError, e:
             raise e
        return statistics_dict

    # def get_demo_event_to_activity_data(self,event_name=None,app_table='DemoApplication'):
    #    return  self.get_event_to_activity_data(event_name=event_name,app_table=app_table)
    # def get_demo_event_to_location_data(self,event_name=None,app_table='DemoApplication'):
    #    return  self.get_event_to_location_data(event_name=event_name,app_table=app_table)



    def get_user_profile_category_dict(self):
        # return {'occupation':'Occupation','taste':'Tastes'}
        return {'age':'Age&Gender','occupation':'Occupation','sport':'Sport','field':'Field','consumption':'Consumption'}

    def get_path_analysis_measure_dict(self):
        # return {'track':'Frequently Track'}
        return {'location':'Frequently Location'}

    def get_behavior_recognition_event_dict(self):
        return {'Event1':'Event1','Event2':'Event2'}

    def get_behavior_recognition_measure_dict(self):
        # return {'location':'Location','time':'Time'}
        return {'activity':'Activity','location':'Location'}



    def get_profile_option(self,category='age',kind=None):
        user_profile_option = {}
        status = 1
        if category == 'age':
            new_data_dict = self.get_age_and_gender_data_dict(kind=kind)
            if not new_data_dict:
                age_data = False
                age_category_list = []
                man_data_list = []
                woman_data_list = []
                status = 0

            else:
                age_data = True
                age_category_list = sorted(new_data_dict['man'].keys())
                man_data_list = [key[1] for key in sorted(new_data_dict['man'].items(),key=lambda l:l[0])]
                woman_data_list = [key[1] for key in sorted(new_data_dict['woman'].items(),key=lambda l:l[0])]

                user_profile_option = copy.deepcopy(user_profile_base_option)
                user_profile_option['title']['text'] = 'Age & Gender'
                user_profile_option['legend']['data'] = ['man', 'woman']
                user_profile_option['xAxis'][0]['name'] = 'Age Range'
                user_profile_option['xAxis'][0]['data'] = age_category_list   #['16down','16to35','35to55','55up']
                user_profile_option['yAxis'][0]['name'] = 'Total Amount'
                user_profile_option['series'][0]['name'] ='man'
                user_profile_option['series'][0]['data'] = man_data_list
                user_profile_option['series'][1]['name'] = 'woman'
                user_profile_option['series'][1]['data'] = woman_data_list

        elif category == 'occupation':
            new_data_dict = self.get_occupation_data_dict(kind=kind)
            if not new_data_dict:
                occupation_data = False
                occupation_category_list = []
                occupation_data_list = []
                status = 0

            else:
                if 'unknown' in new_data_dict.keys():
                    del new_data_dict['unknown']
                occupation_data = True
                occupation_category_list = [key[0] for key in sorted(new_data_dict.items(),key=lambda l:l[1])]
                occupation_data_list = [key[1] for key in sorted(new_data_dict.items(),key=lambda l:l[1])]

                user_profile_option = copy.deepcopy(user_profile_base_option)
                user_profile_option['title']['text'] = 'Occupation'
                user_profile_option['legend']['data'] = ['occupation']
                user_profile_option['xAxis'][0]['name'] = 'Occupations'
                user_profile_option['xAxis'][0]['data'] = occupation_category_list   #['16down','16to35','35to55','55up']
                user_profile_option['yAxis'][0]['name'] = 'Total Amount'
                user_profile_option['series'][0]['name'] ='occupation'
                user_profile_option['series'][0]['data'] = occupation_data_list
                del user_profile_option['series'][1]
            pass
        elif category == 'sport':
            new_data_dict = self.get_sport_data_dict(kind=kind)
            if not new_data_dict:
                has_data = False
                category_list = []
                data_list = []
                status = 0

            else:
                if 'unknown' in new_data_dict.keys():
                    del new_data_dict['unknown']
                has_data = True
                category_list = [key[0] for key in sorted(new_data_dict.items(),key=lambda l:l[1])]
                data_list = [key[1] for key in sorted(new_data_dict.items(),key=lambda l:l[1])]

                user_profile_option = copy.deepcopy(user_profile_base_option)
                user_profile_option['title']['text'] = 'Sport'
                user_profile_option['legend']['data'] = ['sport']
                user_profile_option['xAxis'][0]['name'] = 'Sports'
                user_profile_option['xAxis'][0]['data'] = category_list   #['16down','16to35','35to55','55up']
                user_profile_option['yAxis'][0]['name'] = 'Total Amount'
                user_profile_option['series'][0]['name'] ='sport'
                user_profile_option['series'][0]['data'] = data_list
                del user_profile_option['series'][1]
            pass
        elif category == 'consumption':
            new_data_dict = self.get_consumption_data_dict(kind=kind)
            if not new_data_dict:
                has_data = False
                category_list = []
                data_list = []
                status = 0
            else:
                if 'unknown' in new_data_dict.keys():
                    del new_data_dict['unknown']
                has_data = True
                category_list = [key[0] for key in sorted(new_data_dict.items(),key=lambda l:l[1])]
                data_list = [key[1] for key in sorted(new_data_dict.items(),key=lambda l:l[1])]

                user_profile_option = copy.deepcopy(user_profile_base_option)
                user_profile_option['title']['text'] = 'Consumption'
                user_profile_option['legend']['data'] = ['consumption']
                user_profile_option['xAxis'][0]['name'] = 'Consumptions'
                user_profile_option['xAxis'][0]['data'] = category_list   #['16down','16to35','35to55','55up']
                user_profile_option['yAxis'][0]['name'] = 'Total Amount'
                user_profile_option['series'][0]['name'] ='consumption'
                user_profile_option['series'][0]['data'] = data_list
                del user_profile_option['series'][1]

        elif category == 'field':
            new_data_dict = self.get_field_data_dict(kind=kind)
            if not new_data_dict:
                has_data = False
                category_list = []
                data_list = []
                status = 0
            else:
                if 'unknown' in new_data_dict.keys():
                    del new_data_dict['unknown']
                has_data = True
                category_list = [key[0] for key in sorted(new_data_dict.items(),key=lambda l:l[1])]
                data_list = [key[1] for key in sorted(new_data_dict.items(),key=lambda l:l[1])]


                user_profile_option = copy.deepcopy(user_profile_base_option)
                user_profile_option['title']['text'] = 'Field'
                user_profile_option['legend']['data'] = ['field']
                user_profile_option['xAxis'][0]['name'] = 'Fields'
                user_profile_option['xAxis'][0]['data'] = category_list   #['16down','16to35','35to55','55up']
                user_profile_option['yAxis'][0]['name'] = 'Total Amount'
                user_profile_option['series'][0]['name'] ='field'
                user_profile_option['series'][0]['data'] = data_list
                del user_profile_option['series'][1]
        else:
            pass
        option={}
        option['data']= user_profile_option
        option['status'] = status
        return option

    def get_path_option(self,category='location',kind=None):
        path_analysis_option = {}
        status=1

        if category == 'location':
            new_data_dict = self.get_location_distribution_data_dict(kind=kind)
            if not new_data_dict:
                location_data = False
                location_category_list = []
                location_data_list = []
                status = 0
            else:
                if 'unknown' in new_data_dict.keys():
                    del new_data_dict['unknown']
                location_data = True
                location_category_list = [key[0] for key in sorted(new_data_dict.items(),key=lambda l:l[1])]
                location_data_list = [key[1] for key in sorted(new_data_dict.items(),key=lambda l:l[1])]


                path_analysis_option = copy.deepcopy(path_analysis_base_option)
                path_analysis_option['title']['text'] = 'Location Percentage'
                path_analysis_option['legend']['data'] = ['location']
                path_analysis_option['xAxis'][0]['name'] = 'Locations'
                path_analysis_option['xAxis'][0]['data'] = location_category_list
                path_analysis_option['yAxis'][0]['name'] = 'Time percentage'
                path_analysis_option['series'][0]['name'] ='location'
                path_analysis_option['series'][0]['data'] = location_data_list
                pass
        elif category == 'track':
            pass
        else:
            pass
        option={}
        option['status'] = status
        option['data'] = path_analysis_option
        return  option

    def get_event_option(self,event_name=None,category=None,kind=None):
        event_recognition_option = {}
        status = 1
        if category == 'activity':
            new_data_dict = self.get_event_to_activity_data(event_name=event_name,kind=kind)
            if not new_data_dict:
                print 'new_data_dict is empty in get_event_option'
                behavior_data = False
                behavior_category_list = []
                behavior_data_list = []
                status = 0
            else:
                print 'new_data_dict is %s' %(str(new_data_dict))
                if 'others' in new_data_dict.keys():
                    del new_data_dict['others']
                behavior_data = True

                behavior_category_list = [key[0] for key in sorted(new_data_dict.items(),key=lambda l:l[1])]
                behavior_data_list = [key[1] for key in sorted(new_data_dict.items(),key=lambda l:l[1])]


                event_recognition_option = copy.deepcopy(event_recognition_base_option)
                event_recognition_option['title']['text'] = 'Custom Event Statistics'
                event_recognition_option['legend']['data'] = ['activity']
                event_recognition_option['xAxis'][0]['name'] = 'Activities'
                event_recognition_option['xAxis'][0]['data'] = behavior_category_list
                event_recognition_option['yAxis'][0]['name'] = 'Total Amount'
                event_recognition_option['series'][0]['name'] ='activity'
                event_recognition_option['series'][0]['data'] = behavior_data_list

        elif category == 'location':
            new_data_dict = self.get_event_to_location_data(event_name=event_name,kind=kind)
            if not new_data_dict:
                print 'new_data_dict is empty in get_event_option'
                behavior_data = False
                behavior_category_list = []
                behavior_data_list = []
                status = 0
            else:
                print 'new_data_dict is %s' %(str(new_data_dict))
                if 'unknown' in new_data_dict.keys():
                    del new_data_dict['unknown']
                behavior_data = True
                behavior_category_list = [key[0] for key in sorted(new_data_dict.items(),key=lambda l:l[1])]
                behavior_data_list = [key[1] for key in sorted(new_data_dict.items(),key=lambda l:l[1])]


                event_recognition_option = copy.deepcopy(event_recognition_base_option)
                event_recognition_option['title']['text'] = 'Custom Event Statistics'
                event_recognition_option['legend']['data'] = ['location']
                event_recognition_option['xAxis'][0]['name'] = 'Locations'
                event_recognition_option['xAxis'][0]['data'] = behavior_category_list
                event_recognition_option['yAxis'][0]['name'] = 'Total Amount'
                event_recognition_option['series'][0]['name'] ='location'
                event_recognition_option['series'][0]['data'] = behavior_data_list

        elif category == 'time':
            pass
        else:
            pass
        option ={}
        option['status'] = status
        option['data'] = event_recognition_option
        return option









#注意这里的Developer并没有继承自User
class Developer:
    def __init__(self,user_id=None):
        self.user = User()
        self.user_id = user_id

    @classmethod
    def is_valid_email(self,email):
        query = Query(User)
        query.exists('email',email)
        return 0 if query.find() else 1;

    def signup(self,email,username,password):
        self.user.set('email',email)
        self.user.set('username',username)
        self.user.set('password',password)
        self.user.set('type','developer')    # for distinguishing developer and tracker in the table _User
        try:
            result = self.user.sign_up()
            print result
            return 1
        except LeanCloudError,e:
            print e
            return 0

    def login_with_email(self,email,password):
        # self.user.login(email,password)
        pass

    def login_with_username(self,username,password):
        try:
            self.user.login(username,password)
            self.user_id = self.user.id
            self.session_token = self.user.get_session_token()
            print 'user.id: %s' %(str(self.user_id))
            print 'session_token: %s' %(str(self.session_token))
            return 1
        except LeanCloudError,e:
            print e
            return 0

    def init_developer_with_user_id(self,user_id):
        query = Query(User)
        query.equal_to('objectId',user_id)
        result = query.find()
        if len(result)==1:
            return result[0]
        else:
            print len(result)
            print user_id

    def get_all_application(self):
        try:
            # 这里认为应用的数量少于1000
            Application = Object.extend(APPLICATION_CLASS)
            query = Query(Application)
            query.equal_to('user',self.user.become(self.session_token))
            query.ascending('createdAt')
            query.limit(1000)
            result_list = query.find()
            all_application_dict = {}
            if result_list:
                for result in result_list:
                    all_application_dict[result.get('app_name')] = result.get('app_id')

            self.all_application_dict = all_application_dict
            return 1
        except LeanCloudError,e:
            print e
            return 0

    def get_all_demo_application(self):
        try:
            # 这里认为应用的数量少于1000
            Application = Object.extend(APPLICATION_CLASS)
            query = Query(Application)
            # query.equal_to('user',self.user.become(self.session_token))
            query.ascending('createdAt')
            query.equal_to('type','demo')
            query.limit(1000)
            result_list = query.find()
            all_demo_application_dict = {}
            if result_list:
                for result in result_list:
                    all_demo_application_dict[result.get('app_name')] = result.get('app_id')

            self.all_demo_application_dict = all_demo_application_dict
            return 1
        except LeanCloudError,e:
            print e
            return 0


    def get_all_tracker(self):
        try:
            # 这里认为应用的数量少于1000
            Tracker = Object.extend('Tracker')
            query = Query(Tracker)
            query.exists('objectId')
            query.ascending('createdAt')
            query.limit(1000)
            result_list = query.find()
            all_tracker_dict = {}
            if result_list:
                for result in result_list:
                    all_tracker_dict[result.get('username')] = result.id

            self.all_tracker_dict = all_tracker_dict
            return 1
        except LeanCloudError,e:
            print e
            return 0

    def create_new_app(self,app_name):
        try:
            if not app_name:
                return 0
            user = self.user.become(self.session_token)
            print 'Got the user'
            Application = Object.extend(APPLICATION_CLASS)
            application = Application()
            query = Query(Application)
            query.equal_to('user',user)
            query.equal_to('app_name',app_name)
            if query.find():
                print 'Application name exists!'
                return 0
            else:
                print 'Application name not exists! '
                application.set('app_name',app_name)
                application.set('user',user)
                application.save()
                app_id = application.id
                app_key = (signer.sign(app_id).split(app_id+'.'))[1]
                # app_key = app_id+"this is app_key"

                application.set('app_id',app_id)
                application.set('app_key',app_key)
                application.save()
                return 1
        except LeanCloudError,e:
            print e
            return 0

    def delete_app(self,app_id=None,kind=None):
        try:
            user = self.user.become(self.session_token)
            print 'Got the user'
            Application = Object.extend(APPLICATION_CLASS)
            application = Application()
            query = Query(Application)
            query.equal_to('user',user)
            query.equal_to('app_id',app_id)
            result = query.find()
            if result:
                print 'Application found!'
                result[0].destroy()
                return 0
            else:
                print 'Application  not exists! '

                application.save()
                return 1
        except LeanCloudError,e:
            print e
            return 0


            # query = Query(Application)
            # app_id = signer.sign(app_name).split(app_name+'.')[1]
            # query.equal_to('user',user)
            # query.equal_to('app_id',app_id)
            # if query.find():
            #     print 'Application name exists'
            #     return 0
            # else:
            #     application.set('app_name',app_name)
            #     application.set('app_id',app_id)
            #     application.set('user',user)
            #     application.save()

    def connect_new_tracker(self,tracker_id='',app_id=''):
        try:
            user = self.user.become(self.session_token)
            Application = Object.extend('Application')
            query = Query(Application)
            query.equal_to('user',user)
            query.equal_to('app_id',app_id)
            app_list = query.find()
            if len(app_list)!=1:
                print 'error with the length of app_list: %s' %(str(len(app_list)))
                return 0
            else:

                the_app = app_list[0]
                print 'successfully get the app with app_id: %s' %(str(the_app.id))

            Tracker = Object.extend('Tracker')
            query = Query(Tracker)
            query.equal_to('objectId',tracker_id)
            tracker_list = query.find()

            if len(tracker_list) != 1:
                print "error with the length of tracker_list: %s" %(str(len(tracker_list)))
                return 0
            else:
                the_tracker = tracker_list[0]
                print 'successfully get the tracker with object_id: %s' %(str(the_tracker.id))

                app_relation_to_tracker = the_app.relation('tracker')
                # tracker_relation_to_app = the_tracker.relation('application')
                app_relation_to_tracker.add(the_tracker)
                # tracker_relation_to_app.add(the_app)
                print 'ready to save'
                # the_tracker.save()
                # print 'successful save the_tracker'

                the_app.save()
                print 'successful save the_app'
                return 1

        except LeanCloudError,e:
            print e
            return 0

    def get_tracker_of_app(self, app_id=''):
        try:
            self.tracker_list = []
            #user = self.user.become(self.session_token)
            Application = Object.extend('Application')
            query = Query(Application)
            #query.equal_to('user', user)

            #app_id = 'demo 55f7e36f60b2fe7115171b4b'
            print "@@@@@@@@@@@@@@@@@@" + app_id
            query.equal_to('app_id', app_id)
            app_list = query.find()

            if len(app_list) != 1:
                return []
            the_app = app_list[0]

            #Tracker = Object.extend('BindingInstallation')
            #query = Query(Tracker)
            #query.equal_to('application', the_app)
            #app_list = query.find()
            relation = the_app.relation('tracker')
            print relation,
            return 1
        except LeanCloudError, e:
            print e
            return 0



