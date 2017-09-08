import time
import numpy as np
import tweepy
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from kafka import SimpleProducer,KafkaClient
import sys
api_key="RoF9Qhnz3Y39sw05k4m7nja7x"
api_secret="hViTwMJdSBODyVQRAjtMd3eYrkCS0X3fvoHMtwCi2bOl2SXAxi"
access_token="734468284452622336-oAekH2StbBLZHSGsPbgFkdO1FuBkhPB"
access_token_secret="YpI4YTfJuCRaTiZQpyldaYqoRaoYYvIQDX0uSg3lcrZrC"
auth=tweepy.OAuthHandler(api_key,api_secret)
auth.set_access_token(access_token,access_token_secret)
from pymongo import MongoClient
client = MongoClient('localhost',27017)
db=client.test
api=tweepy.API(auth)
class listener(tweepy.StreamListener):
	def __init__(self):
		client = KafkaClient("localhost:9092")
		try:
			self.producer = SimpleProducer(client, async = True,
		                          batch_send_every_n = 1000,
								  batch_send_every_t = 10)
								  
			print 'Initialised'
		except e:
			print 'failed:',str(e)
	def on_data(self, data):
		#try:
		try:
			jsondata=json.loads(data)
			print jsondata
			self.producer.send_messages('trumpstream', str(data))
			db.trumpdb.insert(jsondata)
			return True
		except TypeError as e:
			print 'TypeError:',str(e)
			time.sleep(5)
			pass

	def on_error(self, status):

		print status
keyword_list = ["Trump","Hillary","Clinton"] #track list
auth = tweepy.OAuthHandler(api_key, api_secret) #OAuth object
auth.set_access_token(access_token, access_token_secret)
#while True:
#	try:
		#time.sleep(5)
twitterStream = tweepy.Stream(auth, listener()) 
twitterStream.filter(track=keyword_list, languages=['en'])  #call the filter method to run the Stream Object
#	except:
#		continue
