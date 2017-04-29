import json
import gzip
import pandas as pd
from sqlalchemy import create_engine
import re
maxLines = 500000
whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')


def parseGZ(path):
  g = gzip.open(path, 'r')
  for l in g:
      #1st of january 2014
      if eval(l)['unixReviewTime']>1388534400:
          yield json.dumps(eval(l))

def parseGZmeta(path):
  g = gzip.open(path, 'r')
  for l in g:
      yield eval(l)


def parseJSON(path):
  g = open(path, 'r')
  for l in g:
      yield eval(l)


#Writing stuff to mysql
#not works because of column names or whatever
"""
engine = create_engine('mysql://root:password@localhost:3306/amazonreviewproject', echo=False)


for l in parseJSON("F:\\Mini4\\Data Mining\\Amazon Project\\Data\\ReviewsCleanSmall.json"):
    df = {}
    l['reviewText'] = ''.join(filter(whitelist.__contains__, l['reviewText']))
    l['reviewerName'] = ''.join(filter(whitelist.__contains__, l['reviewerName']))
    l['summary'] = ''.join(filter(whitelist.__contains__, l['summary']))
    df[0] = l
    dfInsert = pd.DataFrame.from_dict(df, orient='index')
    dfInsert.to_sql(name='reviewscleancsv', con=engine, if_exists = 'append', index=False)
"""

#writing reviews to csv    
f = open("F:\\Mini4\\Data Mining\\Amazon Project\\Data\\ReviewsCleanCSV.csv", 'a')    

needHeader = 0

i = 0
#skip unhelpful votes a bit
skipCounter = 0

for l in parseJSON("F:\\Mini4\\Data Mining\\Amazon Project\\Data\\ReviewsClean.json"):
    if len(l) != 9:
        continue
    df = {}
    l['helpful']=l['helpful'][0]
    if l['helpful'] == 0:
        if skipCounter == 3:
            skipCounter=0
        else:
            skipCounter+=1
            continue
    
    l['asin'] = re.sub('[^0-9]','', l['asin'])
    l['reviewOrig'] = l['reviewText'].replace(',', '')
    l['reviewText'] = re.sub(r'\b\w{1,4}\b', '', l['reviewText'])
    l['reviewText'] = filter(whitelist.__contains__, l['reviewText'].lower())
    l['reviewTime'] = filter(whitelist.__contains__, l['reviewTime'].lower())
    l['reviewText'] = ' '.join(l['reviewText'].split())
    if len (l['reviewText']) < 50: continue
    l['reviewerName'] = filter(whitelist.__contains__, l['reviewerName'].lower())
    l['summary'] = filter(whitelist.__contains__, l['summary'].lower())
    df[0] = l
    dfInsert = pd.DataFrame.from_dict(df, orient='index')
    if needHeader == 0:
        dfInsert.to_csv(f, index=False, header=True)
        needHeader = 1
    else:
        dfInsert.to_csv(f, index=False, header=False)
        i+=1
        if i > maxLines:
            break
    
f.close()



"""
#writing metadata to csv    
f = open("F:\\Mini4\\Data Mining\\Amazon Project\\Data\\Metadata.csv", 'a')    

needHeader = 0
i = 0

for l in parseGZmeta("F:\\Mini4\\Data Mining\\Amazon Project\\Data\\meta_Books.json.gz"):
    df = {}
    if None not in [l.get(key) for key in ['asin', 'price']]:
        #l['description'] = filter(whitelist.__contains__, l['description'].lower())
        df[0] = {k: l[k] for k in ('asin', 'price')}
    else:
        continue
    dfInsert = pd.DataFrame.from_dict(df, orient='index')
    if needHeader == 0:
        dfInsert.to_csv(f, index=False, header=True)
        needHeader = 1
    else:
        dfInsert.to_csv(f, index=False, header=False)
    #i+=1
    #if i > 10000: break;
        
f.close()
"""