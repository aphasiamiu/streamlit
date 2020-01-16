import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# wordcloud
import json
import jieba
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# for html style
HTML_WRAPPER = """<div id = "comment" style="overflow-x: auto; background-color: #F7F7FF;
border-radius: 0.5rem; padding: 1.5rem;line-height: 2; margin-bottom: 2rem">{}</div>"""
TEXT_WRAPPER = """<font color={}>{}</font> """
text_color = ['#C33C54', '#254E70', '#F26419', '#F6AE2D',
              '#86BBD8', '#2F4858', '#B84A62', '#A997DF', '#F7996E', '#4C9F70']

HTML_SOURCE = """<div style = "font-size: 12px; color: #979797; margin-bottom: 2rem; margin-left: 5rem">{}</div> """


# original embedded function
def embeded(seed_question):
    queries = next(item for item in file if item["query"] == seed_question)
    queries = queries['agg_results']['embed_clusters']
    embed_list = []
    final_result = ""
    for query in queries:
        embed_list.append(query['examples'])
    for i in embed_list:
        color = text_color[embed_list.index(i)]
        feedback = ""
        for query in i:
            feedback += "<b>\"" + query + "\"</b><br>"
        # st.write(TEXT_WRAPPER.format(color,feedback), unsafe_allow_html=True)
        final_result += TEXT_WRAPPER.format(color, feedback) + "<br>"
    st.write('embed_cluster')
    st.write(HTML_WRAPPER.format(final_result), unsafe_allow_html=True)


# new embedded function for new data structure
def embedded(seed_question):
    embed_brand = st.selectbox('embedded by brand', brands)
    queries = next(item for item in file if item["query"] == seed_question)
    queries = queries['brands'][embed_brand]['embed_clusters']

    embed_list = []
    total_num = []
    final_result = ""
    for query in queries:
        embed_list.append(query['examples'])
        total_num.append(query['size'])

    for i in embed_list:
        color = text_color[embed_list.index(i)]
        feedback = ""
        for query in i:
            feedback += "<b>\"" + query + "\"</b><br>"
        # st.write(TEXT_WRAPPER.format(color,feedback), unsafe_allow_html=True)
        num = str(total_num[embed_list.index(i)])
        percentage = int(num) / sum(total_num)
        percentage = "{0:.2%}".format(percentage)
        final_result += TEXT_WRAPPER.format(color,
                                            " Total Sample: " + num + "&nbsp&nbsp   <b>(" + percentage + ")</b> <br>" + feedback) + "<br>"
    st.write(HTML_WRAPPER.format(final_result), unsafe_allow_html=True)


def comments(seed_question):
    queries = next(item for item in file if item["query"] == seed_question)
    # queries = queries['agg_results']['target_clusters'][0]['examples']
    queries = queries['agg_results']['target_clusters']
    keywords = []

    for query in queries:
        keywords.append(query['name'] + ' (' + str(query['size']) + ')')

    keyword = st.selectbox('target_cluster', keywords)
    comment_by_keyword(keyword, queries)


# show the target_cluster result
def target(query):
    queries = next(item for item in file if item["query"] == query)
    factors = []
    num = []
    examples = queries['brands']['All']['target_clusters']
    for example in examples:
        if example['name'] != "others":
            factors.append(example['name'])
    target_list = {}

    for factor in factors:
        target_list[factor] = []
        for brand in brands:
            cluster = queries['brands'][brand]['target_clusters']
            mysize = next(item for item in cluster if item["name"] == factor)
            target_list[factor].append(mysize['size'])

    # get the percentage
    target_list['total'] = []
    for i in range(len(brands)):
        total = 0
        for factor in factors:
            total += target_list[factor][i]
        target_list['total'].append(total)

        for factor in factors:
            target_list[factor][i] /= target_list['total'][i]
    sum(target_list['total'])

    x = [brands[i] + str(target_list['total'][i]) for i in range(len(brands))]
    fig = go.Figure(go.Bar(x=x, y=target_list[factors[0]], name=factors[0], marker_color='#57A773'))
    for i in factors[1:]:
        fig.add_trace(go.Bar(x=x, y=target_list[i], name=i, marker_color=text_color[factors.index(i)]))
    fig.update_layout(barmode='stack')
    st.plotly_chart(fig)
    source = "Source: Consumer survey(N=" + str(sum(target_list['total'])) + ")     Result shown in percentage"
    st.write(HTML_SOURCE.format(source), unsafe_allow_html=True)


def comment_by_keyword(keyword, queries):
    keyword = keyword.split(' ')[0]
    # keyword = ['1','2','3']
    queries = next(item for item in queries if item["name"] == keyword)
    feedback = ""
    for query in queries['examples']:
        feedback += "<b>\"" + query + "\"</b><br>"
    st.write(HTML_WRAPPER.format(feedback), unsafe_allow_html=True)


def barchart(index):
    neg = []
    pos = []
    neu = []
    total_list = []
    sample_num = 0

    for brand in brands:
        num = content[index]['brands'][brand]['keyword_clusters']['num_of_sample'][brand]
        total = num['NEG'] + num['NEU'] + num['POS']
        neg.append(num['NEG'] / total)
        neu.append(num['NEU'] / total)
        pos.append(num['POS'] / total)
        # neg.append("{0:.2%}".format(num['NEG'] / total))
        # neu.append("{0:.2%}".format(num['NEU'] / total))
        # pos.append("{0:.2%}".format(num['POS'] / total))
        total_list.append(total)
        sample_num += total

    x = [brands[i] + str(total_list[i]) for i in range(len(brands))]
    fig = go.Figure(go.Bar(x=x, y=pos, name='Positive', marker_color='#57A773'))
    fig.add_trace(go.Bar(x=x, y=neu, name='Neutural', marker_color='#FABC3C'))
    fig.add_trace(go.Bar(x=x, y=neg, name='Negative', marker_color='#EE6352'))
    fig.update_layout(barmode='stack')
    st.plotly_chart(fig)
    source = 'Source: Consumer survey(N=' + str(sample_num) + ")     Result shown in percentage"
    st.write(HTML_SOURCE.format(source), unsafe_allow_html=True)


def donut(brand, index):
    list = content[index][brand]['num_of_sample']
    values = [list['POS'], list['NEU'], list['NEG']]
    colors = ['#57A773', 'FABC3C', '#EE6352']
    labels = ['Positive', 'Netural', 'Negative']
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.8)])
    fig.update_traces(hoverinfo='label+value', textinfo='percent', textfont_size=20,
                      marker=dict(colors=colors))
    st.plotly_chart(fig)


def criteria():
    fig = go.Figure(go.Bar(
        x=score,
        y=seed_question,
        marker_color='#918EF4',
        orientation='h'))
    st.plotly_chart(fig,width = 750,height = 250+30*rank)


#     #Word Cloud
#     st.subheader('Keyword Cloud')
# 
#     #wordcloud content
#     file_content = open("sampletext.txt","r")
#     mytext = file_content.read()
#     #keywordcloud(mytext)

# random color for the word cloud
def hsl_color_func(word, font_size, position, orientation, random_state=None,
                   **kwargs):
    return "hsl(242, 86%%, %d%%)" % random.randint(74, 86)


# generate keywordcloud
def keywordcloud(mytext):
    cut_text = " ".join(jieba.cut(mytext))
    wordcloud = WordCloud(margin=4, font_path="ziti.otf", \
                          background_color='white', color_func=hsl_color_func).generate(cut_text)
    plt.imshow(wordcloud, interpolation='bilinear')

    plt.axis("off")
    plt.show()
    st.pyplot()


def byfilter(index):
    # Customer's feedback
    barchart(index)
    target(seed_question[index])
    # comments(seed_question[index])
    embedded(seed_question[index])


st.title('Sushi Restaurant Report')

# purchase criteria
file = json.load(open('bain_final_new.json'))
content = sorted(file, key=lambda i: i['score'])
brands = ['万岁', '大禾', '禾绿', '池田', '摩打食堂', '新一番', '元气', '争鲜', '丸米', '滨寿司', '伊秀寿司']
score = []
seed_question = []

st.subheader('Key Purchase Criteria')
rank = st.number_input('insert a number',min_value = 3,value = 5)
for i in content[-rank:]:
    score.append(i['score'])
    seed_question.append(i['query'])

# sidebar
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
key = st.selectbox('Please select a seed_question', seed_question)
byfilter(seed_question.index(key))
