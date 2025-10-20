# app.py
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import webbrowser

st.set_page_config(page_title="Seoul Top10 (Foreigners) — Map", page_icon="🗺️", layout="wide")
st.title("🗺️ 외국인들이 좋아하는 서울 관광지 Top 10 (Folium)")

st.markdown(
    """
    아래 지도에서 관광지를 체크하면 해당 위치에 마커가 표시됩니다.
    각 마커를 클릭하면 간단한 설명과 (있다면) 링크가 나옵니다.
    """
)

# 중심점: 서울 시청 인근
CENTER_LAT, CENTER_LON = 37.5665, 126.9780

# Top10 장소 데이터 (이름, 위도, 경도, 간단설명)
PLACES = [
    {
        "id": "gyeongbokgung",
        "name": "Gyeongbokgung Palace (경복궁)",
        "lat": 37.579617,
        "lon": 126.977041,
        "desc": "조선의 대표 궁궐. 한복 체험과 수문장 교대식으로 유명."
    },
    {
        "id": "changdeokgung",
        "name": "Changdeokgung Palace & Huwon (창덕궁/후원)",
        "lat": 37.579408,
        "lon": 126.991072,
        "desc": "후원(비원)으로 유명한 유네스코 세계유산."
    },
    {
        "id": "bukchon",
        "name": "Bukchon Hanok Village (북촌 한옥마을)",
        "lat": 37.582600,
        "lon": 126.983000,
        "desc": "전통 한옥이 남아있는 포토스팟 동네."
    },
    {
        "id": "insadong",
        "name": "Insadong (인사동)",
        "lat": 37.574011,
        "lon": 126.984901,
        "desc": "전통 찻집, 기념품 숍과 골동품 상점 밀집 지역."
    },
    {
        "id": "myeongdong",
        "name": "Myeongdong (명동)",
        "lat": 37.563817,
        "lon": 126.986041,
        "desc": "쇼핑과 길거리음식의 핫플레이스."
    },
    {
        "id": "nseoultower",
        "name": "N Seoul Tower / Namsan (남산 N타워)",
        "lat": 37.551169,
        "lon": 126.988227,
        "desc": "서울 전망의 대표 스팟 — 야경이 특히 인기."
    },
    {
        "id": "hongdae",
        "name": "Hongdae / Hongik Univ Area (홍대)",
        "lat": 37.556263,
        "lon": 126.923893,
        "desc": "젊음의 거리, 클럽·카페·거리공연이 활발한 지역."
    },
    {
        "id": "ddp",
        "name": "Dongdaemun Design Plaza (동대문 DDP)",
        "lat": 37.566322,
        "lon": 127.009007,
        "desc": "미래지향적 건축과 밤시장, 패션상점이 유명."
    },
    {
        "id": "lotteworld",
        "name": "Lotte World Tower & Seokchon Lake (롯데월드타워/석촌호수)",
        "lat": 37.513090,
        "lon": 127.102516,
        "desc": "초고층 전망대와 쇼핑몰, 호수 산책로."
    },
    {
        "id": "coex",
        "name": "COEX / Starfield Library (코엑스 & 별마당도서관)",
        "lat": 37.511272,
        "lon": 127.059092,
        "desc": "대형 쇼핑몰·전시·아쿠아리움 및 인스타 유명 도서관."
    },
]

# 사이드바: 전체/선택 제어
st.sidebar.header("지도 옵션")
show_all = st.sidebar.checkbox("모든 관광지 표시", value=True)
st.sidebar.write("개별 관광지 보기")
selected = {}
for p in PLACES:
    key = f"show_{p['id']}"
    # 기본: 모든 장소 표시일 때 체크, 아니면 체크 해제
    default = True if show_all else False
    selected[p["id"]] = st.sidebar.checkbox(p["name"], value=default)

# Folium 지도 생성
m = folium.Map(location=[CENTER_LAT, CENTER_LON], zoom_start=12, tiles="OpenStreetMap")
marker_cluster = MarkerCluster(name="Top10 Cluster").add_to(m)

# 마커 추가 (선택된 것만)
for p in PLACES:
    if selected.get(p["id"], False):
        popup_html = f"""
        <b>{p['name']}</b><br>
        {p['desc']}<br>
        <i>위도: {p['lat']}, 경도: {p['lon']}</i>
        """
        folium.Marker(
            location=[p["lat"], p["lon"]],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=p["name"],
        ).add_to(marker_cluster)

# 레이어 컨트롤
folium.LayerControl().add_to(m)

# Streamlit에 Folium 지도 렌더링
st.subheader("서울 관광지 지도")
st_data = st_folium(m, width=1200, height=700)

# 아래는 선택된 장소의 리스트 표시
st.subheader("선택된 관광지 목록")
for p in PLACES:
    if selected.get(p["id"], False):
        st.markdown(f"- **{p['name']}** — {p['desc']}")

st.info("앱을 배포하려면 이 저장소를 GitHub에 올리고 Streamlit Cloud에서 `app.py`를 지정하세요.")

