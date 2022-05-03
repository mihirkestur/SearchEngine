import streamlit as st
import ProcessData
from WildCard import WildCard
from BooleanQuery import performQuery
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

a_file = open("./PosnPostList/Posn.pkl", "rb")
PostList = pickle.load(a_file)
a_file.close()

a_file = open("./PosnPostList/Perm.pkl", "rb")
PermList = pickle.load(a_file)
a_file.close()

def clean(row):
    a = []
    for i in row:
        a.append(int(i))
    a = str(a)
    
    return a

if(Search):
    start = time.process_time()
    if("AND" in Query or "OR" in Query):
        try:
            results = pd.DataFrame(performQuery(Query, PostList), columns=["DocID"])
            # results["Position"] = results["Position"].apply(clean)
            st.write(f"Results queried in {time.process_time() - start} s")
            st.write(results)
        except Exception as e:
            st.error("Query term not present!")
            print(e)
    elif("*" in Query):
        # see if query term is there, else raise error
        try:
            results = pd.DataFrame(WildCard(Query, PermList, PostList), columns=["DocID", "Position"])
            results["Position"] = results["Position"].apply(clean)
            st.write(f"Results queried in {time.process_time() - start} s")
            st.write(results)
        except Exception:
            st.error("Query term not present!")
    else:
        # see if query term is there, else raise error
        try:
            # print(PostList[Query])
            results = pd.DataFrame(PostList[Query], columns=["DocID", "Position"])
            results["Position"] = results["Position"].apply(clean)
            st.write(f"Results queried in {time.process_time() - start} s")
            st.write(results)
        except Exception as e:
            st.error("Query term not present!")

if(Build):
    documents = [pd.DataFrame(fetch_20newsgroups(subset='train', categories=[doc]).data, columns=["text"]) for doc in list(fetch_20newsgroups(subset='train').target_names)]
    ProcessData.CreatePosnPostList(documents)
    st.success("Posting list successfully built")
    