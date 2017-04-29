# AmazonHelpfulReviewClassifier

The classifier system capable of predicting if review will be helpful on Amazon.

Uses text mining to do it.

How to use:
1) Download files from here: http://jmcauley.ucsd.edu/data/amazon/
2) Run ConvertAndCleanup.py to extract reviews from raw files into csv.
3) Import both Metadata and Reviews files into the MS SQL Server database
4) Run SQLPart.sql to merge metatdata with reviews and save into csv.
5) Run Sentiments.py to add sentiments of reviews into file
6) Run LDA.py to add LDA topic probabilities to each review
7) Run Classification.py to train classification algorithms which will predict how helpful the review will be
