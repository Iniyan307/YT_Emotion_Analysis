from nltk.sentiment.vader import SentimentIntensityAnalyzer
from transformers import pipeline
classifier = pipeline("text-classification",model='bhadresh-savani/bert-base-go-emotion')

sid = SentimentIntensityAnalyzer()

import numpy as np
import pandas as pd
from datetime import datetime as dt

# import text2emotion as te


def sentimentAnalysisVader():
    
    today=dt.today().strftime('%d-%m-%y')
    filename="comments_"+today+".csv"

    df = pd.read_csv(filename)

    #delete unwanted columns
    df= df.drop(['videoId','authorProfileImageUrl','authorChannelUrl','authorDisplayName','textDisplay','authorChannelId','canRate','viewerRating','publishedAt','updatedAt','parentId','commentId'],axis=1)

    #delete excess data
    df = df.drop_duplicates()
    # print(df.shape[0])

    df['scores'] = df['textOriginal'].apply(lambda textOriginal: sid.polarity_scores(textOriginal))

    df['compound']  = df['scores'].apply(lambda score_dict: score_dict['compound'])

    df.loc[(df.compound <= -0.5), 'comp_score'] = 'Negative'  #Categorized Using loc ,multiple conditions not accepted
    df['comp_score'] = np.where((df['compound'] < -0.1) & (df['compound'] >-0.5), 'Slightly_Negative', df['comp_score'])
    df['comp_score'] = np.where((df['compound'] <= 0.1) & (df['compound'] >= -0.1), 'Neutral', df['comp_score'])
    df['comp_score'] = np.where((df['compound'] < 0.5) & (df['compound'] > 0.1), 'Slightly_Positive', df['comp_score'])
    df.loc[(df.compound >= 0.5), 'comp_score'] = 'Positive'

    sentiment = df["compound"].mean()
    # print(sentiment)

    Count = df.pivot_table(index = ['comp_score'], aggfunc ='size').to_dict()
    # print(Count)

    ne=Count.get('Negative')
    nu=Count.get('Neutral')
    po=Count.get('Positive')
    sn=Count.get('Slightly_Negative')
    sp=Count.get('Slightly_Positive')

    return sentiment,list(Count.items())

print(sentimentAnalysisVader())
# sentimentAnalysisVader()


def getEmotion(message):
    return classifier(message)[0]["label"]

def sentimentAnalysisBERT():
    today=dt.today().strftime('%d-%m-%y')
    filename="comments_"+today+".csv"
    df = pd.read_csv(filename)

    df= df.drop(['videoId','authorProfileImageUrl','authorChannelUrl','authorDisplayName','textDisplay','authorChannelId','canRate','viewerRating','publishedAt','updatedAt','parentId','commentId'],axis=1)
    df = df.drop_duplicates()

    df['sentiment'] = df['textOriginal'].apply(lambda x: getEmotion(x[:512]))
    Count = df.pivot_table(index = ['sentiment'], aggfunc ='size').sort_values(ascending=False)

    n=len(Count)-10
    if len(Count)>=10:
        Count.drop(Count.tail(n).index,inplace = True)
    Count=Count.to_dict()
    resultList = list(Count.items())
    return resultList
    

# print(sentimentAnalysisBERT())