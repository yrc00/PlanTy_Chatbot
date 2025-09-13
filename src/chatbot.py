import requests
import streamlit as st
import time
import datetime
import csv

# ======================== 사이드바 ========================

def sidebar():
    with st.sidebar:
        # 챗봇 선택
        api_choice = st.selectbox(
            "챗봇 선택",
            options=["Chatroom 1", "Chatroom 2", "Chatroom 3", "Chatroom 4"],
            help="사용할 챗봇을 선택하세요.",
        )
        if api_choice == "Chatroom 1":
            st.session_state.api = st.secrets['GROQ_API_KEY_NO1']
        elif api_choice == "Chatroom 2":
            st.session_state.api = st.secrets['GROQ_API_KEY_NO2']
        elif api_choice == "Chatroom 3":
            st.session_state.api = st.secrets['GROQ_API_KEY_NO3']
        elif api_choice == "Chatroom 4":
            st.session_state.api = st.secrets['GROQ_API_KEY_NO4']
        else:
            st.error("잘못된 선택입니다.")
            return
        st.session_state.api_choice = api_choice

        col1, col2 = st.columns(2)
        with col1:
            chatbot_model = st.radio("챗봇 모델", options=["SLM", "LLM"])
            st.session_state.chatbot_model = chatbot_model
        with col2:
            chatbot_mode = st.radio("챗봇 모드", options=["성격", "질의응답"])
            st.session_state.chatbot_mode = chatbot_mode

        # 식물 정보
        st.divider()
        st.subheader("🌱 식물 정보 설정")
        plant_type = st.selectbox(
            "식물 종류",
            options=["몬스테라","가울테리아","개운죽","러브체인","숙근이베리스","시서스",
                     "스킨답서스","아이비","히포에스테스","호야"],
        )
        st.session_state.plant_type = plant_type

        col3, col4 = st.columns(2)
        with col3:
            st.session_state.plant_name = st.text_input("식물 이름", value="테리")
            st.session_state.plant_env = st.selectbox("식물 환경", options=["적절", "건조", "습함", "추움", "더움"])
            # 대화 기록 삭제
            if st.button("대화 기록 삭제", type="secondary"):
                st.session_state.messages = []
                st.rerun()
        with col4:
            st.session_state.plant_age = st.number_input("식물 나이", min_value=0, value=1, step=1)
            st.session_state.plant_personality = st.selectbox(
                "식물 성격", options=["기쁨이", "슬픔이", "까칠이", "버럭이", "소심이"]
            )
            # 📌 사이드바에 "사용법 다시 보기" 버튼 추가
            if st.button("사용법 보기", type="secondary"):
                st.session_state.show_guide = True
                st.rerun()

        st.divider()
        st.subheader("📝 설문")
        st.link_button("설문 참여하기", url="https://forms.gle/57TiK928X3CnsR5W6")

# ======================== 챗봇 ========================

def load_env_info_from_csv(plant_name, csv_file="./data/plant_env_standards_filtered.csv"):
    """
    plant_env_standards_filtered.csv에서 plant_name(=common_name)에 해당하는 환경 정보 로드
    """
    with open(csv_file, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["common_name"] == plant_name:
                return {
                    "max_humidity": float(row.get("max_humidity", 80)),
                    "max_light": float(row.get("max_light", 15000)),
                    "max_temperature": float(row.get("max_temperature", 30)),
                    "min_humidity": float(row.get("min_humidity", 40)),
                    "min_light": float(row.get("min_light", 5000)),
                    "min_temperature": float(row.get("min_temperature", 15)),
                }

    # 찾지 못하면 기본값 반환
    return {
        "max_humidity": 80,
        "max_light": 15000,
        "max_temperature": 30,
        "min_humidity": 40,
        "min_light": 5000,
        "min_temperature": 15,
    }

def run_persona(type, user_input: str) -> str:
    """
    페르소나 챗봇 실행
    """

    # 환경 정보 로드
    env_info = load_env_info_from_csv(st.session_state.plant_type)

    # 기본값 = "적절"
    env_type = st.session_state.plant_env
    temperature = (env_info["min_temperature"] + env_info["max_temperature"]) // 2
    humidity = (env_info["min_humidity"] + env_info["max_humidity"]) // 2
    light = (env_info["min_light"] + env_info["max_light"]) // 2

    if env_type == "건조":
        humidity = env_info["min_humidity"] - 5
    elif env_type == "습함":
        humidity = env_info["max_humidity"] + 5
    elif env_type == "추움":
        temperature = env_info["min_temperature"] - 2
    elif env_type == "더움":
        temperature = env_info["max_temperature"] + 2
    # "적절"이면 그대로 사용

    cur_info = {
        "temperature": temperature,
        "humidity": humidity,
        "light": light,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    chat_log = "\n".join([m["content"] for m in st.session_state.messages if m["role"] == "user"])

    personality_map = {
        "기쁨이": "joy",
        "슬픔이": "sadness",
        "까칠이": "disgust",
        "버럭이": "anger",
        "소심이": "fear"
    }

    personality = personality_map.get(st.session_state.plant_personality, "joy")

    url = st.secrets["Chat_URL"]
    payload = {
        "type": st.session_state.chatbot_model.lower(), 
        "nickname": st.session_state.plant_name,       
        "env_info_dict": env_info,                      
        "cur_info_dict": cur_info,                     
        "chat_log": chat_log,
        "persona": personality,
        "user_input": user_input,
        "api_key": st.session_state.api,
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        result = response.json().get("final_response", "챗봇 응답에 실패했습니다.")
    else:
        result = "챗봇 응답에 실패했습니다."    

    return result

def run_qa(type, user_input: str) -> str:
    """
    질의응답 챗봇 실행
    """
    url = st.secrets["QA_URL"]
    payload = {
        "type": st.session_state.chatbot_model.lower(),
        "user_input": user_input,
        "api_key": st.session_state.api,
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        result = response.json().get("final_response", "챗봇 응답에 실패했습니다.")
    else:
        result = "챗봇 응답에 실패했습니다."

    return result

def get_chatbot_response(user_input: str) -> str:
    if st.session_state.chatbot_mode == "성격":
        result = run_persona(st.session_state.chatbot_model, user_input)
    else:
        result = run_qa(st.session_state.chatbot_model, user_input)
    
    return result

def chatbot():
    # 세션 상태 초기화 (처음 페이지 로드 시)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "show_guide" not in st.session_state:
        st.session_state.show_guide = True

    # === 사용법 안내 ===
    if st.session_state.show_guide:
        st.info(
            """
            PlanTy는 IoT 데이터를 기반으로 식물과 대화할 수 있는 챗봇 서비스입니다.

            본 페이지는 PlanTy의 챗봇을 테스트할 수 있는 공간입니다. 

            **사용법**
            1. 왼쪽 사이드바에서 챗봇 모델, 식물 정보 등을 설정하세요.
                - **SLM**: 소규모 언어 모델 (Small Language Model) -> 응답 속도 느림
                - **LLM**: 대규모 언어 모델 (Large Language Model) -> 응답 속도 빠름
                - **성격**: 식물 정보 설정에서 지정된 식물의 환경과 성격을 반영하여 답변
                - **질의응답**: 식물과 관련된 질문에 답변
                - 식물의 종류, 이름, 나이, 성격, 환경을 자유롭게 설정해보세요
            2. 아래 입력창에 메시지를 입력하면 식물과 대화할 수 있어요.
            3. 필요하면 사이드바에서 "대화 기록 삭제" 또는 "사용법 보기" 버튼을 눌러 초기화할 수 있어요.

            **중요!**
            - 사용중 오류가 발생했다면 챗봇을 Chatroom 1, 2, 3, 4로 변경해보세요.
            - 새로고침을 하면 대화 기록이 초기화됩니다
            - 사용을 완료했다면 사이드바 하단의 설문 참여하기를 눌러 **설문조사**를 완료해주세요!
            """
        )

    chat_container = st.container()

    # 기존 메시지 표시
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # 사용자 입력
    user_input = st.chat_input("메시지를 입력하세요...")

    if user_input:
        # 사용법 숨기기
        st.session_state.show_guide = False

        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": user_input})
        with chat_container:
            with st.chat_message("user"):
                st.write(user_input)

        with st.spinner("생각 중..."):
            bot_response = get_chatbot_response(user_input)

        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with chat_container:
            with st.chat_message("assistant"):
                st.write(bot_response)

        st.rerun()
