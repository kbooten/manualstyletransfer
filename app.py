
from flask import Flask, render_template, jsonify, request, make_response

from nltk import tokenize

import json,os

from SimTester import SimTester
simtester = SimTester()

from AuthorTest import AuthorTest
authortest = AuthorTest()

app = Flask(__name__)


import random

def is_it_like_author(msg):
	return float(authortest.author_test(msg))

def is_it_similar(s1,s2):
	return (simtester.sim_score(s1,s2))*-1

@app.route("/get", methods=["GET"])
def get_bot_response():
	msg = request.args.get('msg')
	other_sent = request.args.get('startSent')
	author_score = is_it_like_author(msg)
	sim_score = is_it_similar(msg,other_sent)
	return jsonify({"cond1":author_score, "cond2":sim_score})


@app.route('/', methods=['GET', 'POST'])
def main():
	resp = make_response(render_template("game.html"))
	return resp

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)