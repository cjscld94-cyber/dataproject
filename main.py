import streamlit as st
st.title('!!')
# app.py
import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천 🍀", page_icon="🧭", layout="centered")

st.title("MBTI로 골라보는 진로 꿀팁 ✨")
st.write("안녕! 아래에서 너의 MBTI를 골라봐. 그 유형에 잘 맞는 **진로 2가지**랑, 어떤 전공이 어울리는지, 어떤 성격이 잘 맞는지도 알려줄게 😄")

mbti_list = [
    "ISTJ","ISFJ","INFJ","INTJ",
    "ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP",
    "ESTJ","ESFJ","ENFJ","ENTJ"
]

# 데이터: 각 MBTI별 추천 진로(2개), 전공, 성격 설명
# 간결하고 청소년 친화적 표현 사용
recommendations = {
    "ISTJ": [
        {"career":"회계사 / 세무사 📊",
         "majors":"경영학(회계), 세무학, 경제학",
         "personality":"세부사항에 강하고 책임감 높은 사람. 규칙 잘 지키고 신뢰감 있는 타입."},
        {"career":"공무원 / 행정직 🏛️",
         "majors":"행정학, 정책학, 법학",
         "personality":"체계적이고 꾸준히 준비할 수 있는 꼼꼼한 성격."}
    ],
    "ISFJ": [
        {"career":"간호사 / 보건직 ❤️",
         "majors":"간호학, 보건학, 사회복지학",
         "personality":"남을 돌보는 성향이 강하고 세심한 배려를 잘하는 타입."},
        {"career":"초등교사 / 교육 관련 🌱",
         "majors":"교육학, 유아교육, 아동학",
         "personality":"인내심 있고 학생들과 안정적인 관계를 잘 맺는 사람."}
    ],
    "INFJ": [
        {"career":"임상심리사 / 상담사 💬",
         "majors":"심리학, 상담학, 사회복지학",
         "personality":"사람의 내면을 이해하려 하고 깊은 공감 능력이 있는 타입."},
        {"career":"사회적 기업가 / NGO 활동가 🌍",
         "majors":"사회학, 국제학, 지속가능경영",
         "personality":"가치 중심적이고 세상을 더 좋게 만들고 싶은 사람."}
    ],
    "INTJ": [
        {"career":"연구원 / 전략기획자 🔬",
         "majors":"수학, 물리, 컴퓨터공학, 경영학(전략)",
         "personality":"논리적 사고와 장기 플랜을 잘 세우는 독창적 타입."},
        {"career":"소프트웨어 아키텍트 / 개발자 💻",
         "majors":"컴퓨터공학, 소프트웨어학",
         "personality":"문제 해결을 차분히 해내는 분석가형."}
    ],
    "ISTP": [
        {"career":"기계공학자 / 엔지니어 🛠️",
         "majors":"기계공학, 전기공학, 메카트로닉스",
         "personality":"실용적이고 손으로 직접 만들어 보는 걸 좋아하는 타입."},
        {"career":"파일럿 / 항공정비 ✈️",
         "majors":"항공운항학, 항공정비학",
         "personality":"빠르게 상황 판단하고 행동으로 옮기는 데 능한 사람."}
    ],
    "ISFP": [
        {"career":"디자이너 (패션/그래픽) 🎨",
         "majors":"시각디자인, 패션디자인, 산업디자인",
         "personality":"감각적이고 창의적인 표현을 좋아하는 따뜻한 타입."},
        {"career":"사진작가 / 영상편집가 📷",
         "majors":"미디어학, 영상학, 사진학",
         "personality":"감수성이 풍부하고 순간을 포착하는 능력이 좋은 사람."}
    ],
    "INFP": [
        {"career":"작가 / 콘텐츠 크리에이터 ✍️",
         "majors":"문예창작, 국문학, 커뮤니케이션",
         "personality":"이상과 가치 중심으로 깊이 있는 글을 쓰는 걸 좋아함."},
        {"career":"문화예술치료사 / 상담 💖",
         "majors":"심리학, 예술치료, 사회복지학",
         "personality":"다정하고 타인 감정에 민감해 도움을 주고 싶은 타입."}
    ],
    "INTP": [
        {"career":"데이터 사이언티스트 / 연구원 📈",
         "majors":"통계학, 컴퓨터공학, 수학",
         "personality":"지적 호기심이 왕성하고 개념을 구조화하는 걸 좋아함."},
        {"career":"소프트웨어 개발자 / 시스템 설계자 🧩",
         "majors":"컴퓨터공학, 소프트웨어학",
         "personality":"논리적이고 새로운 아이디어를 실험해보는 타입."}
    ],
    "ESTP": [
        {"career":"영업 / 마케팅 실무 💼",
         "majors":"경영학, 광고홍보학, 마케팅",
         "personality":"활발하고 사람 상대하는 걸 즐기며 설득력이 좋은 타입."},
        {"career":"응급구조사 / 소방관 🚒",
         "majors":"응급구조학, 소방안전학",
         "personality":"위기 상황에서 빠르게 움직이고 행동하는 것을 즐김."}
    ],
    "ESFP": [
        {"career":"무대예술가 / 공연예술 🎭",
         "majors":"연극영화학, 뮤지컬학, 공연예술",
         "personality":"표현력이 풍부하고 사람들 앞에서 빛나는 걸 좋아함."},
        {"career":"이벤트 플래너 / 서비스업 🥳",
         "majors":"관광학, 레저스포츠학, 호텔경영",
         "personality":"사교적이고 분위기 만드는 걸 잘하는 타입."}
    ],
    "ENFP": [
        {"career":"광고 카피라이터 / 크리에이티브 ✨",
         "majors":"커뮤니케이션, 광고홍보, 문예창작",
         "personality":"아이디어가 많고 사람을 끌어들이는 매력이 있음."},
        {"career":"창업가 / 스타트업 마케터 🚀",
         "majors":"경영학, 창업학, 디자인씽킹",
         "personality":"새로운 걸 시도하고 사람들과 협업하는 걸 즐김."}
    ],
    "ENTP": [
        {"career":"컨설턴트 / 전
