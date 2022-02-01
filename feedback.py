from flask import Flask, request, jsonify, Response, send_file, send_from_directory, abort
from flask_restful import Resource, Api, reqparse
import argparse
import pandas as pd
import os
from allennlp.predictors import Predictor
from lerc.lerc_predictor import LERCPredictor
import json
from collections import Counter

app = Flask(__name__)

# Loads an AllenNLP Predictor that wraps our model
predictor = Predictor.from_path(
    archive_path='https://storage.googleapis.com/allennlp-public-models/lerc-2020-11-18.tar.gz',
    predictor_name='lerc',
    cuda_device=0
)

mapping = {
 '1':'pinky_left',
 'q':'pinky_left',
 'a':'pinky_left',
 'z':'pinky_left',
 
 '2':'ring_left',
 'w':'ring_left',
 's':'ring_left',
 'x':'ring_left',

 '9':'ring_right',
 'o':'ring_right',
 'l':'ring_right',
 
 '3':'middle_left',
 'e':'middle_left',
 'd':'middle_left',
 'c':'middle_left',
 
 '8':'middle_right',
 'i':'middle_right',
 'k':'middle_right',
 
 '4':'index_left',
 '5':'index_left',
 'r':'index_left',
 't':'index_left',
 'f':'index_left',
 'g':'index_left',
 'v':'index_left',
 'b':'index_left',

 '6':'index_right',
 '7':'index_right',
 'y':'index_right',
 'u':'index_right',
 'h':'index_right',
 'j':'index_right',
 'n':'index_right',
 'm':'index_right',

 ' ': 'thumb'
 }
## Load our dataset
with open('/content/news_output_new(2).json') as f:
  data=json.load(f)

@app.errorhandler(404)
def pageNotFound(error):
    return ("page not found")

@app.errorhandler(500)
def raiseError(error):
    return (error)

def get_score(passage_no, q_no):
	global predictor, data

	json_batch = []
	all_answers = data[str(passage_no)]['answer_char_ranges_'+str(q_no)].split("|")
	for i in range(len(all_answers)):
		d = {
		'context': data[str(passage_no)]['story_text'],
		'question': data[str(passage_no)]['question_'+str(q_no)],
		'reference': all_answers[i], 
		'candidate': 'he is a senator'
		}
		json_batch.append(d)
	return [x['pred_score'] for x in predictor.predict_batch_json(json_batch)]

@app.route('/get_mocha_scores', methods=['GET'])
def get_mocha_scores(passage_no = '0', q_no = '1'):
	score = get_score(passage_no,q_no)
	return jsonify(score)

@app.route('/get_mistakes', methods=['GET'])
def get_mistakes(path = ''):
	global mapping
	data = pd.read_csv(path)
	data_new = data[data['type']=='KEYDOWN'].reset_index()
	key_seq = data_new['key'].tolist()

	ans = []
	v= []
	for i,k in enumerate(key_seq):
	  if k == 'Backspace':
	    val = v.pop()
	    if val in mapping:
	      ans.append(mapping[val])
	    else:
	      ans.append('pinky_right')
	  else:
	    v.append(k)
	rv = dict(Counter(ans))
	return jsonify(rv)

@app.route('/get_typing_speed', methods=['GET'])
def get_typing_speed(path = ''):
	data = pd.read_csv(path)
	data_new = data[data['type']=='KEYDOWN'].reset_index()
	# data_new['rolling'] = data_new.timestamp_ms.diff()
	# print(data_new['rolling'])
	total_time_elapsed = (data_new['timestamp_ms'].iloc[-1] - data_new['timestamp_ms'].iloc[0])/1000
	total_chars = len(data_new)
	wpm = (total_chars/(total_time_elapsed*5))*60
	return jsonify([wpm])

@app.after_request
def add_headers(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	return (response)

if __name__ == '__main__':
	app.run(port = 5000)