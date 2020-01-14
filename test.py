import json
file = json.load(open('bain_final.json'))

queries = next(item for item in file if item["query"] == "品牌知名度怎么样")
queries = queries['agg_results']['target_clusters']
#queries = queries['examples']
feedback = ""
for query in queries:
    feedback+="\""+query['examples'][0]+"\"<br>"

print(feedback)    