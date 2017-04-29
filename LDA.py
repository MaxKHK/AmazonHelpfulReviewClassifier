import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


#how many topics we want
n_topics = 20
#how many most popular words we consider
n_features = 7500

#how many top words from topic
n_top_words = 20

#load data
df = pd.DataFrame.from_csv('F:\\Mini4\\Data Mining\\Amazon Project\\Data\\DataWithSentiment.csv',index_col=None)


#build count vector matrix of words in reviews. Notice, we remove words which are in 95% of all reviews
#and wods which occur less than 2 times in reviews (that will typos most likely)
#also we kill english stop words (built in list of terms which are too common or meaningless for task)
tf_vectorizer = CountVectorizer(max_df=0.5, min_df=2,
                                max_features=n_features,
                                stop_words='english')


#getting the TF matrix
tf = tf_vectorizer.fit_transform(df['reviewText'])


#fitting the LDA
lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=50,
                                learning_method='batch',
                                learning_offset=50.,
                                random_state=0)

lda.fit(tf)


#getting top words from topic
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()

#getting topics
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)


#getting topics of the docs
topics = pd.DataFrame(lda.transform(tf))

result = pd.concat([df, topics], axis=1)

#adding topics to the dataframe
result.to_csv('F:\\Mini4\\Data Mining\\Amazon Project\\Data\\DataWithSentimentAndTopics.csv', index = False, header=True)
#topics of specific row (notice in final file 2nd row is index 0 in topics)
#topics.loc[33,]