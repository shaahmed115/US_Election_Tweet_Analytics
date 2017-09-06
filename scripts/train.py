from pymongo import MongoClient
from random import randint

client = MongoClient('localhost:27017')
db=client.test
tweets=db.trumpdb.find({},{'text':1,'place':1}).limit(100)

#Training samples
f1 = open('training_samples.txt', 'w')
#Sentiments of training samples(1:Positive,-1:Negative,0:Neutral)
f2 = open('training.txt', 'w')
#Training samples
f3 = open('testing_samples.txt', 'w')
#Sentiments of training samples(1:Positive,-1:Negative,0:Neutral)
f4 = open('testing.txt', 'w')
#List of already checked samples
trained_samples=[]
def generate_random(lower,upper):
	global trained_samples
	index = -1
	while True:
		index=randint(lower,upper)
		if index not in trained_samples:
			break
	trained_samples.append(index)	
	return index
def annotate_samples(lower,upper,fp1,fp2):
	for i in range(0,100):
			n=generate_random(lower,upper)
			tweet=tweets[n]['text'].encode('utf-8')
			print tweet
			choice =int(raw_input())
			fp1.write(str(tweet) + '\n')
			fp2.write(str(choice) + '\n')

annotate_samples(0,4000,f1,f2)
annotate_samples(5000,8000,f3,f4)

