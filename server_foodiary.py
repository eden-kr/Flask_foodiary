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

import numpy
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def ImageToName(file):
    image_w = 128
    image_h = 128
    X = []
    
    img = Image.open(file)
    img = img.convert("RGB")
    img = img.resize((image_w, image_h))
    data = np.asarray(img)      #이미지 배열 재생성
    X.append(data)
    X = np.array(X)

    #모델 불러오기
    from keras.models import load_model
    model = load_model("/home/ubuntu/data")
    model.summary()
    prediction = model.predict(X)
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    print('Using tensorflow..')
    cnt = 0
    categories = ["감바스","계란초밥","김치볶음밥","냉면","대구꿀떡","돈가스","돌솥비빔밥","떡볶이","미역국","바나나우유",
	"샐러드","쌀국수","연어회","육회","족발","짜장면","햄버거","허니브레드","후라이드치킨"]
    pre_ans_str = ""
    for i in prediction:
        pre_ans = i.argmax()  # 예측 레이블
        if pre_ans == 0: pre_ans_str = categories[0]
        elif pre_ans == 1: pre_ans_str = categories[1]
        elif pre_ans == 2: pre_ans_str = categories[2]
        elif pre_ans == 3: pre_ans_str = categories[3]
        elif pre_ans == 4: pre_ans_str = categories[4]
        elif pre_ans == 5: pre_ans_str = categories[5]
        elif pre_ans == 6: pre_ans_str = categories[6]
        elif pre_ans == 7: pre_ans_str = categories[7]
        elif pre_ans == 8: pre_ans_str = categories[8]
        elif pre_ans == 9: pre_ans_str = categories[9]
        elif pre_ans == 10: pre_ans_str = categories[10]
        elif pre_ans == 11: pre_ans_str = categories[11]
        elif pre_ans == 12: pre_ans_str = categories[12]
        elif pre_ans == 13: pre_ans_str = categories[13]
        elif pre_ans == 14: pre_ans_str = categories[14]
        elif pre_ans == 15: pre_ans_str = categories[15]
        elif pre_ans == 16: pre_ans_str = categories[16]
        elif pre_ans == 17: pre_ans_str = categories[17]
        elif pre_ans == 18: pre_ans_str = categories[18]

        for j in i:
            if j >= 0.7 : 
                print(pre_ans_str+"(으)로 추정됩니다.")
        return pre_ans_str
        cnt += 1
        
        
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
    global db
    if request.method == 'POST':
        try:
            f = request.files['file']   #파일객체 불러오기
            img = Image.open(f)
            string = ImageToName(f)+'%'      #이미지 불러오는 cnn apply model
            sql = "select * from data where foodName like(%s) LIMIT 1"
            cursor = db.cursor()
            cursor.execute(sql,string)
            res = dataToJson(cursor.description,cursor.fetchall())
            return res
        except Exception as e:
            print(e)
        cursor.close()
        return jsonify(res)
        

#영양정보 가져오기
@app.route('/get_food_data',methods = ["POST"])
def getNutrient(): 
    global db
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
