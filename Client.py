import streamlit as st

st.set_page_config("Search Engine")
st.title("Search Engine")
    
Query = st.text_input('')
Search = st.button("Search")

def ExecuteQuery():
    print(Query)

if(Search):
    ExecuteQuery()