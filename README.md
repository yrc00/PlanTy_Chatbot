# 🌱 PlanTy_Chatbot

PlanTy Agent 서버를 열어 챗봇을 테스트하는 페이지입니다.
[PlanTy Agent 레포지토리](https://github.com/Team-BIoTy/Planty_Agent)에서 main.py를 실행하여 서버를 올린 뒤, streamlit을 활용하여 챗봇을 테스트할 수 있는 페이지를 올릴 수 있습니다. 

## 📦 다운로드 및 설치
---
### 1. 레포지토리 클론
```
git clone https://github.com/Team-BIoTy/PlanTy_Chatbot.git
cd PlanTy_Catbot
```

### 2. .streamlit 폴더 추가
```
GROQ_API_KEY_NO1 = ""
Chat_URL = "http://localhost:8000/chat_direct"
QA_URL = "http://localhost:8000/plant_qa"
```
- `.streamlit/secrets.toml`를 추가하여 사용할 groq api key 들과 url을 등록합니다. 
- 로컬에서 사용할 경우 경로를 `localhost:8000`으로 지정하고,
- 외부 서버를 사용할 경우 서버 주소를 변경해야합니다. 

### 3. streamlit 실행
```
streamlit run app.py
```
- `streamlit run`을 사용하여 대시 보드를 실행할 수 있습니다. 