# -*- coding: utf-8 -*-
import leancloud
from leancloud import Object
from leancloud import LeanCloudError
from leancloud import Query
from leancloud import User


from wsgi import signer



not_binary_label_dict = {'field':['field__manufacture', 'field__financial', 'field__infotech', 'field__law', 'field__agriculture', 'field__human_resource', 'field__commerce', 'field__natural', 'field__service', 'field__humanities', 'field__medical', 'field__architecture', 'field__athlete'], 'age':['age__16to35', 'age__35to55', 'age__55up', 'age__16down'], 'sport':['sport__basketball', 'sport__bicycling', 'sport__tabel_tennis', 'sport__football', 'sport__jogging', 'sport__badminton', 'sport__fitness'],'consumption': ['consumption__10000to20000', 'consumption__20000up', 'consumption__5000to10000', 'consumption__5000down'], 'occupation':['occupation__freelancer', 'occupation__supervisor', 'occupation__student', 'occupation__others', 'occupation__official', 'occupation__salesman', 'occupation__teacher', 'occupation__soldier', 'occupation__engineer']}
binary_label_list = [u'ACG', u'indoorsman', u'game_show', u'has_car', u'game_news', u'entertainment_news', u'health', u'online_shopping', u'variety_show', u'business_news', u'tvseries_show', u'current_news', u'sports_news', u'tech_news', u'offline_shopping', u'pregnant', u'gender', u'study', u'married', u'sports_show', u'gamer', u'social', u'has_pet']
query_limit = 1000
class Dashboard:
    def __init__(self):
        self.app_id = None
        pass

    def get_all_tracker(self):
        try:
            # 这里不能认为终端用户的数量少于1000
            Application = Object.extend('Application')
            query = Query(Application)
            query.equal_to('app_id',self.app_id)
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
    def get_age_and_gender_data_dict(self,table_name='AppStaticInfo',filed_name = 'app'):
        try:

            Application = Object.extend('Application')
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
                app = result_list[0]
                DbTable = Object.extend(table_name)
                query = Query(DbTable)
                query.equal_to(filed_name,app)
                result_list = query.find()
                length = len(result_list)
                if length==0:
                    print 'error: application not exists in table %s' %(str(table_name))
                    return 0
                elif length != 1:
                    print 'error: multi application  exists in table %s' %(str(table_name))
                    return 0
                else:
                    app_static_info = result_list[0]
                    age_and_gender_dict = app_static_info.get('age_and_gender')
                    return age_and_gender_dict


            # WeightedStaticInfo  = Object.extend('WeightedStaticInfo')
            # query = Query(WeightedStaticInfo)
            # query.exists('objectId')
            # query.select('age','gender')
            # staticInfoList = query.find()
            # gender_type_list =['man','woman']
            # age_type_list = ['16down','16to35','35to55','55up']
            # dataDict ={gender_type:{age_type:0 for age_type in age_type_list} for gender_type in gender_type_list}
            #
            # for staticInfo in staticInfoList:
            #     gender = 'man' if staticInfo.get('gender') >0 else 'woman'
            #     age_info_dict= staticInfo.get('age')
            #     dataDict[gender][age_info_dict.keys()[0]] += 1
            # # dataDict ={'man' if staticInfo.get('gender') >0 else 'woman':dataDict['man' if staticInfo.get('gender') >0 else 'woman'][staticInfo.get('age').keys()[0]] +=1 for staticInfo in staticInfoList}
            # new_data_dict = {key:[0 for i in range(4)] for key in dataDict.keys()}
            # for index ,age_type in enumerate(age_type_list):
            #     for gender_type in dataDict.keys():
            #         new_data_dict[gender_type][index] = dataDict[gender_type][age_type]

        except LeanCloudError, e:

             raise e
        return age_and_gender_dict

    def get_occupation_data_dict(self):
        try:
            WeightedStaticInfo  = Object.extend('WeightedStaticInfo')
            query = Query(WeightedStaticInfo)
            query.exists('objectId')
            staticInfoList = query.find()
            dataDict ={gender_type:{age_type:0 for age_type in age_type_list} for gender_type in gender_type_list}

            for staticInfo in staticInfoList:
                gender = 'man' if staticInfo.get('gender') >0 else 'woman'
                age_info_dict= staticInfo.get('age')
                dataDict[gender][age_info_dict.keys()[0]] += 1
            # dataDict ={'man' if staticInfo.get('gender') >0 else 'woman':dataDict['man' if staticInfo.get('gender') >0 else 'woman'][staticInfo.get('age').keys()[0]] +=1 for staticInfo in staticInfoList}
            new_data_dict = {key:[0 for i in range(4)] for key in dataDict.keys()}
            for index ,age_type in enumerate(age_type_list):
                for gender_type in dataDict.keys():
                    new_data_dict[gender_type][index] = dataDict[gender_type][age_type]

        except LeanCloudError, e:

             raise e
        return new_data_dict

#下面三个函数的代码可以优化合并
    def get_location_distribution_data_dict(self):
        field = 'location'
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
                for key, value in location_dict.items():
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





    def get_event_to_activity_data(self,application_id,event_name,db_name='EventActivity'):
        try:
            DbTable  = Object.extend(db_name)
            query = Query(DbTable)
            #这里只是测试知道是少于1K条的
            query.equal_to('event_name',event_name)
            # query.equal_to('application_id',application_id)
            query.descending('createdAt')
            query.limit(1)
            result = query.find()
            activity_statistics_dict = result[0].get('activity_dict')


        except LeanCloudError, e:

             raise e
        return activity_statistics_dict

            # query.select('user','timestamp')
            # resultList = query.find()
            # DBTable = Object.extend('MergedUserContext')
            # activity_dict = {}
            # total_count = len(resultList)
            # print 'the length of resultList is : %s' %(str(total_count))
            # for index1,result in enumerate(resultList):
            #     query = Query(DBTable)
            #     query.equal_to('user',result.get('user'))
            #     query.less_than_or_equal_to('startTime',result.get('timestamp'))
            #     query.greater_than_or_equal_to('endTime',result.get('timestamp'))
            #     resultList1 = query.find()
            #     if len(resultList1) == 1 or len(resultList1) == 2 :
            #         activity = resultList1[0].get('event')[0]
            #         if activity in activity_dict.keys():
            #             activity_dict[activity]+=1
            #         else:
            #             activity_dict[activity] =1
            #     else:
            #         print 'length of resultList1: %s' %(str(len(resultList1)))
            #         print 'Seems to be an error,index: %s,user: %s; timestamp: %s \n' %(str(index1),str(result.get('user').id),str(result.get('timestamp')))
            #
            # activity_dict['others'] = total_count-sum(activity_dict.values())






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
            Application = Object.extend('Application')
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
            user = self.user.become(self.session_token)
            Application = Object.extend('Application')
            application = Application()
            query = Query(Application)
            query.equal_to('user',user)
            query.equal_to('app_name',app_name)
            if query.find():
                print 'Application name exists!'
                return 0
            else:
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


































# # -*- coding: utf-8 -*-
# import leancloud
# from leancloud import Object
# from leancloud import LeanCloudError
# from leancloud import Query
# from leancloud import User
# import time
# import datetime
# import operator
# import numpy as np
# from logentries import LogentriesHandler
# import logging
# # from flask import current_app
#
# from wsgi import signer
#
#
# not_binary_label_dict = {'field':['field__manufacture', 'field__financial', 'field__infotech', 'field__law', 'field__agriculture', 'field__human_resource', 'field__commerce', 'field__natural', 'field__service', 'field__humanities', 'field__medical', 'field__architecture', 'field__athlete'], 'age':['age__16to35', 'age__35to55', 'age__55up', 'age__16down'], 'sport':['sport__basketball', 'sport__bicycling', 'sport__tabel_tennis', 'sport__football', 'sport__jogging', 'sport__badminton', 'sport__fitness'],'consumption': ['consumption__10000to20000', 'consumption__20000up', 'consumption__5000to10000', 'consumption__5000down'], 'occupation':['occupation__freelancer', 'occupation__supervisor', 'occupation__student', 'occupation__others', 'occupation__official', 'occupation__salesman', 'occupation__teacher', 'occupation__soldier', 'occupation__engineer']}
# binary_label_list = [u'ACG', u'indoorsman', u'game_show', u'has_car', u'game_news', u'entertainment_news', u'health', u'online_shopping', u'variety_show', u'business_news', u'tvseries_show', u'current_news', u'sports_news', u'tech_news', u'offline_shopping', u'pregnant', u'gender', u'study', u'married', u'sports_show', u'gamer', u'social', u'has_pet']
#
# class Dashboard:
#     def get_age_and_gender_data_dict(self):
#         try:
#             WeightedStaticInfo  = Object.extend('WeightedStaticInfo')
#             query = Query(WeightedStaticInfo)
#             query.exists('objectId')
#             query.select('age','gender')
#             staticInfoList = query.find()
#             gender_type_list =['man','woman']
#             age_type_list = ['16down','16to35','35to55','55up']
#             dataDict ={gender_type:{age_type:0 for age_type in age_type_list} for gender_type in gender_type_list}
#
#             for staticInfo in staticInfoList:
#                 gender = 'man' if staticInfo.get('gender') >0 else 'woman'
#                 age_info_dict= staticInfo.get('age')
#                 dataDict[gender][age_info_dict.keys()[0]] += 1
#             # dataDict ={'man' if staticInfo.get('gender') >0 else 'woman':dataDict['man' if staticInfo.get('gender') >0 else 'woman'][staticInfo.get('age').keys()[0]] +=1 for staticInfo in staticInfoList}
#             new_data_dict = {key:[0 for i in range(4)] for key in dataDict.keys()}
#             for index ,age_type in enumerate(age_type_list):
#                 for gender_type in dataDict.keys():
#                     new_data_dict[gender_type][index] = dataDict[gender_type][age_type]
#
#         except LeanCloudError, e:
#
#              raise e
#         return new_data_dict
#     def get_occupation_data_dict(self):
#         try:
#             WeightedStaticInfo  = Object.extend('WeightedStaticInfo')
#             query = Query(WeightedStaticInfo)
#             query.exists('objectId')
#             staticInfoList = query.find()
#             dataDict ={gender_type:{age_type:0 for age_type in age_type_list} for gender_type in gender_type_list}
#
#             for staticInfo in staticInfoList:
#                 gender = 'man' if staticInfo.get('gender') >0 else 'woman'
#                 age_info_dict= staticInfo.get('age')
#                 dataDict[gender][age_info_dict.keys()[0]] += 1
#             # dataDict ={'man' if staticInfo.get('gender') >0 else 'woman':dataDict['man' if staticInfo.get('gender') >0 else 'woman'][staticInfo.get('age').keys()[0]] +=1 for staticInfo in staticInfoList}
#             new_data_dict = {key:[0 for i in range(4)] for key in dataDict.keys()}
#             for index ,age_type in enumerate(age_type_list):
#                 for gender_type in dataDict.keys():
#                     new_data_dict[gender_type][index] = dataDict[gender_type][age_type]
#
#         except LeanCloudError, e:
#
#              raise e
#         return new_data_dict
#
# #下面三个函数的代码可以优化合并
#     def get_location_distribution_data_dict(self):
#         field = 'location'
#         k = 5
#         unknown = 'unknown'
#         try:
#             WeightedStaticInfo = Object.extend('WeightedUserContext')
#             query = Query(WeightedStaticInfo)
#             query.exists('objectId')
#             query.select(field)
#             # 这个地方后面需要做根据applicationid查询
#             #另外也需要分组查询
#             resultList = query.find()
#             seen_location_dict = {}
#             user_count = len(resultList)
#
#             for result in resultList:
#                 location_dict = result.get(field)
#                 for key, valu in location_dict.items():
#                     if key in seen_location_dict.keys():
#                         seen_location_dict[key] += location_dict[key]
#                     else:
#                         seen_location_dict[key] = location_dict[key]
#             total_unknown_location_value = seen_location_dict.get(unknown)
#             #如果seen_location_dict中含有unknown字段的话，就删掉
#             if total_unknown_location_value:
#                 del seen_location_dict[unknown]
#
#             sorted_seen_location = sorted(seen_location_dict.items(), key=lambda l: l[1], reverse=True)
#             sorted_frequent_location = sorted_seen_location[0:k]
#             total_known_time = user_count - total_unknown_location_value
#             sorted_frequent_location_percentage = [(str(kv[0]),(kv[1]/total_known_time)) for kv in sorted_frequent_location]
#             sorted_frequent_location_percentage.append(('others',1-sum([kv[1] for kv in sorted_frequent_location_percentage])))
#
#
#
#         except LeanCloudError, e:
#
#              raise e
#         return sorted_frequent_location_percentage
#     def get_motion_distribution_data_dict(self):
#         field = 'motion'
#         k = 5
#         unknown = 'unknown'
#         try:
#             WeightedStaticInfo = Object.extend('WeightedUserContext')
#             query = Query(WeightedStaticInfo)
#             query.exists('objectId')
#             query.select(field)
#             # 这个地方后面需要做根据applicationid查询
#             #另外也需要分组查询
#             resultList = query.find()
#             seen_location_dict = {}
#             user_count = len(resultList)
#
#             for result in resultList:
#                 location_dict = result.get(field)
#                 for key, valu in location_dict.items():
#                     if key in seen_location_dict.keys():
#                         seen_location_dict[key] += location_dict[key]
#                     else:
#                         seen_location_dict[key] = location_dict[key]
#             total_unknown_location_value = seen_location_dict.get(unknown)
#             #如果seen_location_dict中含有unknown字段的话，就删掉
#             if total_unknown_location_value:
#                 del seen_location_dict[unknown]
#
#             sorted_seen_location = sorted(seen_location_dict.items(), key=lambda l: l[1], reverse=True)
#             sorted_frequent_location = sorted_seen_location[0:k]
#             total_known_time = user_count - total_unknown_location_value
#             sorted_frequent_location_percentage = [(str(kv[0]),(kv[1]/total_known_time)) for kv in sorted_frequent_location]
#             sorted_frequent_location_percentage.append(('others',1-sum([kv[1] for kv in sorted_frequent_location_percentage])))
#
#
#
#         except LeanCloudError, e:
#
#              raise e
#         return sorted_frequent_location_percentage
#     def get_sound_distribution_data_dict(self):
#         field = 'sound'
#         k = 5
#         unknown = 'unknown'
#         try:
#             WeightedStaticInfo = Object.extend('WeightedUserContext')
#             query = Query(WeightedStaticInfo)
#             query.exists('objectId')
#             query.select(field)
#             # 这个地方后面需要做根据applicationid查询
#             #另外也需要分组查询
#             resultList = query.find()
#             seen_location_dict = {}
#             user_count = len(resultList)
#
#             for result in resultList:
#                 location_dict = result.get(field)
#                 for key, valu in location_dict.items():
#                     if key in seen_location_dict.keys():
#                         seen_location_dict[key] += location_dict[key]
#                     else:
#                         seen_location_dict[key] = location_dict[key]
#             total_unknown_location_value = seen_location_dict.get(unknown)
#             #如果seen_location_dict中含有unknown字段的话，就删掉
#             if total_unknown_location_value:
#                 del seen_location_dict[unknown]
#
#             sorted_seen_location = sorted(seen_location_dict.items(), key=lambda l: l[1], reverse=True)
#             sorted_frequent_location = sorted_seen_location[0:k]
#             total_known_time = user_count - total_unknown_location_value
#             sorted_frequent_location_percentage = [(str(kv[0]),(kv[1]/total_known_time)) for kv in sorted_frequent_location]
#             sorted_frequent_location_percentage.append(('others',1-sum([kv[1] for kv in sorted_frequent_location_percentage])))
#
#         except LeanCloudError, e:
#
#              raise e
#         return sorted_frequent_location_percentage
#
#
#
#
#
#     def get_event_to_activity_data(self,application_id,event_name,db_name='EventActivity'):
#         try:
#             DbTable  = Object.extend(db_name)
#             query = Query(DbTable)
#             #这里只是测试知道是少于1K条的
#             query.equal_to('event_name',event_name)
#             # query.equal_to('application_id',application_id)
#             query.descending('createdAt')
#             query.limit(1)
#             result = query.find()
#             activity_statistics_dict = result[0].get('activity_dict')
#
#
#         except LeanCloudError, e:
#
#              raise e
#         return activity_statistics_dict
#
#             # query.select('user','timestamp')
#             # resultList = query.find()
#             # DBTable = Object.extend('MergedUserContext')
#             # activity_dict = {}
#             # total_count = len(resultList)
#             # print 'the length of resultList is : %s' %(str(total_count))
#             # for index1,result in enumerate(resultList):
#             #     query = Query(DBTable)
#             #     query.equal_to('user',result.get('user'))
#             #     query.less_than_or_equal_to('startTime',result.get('timestamp'))
#             #     query.greater_than_or_equal_to('endTime',result.get('timestamp'))
#             #     resultList1 = query.find()
#             #     if len(resultList1) == 1 or len(resultList1) == 2 :
#             #         activity = resultList1[0].get('event')[0]
#             #         if activity in activity_dict.keys():
#             #             activity_dict[activity]+=1
#             #         else:
#             #             activity_dict[activity] =1
#             #     else:
#             #         print 'length of resultList1: %s' %(str(len(resultList1)))
#             #         print 'Seems to be an error,index: %s,user: %s; timestamp: %s \n' %(str(index1),str(result.get('user').id),str(result.get('timestamp')))
#             #
#             # activity_dict['others'] = total_count-sum(activity_dict.values())
#
#
#
#
#
#
#
# class Developer:
#     def __init__(self,user_id=None):
#         self.user = User()
#         self.user_id = user_id
#
#     @classmethod
#     def is_valid_email(self,email):
#         query = Query(User)
#         query.exists('email',email)
#         return 0 if query.find() else 1;
#
#     def signup(self,email,username,password):
#         self.user.set('email',email)
#         self.user.set('username',username)
#         self.user.set('password',password)
#         try:
#             result = self.user.sign_up()
#             print result
#             return 1
#         except LeanCloudError,e:
#             print e
#             return 0
#
#     def login_with_email(self,email,password):
#         # self.user.login(email,password)
#         pass
#
#     def login_with_username(self,username,password):
#         try:
#             self.user.login(username,password)
#             self.user_id = self.user.id
#             self.session_token = self.user.get_session_token()
#             print 'user.id: %s' %(str(self.user_id))
#             print 'session_token: %s' %(str(self.session_token))
#             return 1
#         except LeanCloudError,e:
#             print e
#             return 0
#
#     def init_developer_with_user_id(self,user_id):
#         query = Query(User)
#         query.equal_to('objectId',user_id)
#         result = query.find()
#         if len(result)==1:
#             return result[0]
#         else:
#             print len(result)
#             print user_id
#
#     def create_new_app(self,app_name):
#         try:
#             developer = self.init_developer_with_user_id(self.user_id)
#             signed_key = signer.sign(app_name)
#             Application = Object.extend('Application')
#             application = Application()
#             application.set('application_name',app_name)
#             application.set('user',developer)
#             application.save()
#             app_id = application.id
#             app_key = signer.sign(app_id).split(app_id+'.')[1]
#             application.set('app_id',app_id)
#             application.set('app_key',app_key)
#             application.save()
#             return 1
#         except LeanCloudError,e:
#             print e
#             return 0
#         pass
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#


