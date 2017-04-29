import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer



def get_Sentiment(df, sid):
    sentiments = []
    for text in df:
        ss = sid.polarity_scores(text)
        sentiments.append(ss['compound'])
    return sentiments


#load data
df = pd.DataFrame.from_csv('F:\\Mini4\\Data Mining\\Amazon Project\\Data\\FinalDataSmall.csv')

#sentiment analyzer
sid = SentimentIntensityAnalyzer()

sentiments = get_Sentiment(df['reviewOrig'], sid)
                           
#add to original df
df['reviewSentiment'] = sentiments

df.drop(['reviewOrig'], axis=1).to_csv('F:\\Mini4\\Data Mining\\Amazon Project\\Data\\DataWithSentiment.csv', header=True)