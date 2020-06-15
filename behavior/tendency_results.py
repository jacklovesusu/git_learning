# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 08:16:23 2020

@author: Administrator
"""


import pymongo
from flask import Flask,request,jsonify
import time
import datetime

from . import api
from app.model import get_db


@api.route('/behavior/tendency_results', methods=['POST'])
def tendency_results():
    
    data = request.get_json()
    past_n = data['past_n']
    db = get_db()['invitationCat']
    
    t_now = datetime.datetime.today()
    t_at_zero = t_now.replace(hour=0,minute=0,second=0,microsecond=0)
    past_str = str(t_at_zero - datetime.timedelta(days = int(past_n)))
    pastn_time_array = time.strptime(past_str,'%Y-%m-%d %H:%M:%S')
    past_n_stamp =  int(time.mktime(pastn_time_array) * 1000)
    
    past_str_one = str(t_at_zero - datetime.timedelta(days = int(past_n)-1))
    pastn_time_array_one = time.strptime(past_str_one,'%Y-%m-%d %H:%M:%S')
    past_n_stamp_one =  int(time.mktime(pastn_time_array_one) * 1000)
    
    
        
    pastn_user_plays = db.actions.find({
            'behavior': 0,
            'createdAt':{'$gte':float(past_n_stamp),'$lt':float(past_n_stamp_one)}
            }).count()#过去第n天观看
    
    pastn_user_comments = db.comments.find({
            'status': '1',
            'createdAt':{'$gte':float(past_n_stamp),'$lt':float(past_n_stamp_one)}
            }).count()#过去第n天评论

    pastn_user_danmakus = db.danmakus.find({
            'status': '1',
            'createdAt':{'$gte':float(past_n_stamp),'$lt':float(past_n_stamp_one)}
            }).count()#过去第n天弹幕

    pastn_user_follows = db.follows.find({
            'type':{'$in':[1,2,3]},
            'createdAt':{'$gte':float(past_n_stamp),'$lt':float(past_n_stamp_one)}
            }).count()#过去第n天收藏

    pastn_user_preferences = db.preferences.find({
            'state': 1,
            'createdAt':{'$gte':float(past_n_stamp),'$lt':float(past_n_stamp_one)}
            }).count()#过去第n天点赞

    pastn_user_shares = db.actions.find({
            'behavior': 6,
            'createdAt':{'$gte':float(past_n_stamp),'$lt':float(past_n_stamp_one)}
            }).count()#过去第n天分享    
    
    all_tend_nums = pastn_user_plays + pastn_user_comments + pastn_user_danmakus + pastn_user_follows+\
        pastn_user_preferences+pastn_user_shares
    
    
    return jsonify({
            'plays_n':{float(pastn_user_plays / all_tend_nums) * 100:'%'},
            'comments_n':{float(pastn_user_comments / all_tend_nums) * 100:'%'},
            'danmakus_n':{float(pastn_user_danmakus / all_tend_nums) * 100:'%'},
            'follows_n':{float(pastn_user_follows / all_tend_nums) * 100:'%'},
            'preferences_n':{float(pastn_user_preferences / all_tend_nums) * 100:'%'},
            'shares_n':{float(pastn_user_shares / all_tend_nums) * 100:'%'}
            })