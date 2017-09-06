# US_Election_Tweet_Analytics
Sentiment analysis on Tweets related to US Election and classifying them as Pro-Hillary pro-Trump or neutral

###Environment:

  1.Python 2.7.9(tweepy,nltk) _You may need to use nltk.download() to use stopwords etc_.  
  2.spark-2.0.0

###Resources:
  Used the corpus of positive and negative words from 
  
  https://github.com/MKLab-ITI/image-verification-corpus/blob/master/mediaeval2015/src/featureextraction/resources/negative-words.txt
    
  https://github.com/MKLab-ITI/image-verification-corpus/blob/master/mediaeval2015/src/featureextraction/resources/positive-words.txt

Created a list of positive and negative emoticons from Wikipedia(not used yet)  
  

All features are tagged as 1(pro Trump) 2(pro Hillary).Anti-trump is assumed to imply pro-Hillary

###Features
So far only four features have been extracted and three used:
  PMI-Pointwise Mutual Information(PMI.py)
  
  Absoulte number of positive or negative words
  
  Closest word to Hillary or Trump keywords (positive or negative)
  
  Positive or Negative JJR JJS(Comparitive or Superlative) tag between Trump or Hillary (Hillary is deadlier than Trump),not used as matrix is very sparse

####Step 1: Stream Tweets

 1.Run the Streamer.py file in scripts.Set the paths to your directory
  
 2.It creates two files - Raw_Tweets.txt(tweets in original form) and Tokeised_Tweets.txt(tweets after tokenisation)

####Step2: Feature Extraction

Note:I havent used file writing because of a clash in python 2/3 created problems in formatting.So I just redirected the output to the files in resources directory

  1.Run the PMI.py,pos_neg_absolute.py,Distance.py in he scripts folder.These extract features and are stored with the same names in the Features folder(python PMI.py > ../Features/pmi,txt )(python Distance.py > ../Features/distance.txt)
  
    There is also the pos_tagger.py (To detect JJ tags (Trump is better than Hillary)) but there dont seem to be such tweets.So I havent used it
    
    The PMI calculates the Pointwise Mutual Index,the pos_neg_absolute.py finds the difference between positive and negative words,the Distance.py calculates the if positive or negative word is closer to trump/hillary/clinton/donald
    
  2.Hand classify the tweets:I have hand classified about 160 tweets into(2-pro Trump and 1-pro Hillary)
  
  3.Align the features into traing and testing files.Run the align_features_testing.py and align_features_training.py to create a files training.txt and testing.txt containing features of the form(class,feature1,feature2,feature3)
  

####Step3:  
Run the Bayes classifier:Run the NaiveBayes.py in scripts/

####Results:
Obtained 67.14 % accuracy for Naive_Bayes and 91.2% for LogisticRegression
  
