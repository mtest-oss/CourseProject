import requests_html
import math
import sys
import time
import pandas as pd
import os
import numpy as np
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'
import gensim
from gensim.parsing.preprocessing import remove_stopwords
from bottle import Bottle, static_file, request, run, template
from rank_bm25 import BM25Okapi

ses = requests_html.HTMLSession()


index = 0
# Dataframe 
finalDf = pd.DataFrame(columns=['Index','Time','Strvalue', 'CleanStrvalue', 'relevance'])

# Parse the Corpus and create data frame with appropriate values. 
# Remove stop words to make a cleaned text, convert the words to lower for better search results.
with open('./corpus.txt', 'r') as f:
    dfindex = 0
    for line in f:
        line = line.strip()
        key, _, value = line.partition(' ')
        newkey, _, newvalue = value.partition(' ')
        
        cleanvalue = remove_stopwords(newvalue)
        cleanvalue = cleanvalue.lower()
        finalDf = finalDf.append({'Index' : key, 'Time' : newkey, 'Strvalue' : newvalue, 'CleanStrvalue' : cleanvalue, 'relevance' : 0.0},ignore_index = True)
        dfindex = dfindex + 1
    f.close()

# BM25OKapi for the Corpus with stop words removed.
tokenized_corpus = [doc.split(" ") for doc in (finalDf.CleanStrvalue)]
bm25 = BM25Okapi(tokenized_corpus)


# Calculate ranks/scores for the query term
def calculatescores(search_term):
    query = search_term.lower()
    query = remove_stopwords(query)
    tokenized_query = query.split(" ")
    results = bm25.get_scores(tokenized_query)
    return results

# Get the search results
def getsearchresults(results):
    out_results = []
    rel = finalDf['relevance']
    #print("bef results", rel)
    exres = results.copy()
    #print("bef results", results)
    exres[exres>0] = 1.0
    #print("exres, type", type(exres), exres)
    #print("results", results)
    #print("exres & (rel.to_numpy(dtype=float))")
    rel = rel.to_numpy(dtype=float)
    #print("rel type ", type(rel), rel)
    rel = np.logical_and(exres, rel)
    #print("rel type ", type(rel), rel)
    #results = results + rel
    indices = np.argsort(results)[::-1]
    searchindex = np.nonzero(results) 
    newsearchindex = np.asarray(searchindex)
    #if (len(indices) < 5):
    #    resultlength = len(indices)
    
    resultlength = len(newsearchindex[0])
    #resultlength = 1

    for i in range(resultlength):
        title = finalDf.Strvalue[indices[i]]
        seektime = int(finalDf.Time[indices[i]])
        data = finalDf.Index[indices[i]]
        ind = i
        url = "http://localhost:8787/videos/" + str(finalDf.Index[indices[i]]) + ".mp4" 
        out_results.append({'title': title, 'summary': seektime, 'data': data, 'url': url, 'titleindex': ind})
    return out_results

def search(search_term, language = 'en'):
    results = calculatescores(search_term)
    out_results = getsearchresults(results)
    return out_results

# Bottle Interface and Route paths        
app = Bottle()

@app.route('/')
def index():
    return open('website/index.html').read()

@app.route('/search')
def index():
    query = request.query['query']
    return template(open('website/search.html').read(), results=search(query))

@app.route('/images/<filename>')
def server_static(filename):
    return static_file(filename, root='website/images')

@app.route('/videos/<filename>')
def server_static(filename):
    print('Video Served', filename)
    svalue = (request.query.svalue).strip()
    vvalue = (request.query.vvalue).strip()
    vview = (request.query.view).strip()

    if (vview):
        view = int(vview)
    else:
        view = 0
        
    if (view == 1):
        ent = finalDf.index[(finalDf['Time']==svalue) & (finalDf['Index']==vvalue)].tolist()
        finalDf['relevance'].iloc[ent] = finalDf['relevance'].iloc[ent] + 1.0
        print ("ent", ent)

    return static_file(filename, root='Data/Videos/')

run(app, host='localhost', port=8787, reloader=True)