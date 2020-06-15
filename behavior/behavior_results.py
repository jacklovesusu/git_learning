# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 09:09:30 2020

@author: Administrator
"""


from flask import Flask,jsonify


from . import api
from app.model import get_db

@api.route('/behavior/results', methods=['GET'])
def results():
    '''
    获取用户数量、日用户活跃度、日观看活跃度、日观看活跃度
    '''
    db = get_db()['invitationCat']

    playandshare_user = len(list(
        db.actions.aggregate([
            {'$match': {'behavior': {'$in': [0, 6]}}},
            {'$project': {'user': 1}},
            {'$group': {'_id': '$user'}}
        ])
    ))

    comment_user = len(list(
        db.comments.aggregate([
            {'$match': {'status': '1'}},
            {'$project': {'user': 1}},
            {'$group': {'_id': '$user'}}
        ])
    ))

    danmaku_user = len(list(
        db.danmakus.aggregate([
            {'$match': {'status': '1'}},
            {'$project': {'user': 1}},
            {'$group': {'_id': '$user'}}
        ])
    ))

    follow_user = len(list(
        db.follows.aggregate([
            {'$match': {'type': {'$in': [1, 2, 3]}}},
            {'$project': {'user': 1}},
            {'$group': {'_id': '$user'}}
        ])
    ))

    preference_user = len(list(
        db.preferences.aggregate([
            {'$match': {'state': 1}},
            {'$project': {'user': 1}},
            {'$group': {'_id': '$user'}}
        ])
    ))
    oneday_play_active = playandshare_user + comment_user + danmaku_user + follow_user + preference_user

    all_users = db.users.find({'userType':{'$in':['entity','other']}}).count()

    one_user_plays = db.actions.find({'behavior': 0}).count()
    
    one_user_comments = db.comments.find({'status': '1'}).count()

    one_user_danmakus = db.danmakus.find({'status': '1'}).count()

    one_user_follows = db.follows.find({'type':{'$in':[1,2,3]}}).count()

    one_user_preferences = db.preferences.find({'state': 1}).count()

    one_user_shares = db.actions.find({'behavior': 6}).count()

    one_nums = one_user_plays + one_user_comments + one_user_danmakus + one_user_follows+\
        one_user_preferences + one_user_shares
   
    return jsonify({
        'all_users':all_users,
        'oneday_active_users':oneday_play_active,
        'oneday_play_active':{float(one_user_plays / one_nums) * 100:'%'},
        'oneday_active':{float((one_nums - one_user_plays) / one_nums) * 100:'%'}
        })