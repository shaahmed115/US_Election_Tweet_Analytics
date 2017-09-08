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
sparkConf = SparkConf().setMaster("local").setAppName("PredictKafkaTweetStreaming").set("spark.app.id", "Predict")
sc = SparkContext(appName="PythonSparkStreamingKafka_RM_01")
sc.setLogLevel("WARN")

with open('WordVectors.json') as data_file:    
    WordVectors= json.load(data_file)
Positive = open(os.getcwd() + "/positive.txt").read().splitlines()
Negative = open(os.getcwd() + "/negative.txt").read().splitlines()

sameModel = LogisticRegressionModel.load(sc, "model")

def MakeTuple(l):
	tweet=json.loads(l)
	loc = ""
	coords=""
	#print tweet
	if 'coordinates' in tweet and  not (tweet["coordinates"]  is None):
		#locAll=str(tweet["place"]["full_name"])
		#loc=locAll.split(',')[-1]
		#location= geolocator.geocode(str(tweet['place']['full_name']))
		#coords=str(str(location.longitude) + ',' + str(location.latitude))
		coords=tweet["coordinates"]
	try:
		text = tweet["text"]	
	except KeyError:
		text=""
		return ("blabla",0)
	posneg=float(PosNegCount(Positive,Negative).Sentiment(tweet['text'].encode('utf-8')))
	WV=float(WordVectorAnalyzer(stop_words,WordVectors,Positive,Negative).FindTweetSentiment(tweet['text'].encode('utf-8')))
	sentiment=int(sameModel.predict(array([WV,posneg])))
	l = (text,coords,int(sentiment)-1)
	#l = (text,int(sentiment)-1)
	print l
	return l

#ReviewByLocRDD = sc.parallelize(tweets).map(lambda l: MakeTuple(l)).filter(lambda x:x[0] != "").map(lambda x :(x[0],x[2])).reduceByKey(lambda a,b:a+b).collect()
#ReviewByLocRDD = sc.parallelize(tweets).map(lambda l: MakeTuple(l)).filter(lambda x:x[0] != "").collect()

from pyspark.streaming import StreamingContext  
from pyspark.streaming.kafka import KafkaUtils
import json 
topic = "trumpstream"
ssc = StreamingContext(sc, 30)
tweets = KafkaUtils.createStream(ssc, "localhost:2181",'spark-streaming', {topic:1})  
#lines = tweets.map(lambda l: MakeTuple(l)).filter(lambda x:x[0]!="")
lines = tweets.map(lambda l:MakeTuple(l[1]))
#lines = tweets.map(lambda x: x[1]).filter(lambda x: len(x)>0)
lines.pprint()
ssc.start()
ssc.awaitTermination()

