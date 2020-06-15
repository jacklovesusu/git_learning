# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 14:20:43 2020

@author: Administrator
"""


from flask import Flask,request,jsonify
import time
import datetime

from . import api
from app.model import get_db

@api.route('/behavior/proportion_results', methods=['POST'])
def proportion_results():
    '''
    获
    '''
    data = request.get_json()
    
    past_por_n = data['past_pro_n']
    
    db = get_db()['invitationCat']
    
    
    t_now = datetime.datetime.today()
    t_at_zero = t_now.replace(hour=0,minute=0,second=0,microsecond=0)
    past_str = str(t_at_zero - datetime.timedelta(days = int(past_por_n)))
    pastn_time_array = time.strptime(past_str,'%Y-%m-%d %H:%M:%S')
    past_n_stamp =  int(time.mktime(pastn_time_array) * 1000)
        
    pastpron_user_plays = db.actions.find({
            'behavior': 0,
            'createdAt':{'$gte':float(past_n_stamp)}
            }).count()#过去n天观看
    
    pastpron_user_comments = db.comments.find({
            'status': '1',
            'createdAt':{'$gte':float(past_n_stamp)}
            }).count()#过去n天评论

    pastpron_user_danmakus = db.danmakus.find({
            'status': '1',
            'createdAt':{'$gte':float(past_n_stamp)}
            }).count()#过去n天弹幕

    pastpron_user_follows = db.follows.find({
            'type':{'$in':[1,2,3]},
            'createdAt':{'$gte':float(past_n_stamp)}
            }).count()#过去n天收藏

    pastpron_user_preferences = db.preferences.find({
            'state': 1,
            'createdAt':{'$gte':float(past_n_stamp)}
            }).count()#过去n天点赞

    pastpron_user_shares = db.actions.find({
            'behavior': 6,
            'createdAt':{'$gte':float(past_n_stamp)}
            }).count()#过去n天分享    
    
    all_pro_nums = pastpron_user_plays + pastpron_user_comments + pastpron_user_danmakus + pastpron_user_follows+\
        pastpron_user_preferences+pastpron_user_shares
    
    
    return jsonify({
            'plays_pro_n':{float(pastpron_user_plays / all_pro_nums) * 100:'%'},
            'comments_pro_n':{float(pastpron_user_comments / all_pro_nums) * 100:'%'},
            'danmakus_pro_n':{float(pastpron_user_danmakus / all_pro_nums) * 100:'%'},
            'follows_pro_n':{float(pastpron_user_follows / all_pro_nums) * 100:'%'},
            'preferences_pro_n':{float(pastpron_user_preferences / all_pro_nums) * 100:'%'},
            'shares_pro_n':{float(pastpron_user_shares / all_pro_nums) * 100:'%'}
            })