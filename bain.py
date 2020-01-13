import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

#wordcloud
import json
import jieba
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def comments():
    st.write('Customer feedback')
def barchart(index):
    x = brands
    neg=[]
    pos = []
    neu = []
    for brand in brands:
        neg.append(content[index][brand]['num_of_sample']['NEG'])
        neu.append(content[index][brand]['num_of_sample']['NEU'])
        pos.append(content[index][brand]['num_of_sample']['POS'])
        
    fig = go.Figure(go.Bar(x=x, y=pos, name='Positive',marker_color = '#57A773' ))
    fig.add_trace(go.Bar(x=x, y=neu, name='Neutural',marker_color = '#FABC3C'))
    fig.add_trace(go.Bar(x = x,y = neg,name = 'Negative',marker_color = '#EE6352'))
    fig.update_layout(barmode = 'stack')
    st.plotly_chart(fig)
    

def donut(brand,index):
    list = content[index][brand]['num_of_sample']
    values = [list['POS'],list['NEU'],list['NEG']]
    colors = ['#57A773','FABC3C','#EE6352']
    labels = ['Positive','Netural','Negative']
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.8)])
    fig.update_traces(hoverinfo='label+value', textinfo='percent', textfont_size=20,
                  marker=dict(colors=colors))
    st.plotly_chart(fig)
    
def criteria():
    st.subheader('Key Purchase Criteria')
    

    fig = go.Figure(go.Bar(
            x=score,
            y=seed_question,
            marker_color = '#918EF4',
            orientation='h'))
    st.plotly_chart(fig)
    
    #Word Cloud
    st.subheader('Keyword Cloud')

    #wordcloud content
    file_content = open("sampletext.txt","r")
    mytext = file_content.read()
    #keywordcloud(mytext)

#random color for the word cloud
def hsl_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(242, 86%%, %d%%)" % random.randint(74, 95)

#generate keywordcloud
def keywordcloud(mytext):
    cut_text =" ".join(jieba.cut(mytext))
    wordcloud = WordCloud(margin=20,font_path="ziti.otf", \
                      background_color='white',color_func=hsl_color_func).generate(cut_text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot()    
 
def byfilter(index):
    #Customer's feedback
    st.subheader('Customer\'s Feedback')
    barchart(index)
    brand = st.selectbox('Please select the brand',brands)
    #display selected donut chart
    donut(brand,index)
    comments()
    
    
    
     
st.title('Sushi Restaurant Report')

#purchase criteria
content = sorted(json.load(open('bain_1.json')), key = lambda i: i['score'])
brands = list(content[0].keys())[1:-1]
score= []
seed_question = []
for i in content[:5]:
    score.append(i['score'])
    seed_question.append(i['query'])

#sidebar
# st.sidebar.subheader('Filter results by brand')
# select_brand = {}
# for brand in brands:
#     select_brand[brand]= st.sidebar.checkbox(brand)

st.sidebar.subheader('Filter')
filter = st.sidebar.radio('',('Overall Key Cirteria','By Key Cirteria'))
if filter == 'Overall Key Cirteria':
    criteria()
else:
    key = st.sidebar.selectbox('Please select a seed_question',
    seed_question)
    byfilter(seed_question.index(key))



    



# cut_text =" ".join(jieba.cut(mytext))
# #generate word cloud
# wordcloud = WordCloud(margin=20,font_path="ziti.otf", \
#                       background_color='white',color_func=hsl_color_func).generate(cut_text)
# 
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.show()
# st.pyplot()


