from pyspark import SparkContext,SparkConf
from random import randint
from pyspark.sql import *
import urllib
from pyspark.mllib.classification import LogisticRegressionWithLBFGS,LogisticRegressionModel
import os
from pyspark.mllib.feature import Word2Vec
from time import time
from pyspark.mllib.regression import LabeledPoint
from numpy import array
from classes.PosNeg import PosNegCount
from classes.WordVector import WordVectorAnalyzer
import nltk
import json
from nltk.tree import Tree
from geopy.geocoders import Nominatim
import json
from Levenstein import Lev
stop_words = nltk.corpus.stopwords.words('english')
stop_words+=['?','.','!',',']
geolocator = Nominatim()
sparkConf = SparkConf().setMaster("local").setAppName("Predict").set("spark.app.id", "Predict")
sc = SparkContext(conf=sparkConf)
inp = sc.textFile("WordTraining.txt").map(lambda row: row.split(" "))
word2vec = Word2Vec()
model = word2vec.fit(inp)
WordVectors = {}

for i in model.getVectors().keys():
    WordVectors[i] = model.findSynonyms(i,7)

Positive = open(os.getcwd() + "/positive.txt").read().splitlines()
Negative = open(os.getcwd() + "/negative.txt").read().splitlines()

sameModel = LogisticRegressionModel.load(sc, "model")

from pymongo import MongoClient
client = MongoClient('localhost:27017')
db=client.test
tweetList = []
tweets=db.tweetdb.find({},{'text': 1,'place': 1} )
def MakeTuple(tweet):
	loc = ""
	coords=""
	if tweet.get('place'):
		loc=str(tweet['place']['full_name']).split(',')[-1]
		location= geolocator.geocode(str(tweet['place']['full_name']))
		coords=str(str(location.longitude) + ',' + str(location.latitude))
	text = tweet['text']	
	posneg=float(PosNegCount(Positive,Negative).Sentiment(tweet['text'].encode('utf-8')))
	WV=float(WordVectorAnalyzer(stop_words,WordVectors,Positive,Negative).FindTweetSentiment(tweet['text'].encode('utf-8')))
	sentiment=int(sameModel.predict(array([WV,posneg])))
	l = (loc,coords,int(sentiment)-1)
	return l

#ReviewByLocRDD = sc.parallelize(tweets).map(lambda l: MakeTuple(l)).filter(lambda x:x[0] != "").map(lambda x :(x[0],x[2])).reduceByKey(lambda a,b:a+b).collect()
ReviewByLocRDD = sc.parallelize(tweets).map(lambda l: MakeTuple(l)).filter(lambda x:x[0] != "").collect()



for review in ReviewByLocRDD:
	print review

