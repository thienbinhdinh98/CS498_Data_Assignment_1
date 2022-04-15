import findspark

findspark.init()

from flask import Flask, request, redirect, url_for, jsonify
import asyncio
import sys
import json
import os
import pyspark
app = Flask(__name__)


@app.route("/greet")
def greet():
    return "Hello"

@app.route("/lengthCounts", methods=["GET"])
def cnt():
    f= open("sentence_count.json")
    j = json.load(f)
    f.close()
    return j

task = False

async def Job(json_data):
    word_list =  json_data["wordlist"]
    print(word_list)
    weights = dict(json_data["weights"])
    sc = pyspark.SparkContext()
    lines = sc.textFile("War_and_Peace.txt")
    sentence = lines.flatMap(lambda line: line.split("\n"))
    #now do real job here to do map reduce
    sentence_list = list(sentence.collect())
    mpp_dict = {}
    for s in sentence_list:
        w = 0
        for i in s:
            if(i.isalpha() and i in weights):
                w += weights[i]
        mpp_dict[s] = w

    res_dict = {}
    word_max = {}
    #i wanna check for every key, which are sentences, if word in that sentence, we pick the sentence with highest weight
    for word in word_list:
        res_dict[word] = ""
        word_max[word] = -10
        for sentence in mpp_dict:
            if(word in sentence):
                if mpp_dict[sentence] > word_max[word]:
                    word_max[word] = mpp_dict[sentence]
                    res_dict[word] = sentence
    print(res_dict)
                    
    with open("part4.json",'w')as outfile:
        json.dump(res_dict, outfile)
    return True

@app.route('/analyze',methods=['POST'])
async def analyze():
    json_data =  request.json
    run  = await Job(json_data)
    if(run == True):
        task = True
    return "analyzing"

@app.route('/result',methods=['GET'])
def result():
    
    f = open('part4.json')
    data = json.load(f)
    return data


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port = 80)
