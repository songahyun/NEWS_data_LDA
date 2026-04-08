# NEWS_data_LDA: 뉴스 데이터(1000개)를 사용한 LDA 토픽 모델링 
(https://news-data-lda.onrender.com/docs)

---
### 프로젝트 배경: 뉴스 기사 데이터는 정치, 경제, 사회 등 다양한 주제를 포함하고 있으며, 이를 효과적으로 분류하고 핵심 내용을 파악하는 것은
정보 탐색과 분석에 있어 중요한 요소이다. 그러나 대량의 텍스트 데이터를 사람이 직접 분류하는 것은 시간과 비용이 많이 소요되기 때문에, 자동화된 토픽 
분석 기법의 필요성이 증가하고 있다.  
  
따라서 본 프로젝트에서는 뉴스 텍스트 데이터를 기반으로 토픽 모델링을 수행하고, 이를 API 형태로 제공하여 누구나 쉽게 텍스트의 주제를 분석할 수 있도록
하는 시스템을 구축하고자 한다.                      

### 프로젝트 목표: 
- 뉴스 텍스트 데이터 기반 토픽 모델링 수행
- LDA를 활용한 문서 주제 추룰 및 대표 키워드 도출
- 텍스트 입력 시 자동으로 토픽을 분석하는 API구축
- 모델을 웹 서비스로 배포하여 접근성 향상
- 데이터 분석 결과를 실시간으로 활용 가능한 구조 구현

### 사용 데이터:
2026년 3월 26일 네이버 뉴스 경제 섹션 데이터 1000개를 크롤링해서 사용 → news_dataset_economy.csv

### 사용 기술 및 모델
- Python
- - FastAPI (REST API 서버 구축)
- LDA (Latent Dirichlet Allocation)
- Docker (컨테이너 기반 배포)
- Render (클라우드 배포)
- joblib (모델 저장 및 로드)

### 배포 정보
실제 서비스 URL: `https://news-data-lda.onrender.com/docs`
- Swagger UI를 통해 API 테스트 가능
- 별도 환경 구축 없이 웹에서 바로 사용 가능
- 요청 형식:
{
    "text": "삼성전자 주가가 상승했다."
}

※ 참고사항:
- 무료 배포 환경 특성상 일정 시간 미사용 시 서버가 sleep 상태로 전환될 수 있음.
- 첫 요청 시 응답이 다소 지연될 수 있음.
---

### 파일 설명
[일반 파일]
01_crawl.ipynb: 네이버 뉴스 데이터를 크롤링하는 파일
02_preprocess.ipynb: 수집한 뉴스 데이터의 전처리를 수행하는 파일
03_analyze.ipynb: LDA를 활용한 토픽 모델링 수행 코드 파일
04_visualize.ipynb: 토픽 모델링 결과를 시각화하는 파일
05_API_prepare.ipynb: 모델을 API 형태로 활용하기 위해 전처리 및 추론 로직을 정리한 코드

[데이터]
news_dataset_economy.csv: 네이버 뉴스에서 크롤링한 원본 데이터(전처리 전 기사 1000개)
news_preprocessed_economy.csv: 전처리 과정을 거친 뉴스 데이터(전처리 후 기사 978개)

[Docker 관련 파일]
Dockerfile: 애플리케이션 실행 환경을 정의하고 컨테이너 이미지를 생성하기 위한 설정
.dockerignore: Docker 이미지 빌드 시 제외할 파일을 정의하는 설정 파일

[모델 저장]
lda_model.pkl: 학습된 LDA 토픽 모델
dictionary.pkl: LDA 모델에서 사용하는 단어 사전(Dictionary)
reqirements.txt: 프로젝트 실행에 필요한 Python 라이브러리 목록

main.py: FastAPI를 기반으로 토픽 모델링 결과를 제공하는 REST API 서버 코
