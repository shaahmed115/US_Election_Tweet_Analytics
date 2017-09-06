from pyspark import SparkContext
import nltk
import numpy
from math import log
import io
sc= SparkContext('local','pyspark')
RES_DIR = "/home/shaahmed115/BigData/"
f = io.open(RES_DIR + "testing.txt", "r", encoding="utf-8")
tweets = f.readlines()
f = io.open(RES_DIR + "testing.txt", "r", encoding="utf-8")
tweets_to_tag = f.readlines()
dist_tweets = sc.parallelize(tweets)
class PMI():
		def __init__(self,tweets_to_tag,tweets,dist_tweets):
			self.pos_words=open(RES_DIR + "positive.txt").read().splitlines()
			self.neg_words=open(RES_DIR + "negative.txt").read().splitlines()
			self.N = len(tweets)
			self.dist_tweets=dist_tweets
			self.tweets_to_tag = tweets_to_tag
			self.tweets=tweets
		def calc_prob(self,x):
			occurences=self.dist_tweets.map(lambda l:l.split()).map(lambda l:1 if x in l else 0).reduce(lambda a,b:a + b)
			return float(float(occurences)/float(self.N))
		def calc_bigram_prob(self,x,y):
			occurences=self.dist_tweets.map(lambda l:l.split()).map(lambda l:1 if x in l and y in l else 0).reduce(lambda a,b:a + b)
			return float(float(occurences)/float(self.N))
		def semantic_orientation(self):
			for t in self.tweets_to_tag:
				tokenized=nltk.word_tokenize(t)
				taglist=nltk.pos_tag(tokenized)
				target_tags = ["VB","JJR","JJ","JJS","VBD","NN"]
				Bigram = ("","")
				tag_len = len(taglist)
				semo = 0.0
				for i in range(0,tag_len):
					PMI = 0.0
					if (taglist[i][1] in target_tags) and ((taglist[i][0] in self.pos_words) or (taglist[i][0] in self.neg_words)):#Bigram for ADJ/VERB with NOUN
						x=taglist[i][0]
						for j in range(i+1,tag_len):
							if(taglist[j][1] == "NN"):
								y=taglist[j][0]
								break
						Px  = self.calc_prob(x)
						Py  = self.calc_prob(y)
						Pxy = self.calc_bigram_prob(x,y) 
						try:	
							PMI = PMI + float(log(Pxy/(Px * Py)))
						except:
							PMI = PMI + 1
						if x in self.pos_words:
							semo = semo + 1 * PMI
						if x in self.neg_words:
							semo = semo + (-1) * PMI
						
				if semo > 0:
					print "2.0"
				else:
					if semo < 0:
						print "0.0"
					else:
						print "1.0"
				

tagger = PMI(tweets,tweets_to_tag,dist_tweets)
tagger.semantic_orientation()
