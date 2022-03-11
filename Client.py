import streamlit as st
import ProcessData
from sklearn.datasets import fetch_20newsgroups
import pandas as pd
import json
import pickle
import time

st.set_page_config("Search Engine")
st.title("Search Engine")
    
Corpus = st.text_input('Enter corpus path')
Build = st.button("Build the posting list")
Query = st.text_input('Enter the search query')
Search = st.button("Search")

def WildCard(query):
    ans_token = []
    first, second = query.split("*")
    check = second[::-1] + "$" + first
    for token in PermList.keys():
        # See if token is matching with first and second
        if(token.startswith(check)):
            ans_token.append(PermList[token])
            
    return [PostList[i][0] for i in ans_token]

a_file = open("./PosnPostList/Posn.pkl", "rb")
PostList = pickle.load(a_file)
a_file.close()

a_file = open("./PosnPostList/Perm.pkl", "rb")
PermList = pickle.load(a_file)
a_file.close()

if(Search):
    start = time.process_time()
    if("AND" in Query or "OR" in Query):
        try:
            #results = pd.DataFrame(, columns=["DocID", "Position"])
            #st.write(f"Results queried in {time.process_time() - start} s")
            #st.write(results)
            pass
        except Exception:
            st.error("Query term not present!")
    elif("*" in Query):
        # see if query term is there, else raise error
        try:
            results = pd.DataFrame(WildCard(Query), columns=["DocID", "Position"])
            st.write(f"Results queried in {time.process_time() - start} s")
            st.write(results)
        except Exception:
            st.error("Query term not present!")
    else:
        # see if query term is there, else raise error
        try:
            results = pd.DataFrame(PostList[Query], columns=["DocID", "Position"])
            st.write(f"Results queried in {time.process_time() - start} s")
            st.write(results)
        except Exception:
            st.error("Query term not present!")

if(Build):
    documents = [pd.DataFrame(fetch_20newsgroups(subset='train', categories=[doc]).data, columns=["text"]) for doc in 
        list(fetch_20newsgroups(subset='train').target_names)]
    print(ProcessData.CreatePosnPostList(documents[:2]))