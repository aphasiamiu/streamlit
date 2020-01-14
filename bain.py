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
HTML_WRAPPER = """<div id = "comment" style="overflow-x: auto; background-color: #F7F7FF;
border-radius: 0.5rem; padding: 1.5rem;line-height: 2; margin-bottom: 2rem">{}</div>"""

def comments(seed_question):
     queries = next(item for item in file if item["query"] == seed_question)
     #queries = queries['agg_results']['target_clusters'][0]['examples']
     queries = queries['agg_results']['target_clusters']
     keywords = []
     
     for query in queries:
         keywords.append(query['name'])
         
     keyword = st.selectbox('Please select the keyword',keywords)
     comment_by_keyword(keyword, queries)
def comment_by_keyword(keyword,queries):
    #keyword = ['1','2','3']
    queries = next(item for item in queries if item["name"] == keyword)
    feedback = ""
    for query in queries['examples']:
        feedback+="<b>\""+query+"\"</b><br>"
    st.write(HTML_WRAPPER.format(feedback), unsafe_allow_html=True)
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
    fig.update_layout(barmode = 'stack',xaxis={'categoryorder':'total descending'})
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
    
#     #Word Cloud
#     st.subheader('Keyword Cloud')
# 
#     #wordcloud content
#     file_content = open("sampletext.txt","r")
#     mytext = file_content.read()
#     #keywordcloud(mytext)

#random color for the word cloud
def hsl_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(242, 86%%, %d%%)" % random.randint(74, 86)

#generate keywordcloud
def keywordcloud(mytext):
    cut_text =" ".join(jieba.cut(mytext))
    wordcloud = WordCloud(margin=4,font_path="ziti.otf", \
                      background_color='white',color_func=hsl_color_func).generate(cut_text)
    plt.imshow(wordcloud, interpolation='bilinear')
    
    plt.axis("off")
    plt.show()
    st.pyplot()    
 
def byfilter(index):
    #Customer's feedback
    barchart(index)
    #brand = st.selectbox('Please select the brand',brands)
        #display selected donut chart
    #donut(brand,index)
    comments(seed_question[index])
    
    
    
    
    
     
st.title('Sushi Restaurant Report')

#purchase criteria
file = json.load(open('bain_final.json'))
content = sorted(file, key = lambda i: i['score'])
#brands = list(content[0].keys())[1:-1]
brands = ['万岁' ,'大禾', '禾绿', '池田', '摩打食堂', '新一番', '元气', '争鲜', '丸米', '滨寿司', '伊秀寿司']
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

# st.sidebar.subheader('Filter')
# filter = st.sidebar.radio('',('Overall Key Criteria','By Key Criteria'))
# if filter == 'Overall Key Criteria':
#     criteria()
# else:
#     key = st.sidebar.selectbox('Please select a seed_question',
#     seed_question)
#     byfilter(seed_question.index(key))

criteria()
st.subheader('Customer\'s Feedback')
key = st.selectbox('Please select a seed_question',seed_question)
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


