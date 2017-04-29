import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import datetime
from sklearn.svm import LinearSVC
from sklearn.neural_network import MLPClassifier
#how many most popular words we consider
n_features = 7500

df = pd.DataFrame.from_csv('F:\\Mini4\\Data Mining\\Amazon Project\\Data\\DataWithSentimentAndTopics.csv',index_col=None)

df = df.drop(['reviewerID', 'asin'], axis=1)

#normalizing values of some fields and changing names to avoid clashes with vectorizer
scaler = StandardScaler()

df['productPrice'] = scaler.fit_transform(df['price'].values.reshape(-1, 1))
df['overallScore'] = scaler.fit_transform(df['overall'].values.reshape(-1, 1))
df = df.drop(['overall', 'price'], axis=1)
df['LenSummary'] = scaler.fit_transform(df['LenSummary'].values.reshape(-1, 1))
df['LenReview'] = scaler.fit_transform(df['LenReview'].values.reshape(-1, 1))


#binning target variable into 2 bins.
df['helpfulVote'] = pd.cut(df['helpful'],[-1,0,100000], labels = [0,1])
df = df.drop(['helpful'], axis=1)

#vectorizing text
tf_vectorizer = TfidfVectorizer(max_df=0.5, min_df=2,
                                max_features=n_features,
                                stop_words='english')

#getting the TF matrix
tf = tf_vectorizer.fit_transform(df['reviewText'])

for i, col in enumerate(tf_vectorizer.get_feature_names()):
    df[col] = pd.SparseSeries(tf[:, i].toarray().ravel(), fill_value=0)



#splitting into train and test
X_train, X_test, y_train, y_test = train_test_split(df.drop(['helpfulVote', 'Summary', 'reviewText'], axis=1), df['helpfulVote'], test_size=0.1)

del(df)

#creating LRC
lrc = LogisticRegression(class_weight = 'balanced')

print('Training LRC')
print(datetime.datetime.now())
#fit classifier
lrc.fit(X_train, y_train)
print('Done training LRC')
print(datetime.datetime.now())

#get results
predicted = pd.DataFrame(y_test.get_values(), columns=['helpfulVote'])
predicted.insert(1, 'predResultLRC', lrc.predict(X_test))

#confusion matrix (left - true values, top - predicted)
print(confusion_matrix(predicted['helpfulVote'], predicted['predResultLRC']))

#creating MLP
mlp = MLPClassifier(hidden_layer_sizes=[1500,1000,500, 250])

print('Training MLP')
print(datetime.datetime.now())
#fit classifier
mlp.fit(X_train, y_train)
print('Done training MLP')
print(datetime.datetime.now())

predicted.insert(1, 'predResultMLP', mlp.predict(X_test))

#confusion matrix (left - true values, top - predicted)
print(confusion_matrix(predicted['helpfulVote'], predicted['predResultMLP']))

#creating SVM
svm = LinearSVC(class_weight='balanced')

print('Training SVM')
print(datetime.datetime.now())
#fit classifier
svm.fit(X_train, y_train)
print('Done training SVM')
print(datetime.datetime.now())

predicted.insert(1, 'predResultSVM', svm.predict(X_test))

#confusion matrix (left - true values, top - predicted)
print(confusion_matrix(predicted['helpfulVote'], predicted['predResultSVM']))


print('Combining predictions')
#combining predictions
predicted.insert(1, 'CombinedPrediction', predicted[['predResultLRC', 'predResultMLP', 'predResultSVM']].median(axis=1))

print(confusion_matrix(predicted['helpfulVote'], predicted['CombinedPrediction']))

