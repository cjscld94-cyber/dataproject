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
        {"career":"컨설턴트 / 전략 기획 🧠",
         "majors":"경영학, 경제학, 산업공학",
         "personality":"논쟁을 즐기고 문제에 대한 다각적 접근을 잘함."},
        {"career":"발명가 / 제품기획자 💡",
         "majors":"산업디자인, 기계공학, 컴퓨터공학",
         "personality":"혁신적 아이디어로 솔루션을 만드는 걸 좋아함."}
    ],
    "ESTJ": [
        {"career":"기업관리자 / 운영 매니저 📋",
         "majors":"경영학, 회계학, 산업경영공학",
         "personality":"조직 운영과 규율을 잘 세우고 실행하는 리더형."},
        {"career":"법조인 / 변호사 ⚖️",
         "majors":"법학, 정치외교학",
         "personality":"논리적이고 규칙을 중시하며 책임감이 강함."}
    ],
    "ESFJ": [
        {"career":"의료서비스 관리자 / 간호관리 🌼",
         "majors":"간호학, 보건행정, 사회복지학",
         "personality":"타인 돌봄에 능하고 팀워크를 잘 이끄는 타입."},
        {"career":"HR / 인사담당자 🤝",
         "majors":"경영학(인사), 심리학, 교육학",
         "personality":"사람을 이해하고 지원하는 걸 즐기는 다정한 리더."}
    ],
    "ENFJ": [
        {"career":"교사 / 교육 컨설턴트 🧑‍🏫",
         "majors":"교육학, 상담교육, 심리학",
         "personality":"사람을 이끌고 성장시키는 데 열정적인 타입."},
        {"career":"PR / 커뮤니케이션 매니저 📣",
         "majors":"커뮤니케이션, 미디어학, 광고홍보",
         "personality":"사람과의 소통에 능하고 조직의 얼굴이 되는 걸 잘함."}
    ],
    "ENTJ": [
        {"career":"CEO / 경영진 리더 🏢",
         "majors":"경영학, 경제학, 산업공학",
         "personality":"목표지향적이고 팀을 이끌어 큰 그림을 실현하는 타입."},
        {"career":"전략 컨설턴트 / 투자은행가 💼",
         "majors":"경영학, 금융공학, 경제학",
         "personality":"결단력 있고 분석적으로 사업 기회를 보는 능력 있음."}
    ]
}

# UI
with st.sidebar:
    st.header("선택")
    selected = st.selectbox("너의 MBTI를 골라줘 😊", mbti_list)
    st.write("👉 아래 버튼을 누르면 추천을 보여줄게.")
    show = st.button("추천 보기 🔎")

st.markdown("---")

if show:
    st.subheader(f"{selected} 유형을 골랐구나! 🎉")
    st.write("친구한테 설명해주듯 쉽게 알려줄게 — 두 가지 진로 추천과 어울리는 전공, 성격 팁까지!")
    recs = recommendations.get(selected, [])

    for i, r in enumerate(recs, 1):
        st.markdown(f"### 추천 {i}: {r['career']}")
        with st.expander("자세히 보기 📝", expanded=(i==1)):
            st.write(f"**어떤 전공이 잘 맞을까?**\n\n> {r['majors']}")
            st.write(f"**어떤 성격이 잘 맞을까?**\n\n> {r['personality']}")
            # 친근한 한 줄 팁
            if "간호" in r['career'] or "보건" in r['majors']:
                st.info("팁: 사람을 직접 돌보는 일이니 공감능력과 체력이 큰 장점이야! 💪")
            elif "개발" in r['career'] or "소프트웨어" in r['career'] or "데이터" in r['career']:
                st.info("팁: 논리적으로 생각하고 꾸준히 문제풀이하는 걸 즐기면 딱 맞아! 🧠")
            elif "디자인" in r['career'] or "예술" in r['career']:
                st.info("팁: 감각을 많이 쓰는 분야니까 포트폴리오 하나씩 만들어봐 ✨")
            else:
                st.info("팁: 먼저 소소한 경험(동아리, 봉사, 아르바이트 등)을 해보는 걸 추천해 👍")

    st.markdown("---")
    st.success("마음에 드는 진로가 있었으면 좋겠다! 더 궁금하면 어떤 진로를 더 자세히 알고 싶은지 말해줘 😊")
else:
    st.write("아직 추천을 보지 않았어 — 사이드바에서 MBTI를 고르고 '추천 보기' 버튼을 눌러줘! 🙌")

st.markdown("---")
st.write("⚠️ 참고: 이 추천은 일반적인 성향과 어울리는 전공·진로 아이디어야. 네 개의 MBTI 지표는 참고용으로만 쓰고, 궁금하면 실제 전공 수업이나 직무 체험도 해보자!")

