import re
import unidecode
import pickle
import string
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from nltk.stem import WordNetLemmatizer
lm = WordNetLemmatizer()

PosnPostingList = dict()
PermIndex = dict()

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


def Permutize(permIndex, token):
    temp = token + "$"
    temp = temp[-1] + temp[:len(temp)-1]
    permIndex[temp] = token
    while(temp[-1] != "$"):
        permIndex[temp] = token
        temp = temp[-1] + temp[:len(temp)-1]

"""
Main function to create the posn posting list
Returns the posn posting list
"""
def CreatePosnPostList(documents):
    NumDocs = len(documents)
    
    CleanData(documents)
    
    for doc in range(NumDocs): documents[doc].apply(GetPosnPostList, docID=doc, axis=1)
    pd.DataFrame([(i,j) for i,j in PosnPostingList.items()], columns=["Token", "PositionPostingList"])
    
    # Creating the Position Posting list
    a_file = open("./PosnPostList/Posn.pkl", "wb")
    pickle.dump(PosnPostingList, a_file)
    a_file.close()

    # Creating the permuterm index
    a_file = open("./PosnPostList/Perm.pkl", "wb")
    for token in PosnPostingList.keys():
        Permutize(PermIndex, token)
    pickle.dump(PermIndex, a_file)
    a_file.close()

    return PosnPostingList