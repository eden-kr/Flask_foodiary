# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 00:32:09 2020

@author: 82109
"""
from flask import Flask, jsonify, request
import matplotlib.pyplot as plt
from PIL import Image
import pymysql
import json

def dataToJson(header_data,data):
    header = [h[0] for h in header_data]
    res = []
    for d in data :
        res.append(dict(zip(header,d)))
    data = json.dumps(res,ensure_ascii=False)
    print(data)
    return data

app = Flask(__name__)
db = pymysql.connect(host="foodiary.ctfobxkhliur.ap-northeast-2.rds.amazonaws.com", user = "root", password="database", db="fooddata",read_timeout=80)

@app.route('/')
def main():
    return 'flask server is Ready'
@app.route('/image',methods = ['POST'])
def getImageToFoodData():
    res = ''
    if request.method == 'POST':
        try:
            f = request.files['file']   #파일객체 불러오기
            img = Image.open(f)
            string = sc.ImageToName(f)+'%'      #이미지 불러오는 cnn apply model
            sql = "select * from data where foodName like(%s) LIMIT 1"
            cursor = db.cursor
            cursor.execute(sql,string)
            res = dataToJson(cursor.description,cursor.fetchone())
            return res
        except Exception as e:
            print(e)
        cursor.close()
        return jsonify(res)
        

#영양정보 가져오기
@app.route('/get_food_data',methods = ["POST"])
def getNutrient(): 
    topic = request.form['foodName']
    print('받아온 단어',topic)
    word = topic+'%'
    res = ''
    try:
        sql = "select * from data where foodName Like(%s) LIMIT 20"
        cursor = db.cursor()
        cursor.execute(sql,word)
        res = dataToJson(cursor.description, cursor.fetchall()) #헤더 + 값      
        return res
    except Exception as e:
        print(e)
    cursor.close()
    return jsonify(res)


    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.run(threaded=False)