headers = {
    "Content-Type": "application/json",
    "Authorization": "585c5ce2-ca33-4e00-a71a-abad3b232b11"
}
import streamlit as st
import requests
import pprint

result = requests.post(
    "https://api.soco.ai/v1/search/aggregate",
    headers=headers,
    json={
        "query": "需要排位置么",
        "uid": "Tony",
        "n_best": 100,
        "query_args": {
            "use_embed": True,
            "keep_vectors": True,
            #"filters": [{"term": {"meta.brand.keyword": "万岁"}}]
        },
        "agg_args": {
            "target_answers": ['不需要','还是要排一会'],
            "target_meta": [],
            "keywords": False
        }
    }
).json()

st.write(result)
