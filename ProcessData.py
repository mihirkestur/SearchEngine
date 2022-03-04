import re
import unidecode
import string
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from nltk.stem import WordNetLemmatizer
lm = WordNetLemmatizer()

def PreProcess(text):
    # Convert to lower case i.e. case folding
    text = text.lower()
    text = unidecode.unidecode(text)
    
    # Removing spl characters
    text = re.sub('\[.*?\]', '', text)
    
    # Removing urls/links
    remove_url = re.sub('https?://\S+|www\.\S+', '', text)
    
    # Removing tags
    remove_tag = re.sub('<.*?>+', '', remove_url)
    
    # Removing punctuation
    text = re.sub(f'[{re.escape(string.punctuation)}]', '', remove_tag)
    
    # Removing new lines
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    
    return text

def CleanData(documents):
    NumDocs = len(documents)
    # Cleaning
    for doc in range(NumDocs): documents[doc]["processed"] = documents[doc].text.apply(PreProcess)
    # Tokenizing
    for doc in range(NumDocs): documents[doc].processed = documents[doc].processed.apply(word_tokenize)
    # Remove stop words
    for doc in range(NumDocs): documents[doc].processed = documents[doc].processed.apply(lambda processed: [w for w in processed if w not in stopwords.words('english')])
    # Stemming
    for doc in range(NumDocs): documents[doc].processed = documents[doc].processed.apply(lambda processed: [ps.stem(w) for w in processed])
    # Lemmatization
    for doc in range(NumDocs): documents[doc].processed = documents[doc].processed.apply(lambda processed: [lm.lemmatize(w) for w in processed])

def GetPosnPostList(row, docID):
    tokens = row["processed"]
    for t in range(len(tokens)):
        if(tokens[t] not in PosnPostingList):
            PosnPostingList[tokens[t]] = [[docID,[t]]]
        else:
            docThere = False
            for doc in PosnPostingList[tokens[t]]:
                if(doc[0] == docID):
                    docThere = True
                    doc[1].append(t)
                    break
            if(docThere == False):
                PosnPostingList[tokens[t]].append([docID,[t]])
    return row

PosnPostingList = dict()

def CreatePosnPostList(documents):
    NumDocs = len(documents)
    for doc in range(NumDocs): documents[doc].apply(GetPosnPostList, docID=doc, axis=1)
    pd.DataFrame([(i,j) for i,j in PosnPostingList.items()], columns=["Token", "PositionPostingList"])

