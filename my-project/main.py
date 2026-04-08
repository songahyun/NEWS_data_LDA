from fastapi import FastAPI
import joblib
import re
from kiwipiepy import Kiwi
from pydantic import BaseModel

class Item(BaseModel):
    text: str

# FastAPI 앱 생성
app = FastAPI()

# 모델 로드
lda_model = joblib.load("lda_model.pkl")
dictionary = joblib.load("dictionary.pkl")

# Kiwi
kiwi = Kiwi()
TARGET_POS = ["NNG", "NNP", "VV", "VA"]

STOPWORDS = set([
    '기자','사진','뉴스','연합뉴스','뉴시스','보도','관련','이번','대한','통해','하다','이다',
    '지난','현재','이날','오전','오후','당시','이후','앞서','최근','정부','관계자','업계','측','대통령','국회','위원회',
    '등','것','수','때','위해','경우','때문','대해','지난해','올해','내년','년','월','일','억','만','천',
    '파이낸셜뉴스','KBS','한국경제','매일경제','이데일리','SBS Biz','부산일보','서울경제','머니투데이','세계일보','국제신문',
    '가능','상황','수준','계획','내용','포함','실제','방안','검토','일각','입장','통해',
    '발표','조사','응답','보고','설명','강조','언급','진단','요청','건의',
    '전체','가운데','이전','이후','처음','주요','전반','핵심','본격','적극','철저','효과','역할','문제','요소','체계','기반','구성','구축','확보','강화','지원',
    '작년','새해','연내','시기','기간','차례','대상','이용','통하','위하','대하','나타나','밝히','따르','보이','점치','내다보','늘리','줄이','높이','갖추','만들'
])

def clean_text(text: str):
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub(r'http\S+|www\S+', ' ', text)
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'[^가-힣\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def tokenize(text: str):
    tokens = []
    result = kiwi.analyze(text)[0][0]
    for token, pos, _, _ in result:
        if pos in TARGET_POS:
            tokens.append(token)
    return tokens

def postprocess(tokens):
    return [
        t for t in tokens
        if t not in STOPWORDS and len(t) > 1 and not t.isdigit()
    ]

def preprocess(text: str):
    text = clean_text(text)
    tokens = tokenize(text)
    tokens = postprocess(tokens)
    return tokens

def get_topic_keywords():
    topic_keywords = {}
    for i in range(lda_model.num_topics):
        words = lda_model.show_topic(i, topn=5)
        topic_keywords[i] = [w[0] for w in words]
    return topic_keywords

def predict(text: str):
    tokens = preprocess(text)

    if not tokens:
        return {"error": "유효한 단어가 없습니다."}

    bow = dictionary.doc2bow(tokens)
    topics = lda_model.get_document_topics(bow)
    topics = [(int(t[0]), float(t[1])) for t in topics]

    dominant_topic = max(topics, key=lambda x: x[1])[0]

    topic_keywords = get_topic_keywords()

    return {
        "topics": topics,
        "dominant_topic": dominant_topic,
        "keywords": topic_keywords[dominant_topic]
    }

# API 엔드포인트(기존)
# @app.post("/predict")
# def predict_api(text: str):
#     return predict(text)

# API 엔드포인트
@app.post("/predict")
def predict_api(item: Item):  # text: str 대신 item: Item으로 변경
    return predict(item.text) # item 내의 text 필드 접근
