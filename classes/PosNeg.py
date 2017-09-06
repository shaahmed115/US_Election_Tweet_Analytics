from pyspark import  SparkContext

class PosNegCount:
	def __init__(self,pos_words,neg_words):
		self.pos_words = pos_words
		self.neg_words = neg_words
	def Sentiment(self,line):
		pos = 0
		neg = 0
		for word in line.split():
			if word in self.pos_words:
				pos=pos+1
			if word in self.neg_words:
				neg=neg+1

		if(neg > pos):
			return 0.0 
		if(neg < pos):
			return  2.0 
		else:
			return 1.0
