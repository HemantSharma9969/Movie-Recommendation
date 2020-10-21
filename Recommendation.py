import streamlit as st
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as soup
import requests
from tmdbv3api import TMDb
import json
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from PIL import Image
from tmdbv3api import Movie
from fuzzywuzzy import fuzz
import pickle


tmdb_movie=Movie()
tmdb = TMDb()
tmdb.api_key = '281825c11d7e66ad7a6a8fb94fa92276'


STOP_WORDS= stopwords.words('english')



df = pd.read_csv("main_data.csv")
cv = CountVectorizer(stop_words=STOP_WORDS)
count_matrix = cv.fit_transform(df['comb'])
similarity = cosine_similarity(count_matrix)

#pickle_in = open("C:\\Users\\Hemant\\Desktop\\Projects\\Recomeend\\AJAX-Movie-Recommendation-System-with-Sentiment-Analysis-master\\similarity.pkl","rb")
#similarity= pickle.load(pickle_in)


movie=df["movie_title"].to_list()









def result():
    placeholder.empty()
    image_address = []
    over_view=[]
    name =[]

   
    i = df[df["movie_title"]==m].index[0]
    lst = list(enumerate(similarity[i]))
    lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
    lst = lst[1:6] # excluding first item since it is the requested movie itself
    l=[]
    for i in range(len(lst)):
        a = lst[i][0]
        l.append(df['movie_title'][a])



    result = tmdb_movie.search(str(m))
    movie_id = result[0].id
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
    data_json = response.json()    
    st.title(str(m).capitalize())
    st.image("https://image.tmdb.org/t/p/original/"+data_json['poster_path'],width=300)
    st.write('**Overview : **.',str(data_json['overview']))


    st.title("Cast")
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&append_to_response=credits'.format(movie_id,tmdb.api_key))
    data_json = response.json()
    images=[]
    names=[]
    for i in range(0,6):     
        r =data_json["credits"]["cast"][i]
        image = "https://image.tmdb.org/t/p/w600_and_h900_bestv2{}".format(r['profile_path'])
        images.append(image)
        names.append(r['name'])
        
    st.image(images,width =200,caption=names)
    

    
    
    for i in l:
        try:
        
            result = tmdb_movie.search(str(i))
            movie_id = result[0].id
            response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
            data_json = response.json()
            name.append(str(i))
            image_address.append("https://image.tmdb.org/t/p/original/"+data_json['poster_path'])
            over_view.append(data_json['overview'])      

        except:
            pass


    html2 ="""
    <div style="background-color:black;padding:10px">
    <h2 style="color:white;text-align:center;">Top 5 Recommendation </h2>
    </div>"""
    st.markdown(html2,unsafe_allow_html=True)
    
    for h in range(0,5):

        st.title(name[h].capitalize())
        st.image(image_address[h],width=200)
        st.write('**Overview : **.',str(over_view[h]))
    
    

page_bg_img = '''
<style>
body {
background-image: url("https://hookagency.com/wp-content/uploads/2015/11/light-blue-gradient-ui-gradient.jpg");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("Movie Recommendation System")


m = st.text_input("Enter the Movie Name ","")


m = str(m).lower()


if m:    

    
    names=[]
    q=dict()
    for i in movie:
        fuzz1=fuzz.token_set_ratio(m, i)
        q.update({i:fuzz1})

    s = dict(sorted(q.items(), key=lambda x: x[1],reverse=True)[0:5])

    s = list(s.keys())

    placeholder = st.empty()
    placeholder.write("Just to make sure there isn't any Spelling Mistake. Please select your movie name from side bar")





    
    b1 = st.sidebar.button(s[0].capitalize(), key="1")
    b2 = st.sidebar.button(s[1].capitalize(), key="2")
    b3 = st.sidebar.button(s[2].capitalize(), key="3")
    b4 = st.sidebar.button(s[3].capitalize(), key="4")
    b5 = st.sidebar.button(s[4].capitalize(), key="5")

    

    if b1:
        m=str(s[0]).lower()
        result()

    elif b2:
        m=str(s[1]).lower()
        result()

    elif b3:
        m=str(s[2]).lower()
        result()

    elif b4:
        m=str(s[3]).lower()
        result()

    elif b5:
        m=str(s[4]).lower()
        result()





    


