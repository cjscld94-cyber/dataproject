# app.py
import streamlit as st
import pandas as pd
import numpy as np
import io

import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(page_title="Countries MBTI Explorer", layout="wide", initial_sidebar_state="expanded")

MBTI_COLUMNS = ["INFJ","ISFJ","INTP","ISFP","ENTP","INFP","ENTJ","ISTP","INTJ","ESFP","ESTJ","ENFP","ESTP","ISTJ","ENFJ","ESFJ"]

@st.cache_data
def load_data_from_path(path):
    return pd.read_csv(path)

@st.cache_data
def load_data_from_upload(uploaded_file):
    return pd.read_csv(uploaded_file)

def get_basic_stats(df):
    stats = df[MBTI_COLUMNS].describe().T
    stats = stats.rename(columns={"25%":"q1","50%":"median","75%":"q3"})
    return stats[["mean","std","min","q1","median","q3","max"]]

def top_countries_by_type(df, mbti_type, top_n=10, ascending=False):
    return df[["Country", mbti_type]].sort_values(by=mbti_type, ascending=ascending).head(top_n)

def correlation_heatmap(df):
    corr = df[MBTI_COLUMNS].corr()
    fig = px.imshow(corr, 
                    labels=dict(x="MBTI Type", y="MBTI Type", color="Correlation"),
                    x=MBTI_COLUMNS, y=MBTI_COLUMNS,
                    zmin=-1, zmax=1,
                    color_continuous_scale="RdBu")
    fig.update_layout(height=700, width=700, margin=dict(l=0,r=0,t=30,b=0))
    return fig

def bar_most_common_types(df, top_n=6):
    means = df[MBTI_COLUMNS].mean().sort_values(ascending=False).head(top_n)
    fig = px.bar(x=means.index, y=means.values, labels={"x":"MBTI Type", "y":"Average Proportion"}, title=f"Top {top_n} Most Common MBTI Types (global average)")
    return fig

def plot_country_profile(df, country):
    row = df[df["Country"]==country]
    if row.empty:
        return None
    values = row[MBTI_COLUMNS].iloc[0].values
    fig = go.Figure(go.Bar(x=MBTI_COLUMNS, y=values))
    fig.update_layout(title=f"{country} — MBTI 분포", xaxis_title="MBTI Type", yaxis_title="Proportion")
    return fig

def perform_kmeans(df, n_clusters=4, random_state=42):
    X = df[MBTI_COLUMNS].values
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    km = KMeans(n_clusters=n_clusters, random_state=random_state)
    labels = km.fit_predict(Xs)
    return labels, Xs, km, scaler

def pca_scatter(Xs, labels, df_countries):
    pca = PCA(n_components=2)
    comp = pca.fit_transform(Xs)
    plot_df = pd.DataFrame(comp, columns=["PC1","PC2"])
    plot_df["cluster"] = labels.astype(str)
    plot_df["Country"] = df_countries["Country"].values
    fig = px.scatter(plot_df, x="PC1", y="PC2", color="cluster", hover_data=["Country"], title="PCA of MBTI distributions (2 components)")
    return fig

def download_link(df):
    towrite = io.BytesIO()
    df.to_csv(towrite, index=False)
    towrite.seek(0)
    return towrite

# --- UI ---

st.title("🌐 Countries MBTI Explorer")
st.markdown("158개 국가의 MBTI 16유형 비율 데이터셋을 인터랙티브하게 탐색합니다. "
            "왼쪽 사이드바에서 데이터 로드와 분석 옵션을 선택하세요.")

# Sidebar - Data input
st.sidebar.header("데이터 로드")
use_sample = st.sidebar.checkbox("내장 sample 사용 (없으면 업로드 필요)", value=True)
uploaded_file = st.sidebar.file_uploader("CSV 파일 업로드", type=["csv"])

df = None
if uploaded_file is not None:
    try:
        df = load_data_from_upload(uploaded_file)
        st.sidebar.success("업로드 파일을 불러왔습니다.")
    except Exception as e:
        st.sidebar.error(f"파일을 읽는 중 오류: {e}")

if df is None and use_sample:
    # 기본 경로 시도 (Streamlit Cloud에 파일을 함께 올렸을 때)
    try:
        df = load_data_from_path("countriesMBTI_16types.csv")
        st.sidebar.info("프로젝트 폴더의 countriesMBTI_16types.csv 를 불러왔습니다.")
    except FileNotFoundError:
        st.sidebar.warning("내장 sample 파일을 찾을 수 없습니다. 로컬에 파일을 놓거나 업로드하세요.")

if df is None:
    st.info("데이터 파일이 필요합니다. 왼쪽에서 CSV를 업로드하거나 'use sample' 체크박스를 켜고 파일을 프로젝트에 추가하세요.")
    st.stop()

# Validate columns
missing_cols = [c for c in MBTI_COLUMNS if c not in df.columns]
if missing_cols:
    st.error(f"데이터에 다음 MBTI 컬럼들이 없습니다: {missing_cols}")
    st.stop()

# Main tabs
tabs = st.tabs(["요약", "국가 비교", "상관 & 히트맵", "클러스터링", "데이터 다운로드"])

# --- 요약 탭 ---
with tabs[0]:
    st.header("데이터 기본 요약")
    st.write(f"행 수: {df.shape[0]}  |  열 수: {df.shape[1]}")
    st.subheader("샘플 데이터 (상위 10개)")
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("MBTI별 요약 통계 (평균/표준편차 등)")
    stats = get_basic_stats(df)
    st.dataframe(stats.style.format("{:.4f}"))

    st.subheader("세계 평균에서 가장 흔한 MBTI 유형")
    top_bar = bar_most_common_types(df, top_n=8)
    st.plotly_chart(top_bar, use_container_width=True)

# --- 국가 비교 탭 ---
with tabs[1]:
    st.header("국가별 MBTI 비교")
    country_list = df["Country"].sort_values().tolist()
    selected_country = st.selectbox("국가 선택", country_list, index=0)
    country_fig = plot_country_profile(df, selected_country)
    if country_fig:
        st.plotly_chart(country_fig, use_container_width=True)
    else:
        st.info("선택한 국가 데이터가 없습니다.")

    st.markdown("---")
    st.subheader("특정 MBTI 유형에서 상위/하위 국가")
    sel_type = st.selectbox("MBTI 유형 선택", MBTI_COLUMNS, index=0)
    top_n = st.slider("표시할 국가 수 (Top N)", min_value=3, max_value=30, value=10)
    order = st.radio("정렬", ["높은 순 (Top)","낮은 순 (Bottom)"])
    ascending = (order == "낮은 순 (Bottom)")
    result = top_countries_by_type(df, sel_type, top_n=top_n, ascending=ascending)
    st.dataframe(result.reset_index(drop=True))

    # Bar chart for top_n
    fig = px.bar(result, x=sel_type, y="Country", orientation="h", title=f"{sel_type} — {'Lowest' if ascending else 'Highest'} {top_n} countries")
    st.plotly_chart(fig, use_container_width=True)

# --- 상관 & 히트맵 탭 ---
with tabs[2]:
    st.header("MBTI 유형 간 상관관계")
    st.write("상관계수(피어슨)를 사용합니다.")
    heatmap_fig = correlation_heatmap(df)
    st.plotly_chart(heatmap_fig, use_container_width=True)

    st.subheader("상관계수 표")
    corr_table = df[MBTI_COLUMNS].corr().round(3)
    st.dataframe(corr_table)

# --- 클러스터링 탭 ---
with tabs[3]:
    st.header("KMeans 클러스터링 (국가 그룹화)")
    st.write("MBTI 비율을 표준화(정규화)한 뒤 KMeans를 수행합니다. PCA(2차원)로 시각화합니다.")

    n_clusters = st.slider("클러스터 수", min_value=2, max_value=10, value=4)
    random_state = st.number_input("random_state (재현성)", value=42, step=1)
    run_clustering = st.button("클러스터링 실행")

    if run_clustering:
        labels, Xs, km, scaler = perform_kmeans(df, n_clusters=n_clusters, random_state=int(random_state))
        df_clusters = df.copy()
        df_clusters["cluster"] = labels
        st.subheader("각 클러스터의 국가 수")
        st.table(df_clusters["cluster"].value_counts().sort_index())

        st.subheader("PCA 시각화 (클러스터 결과)")
        pca_fig = pca_scatter(Xs, labels, df)
        st.plotly_chart(pca_fig, use_container_width=True)

        st.subheader("클러스터별 평균 MBTI 프로파일")
        cluster_profile = df_clusters.groupby("cluster")[MBTI_COLUMNS].mean().T
        st.dataframe(cluster_profile.style.format("{:.4f}"))

        st.subheader("선택한 클러스터의 국가 목록")
        chosen_cluster = st.selectbox("클러스터 선택", sorted(df_clusters["cluster"].unique().tolist()))
        st.dataframe(df_clusters[df_clusters["cluster"]==chosen_cluster][["Country"]+MBTI_COLUMNS].reset_index(drop=True))

# --- 데이터 다운로드 탭 ---
with tabs[4]:
    st.header("데이터 다운로드")
    st.markdown("현재 사용 중인 데이터셋을 CSV로 다운로드할 수 있습니다.")
    towrite = download_link(df)
    st.download_button("CSV 다운로드", data=towrite, file_name="countriesMBTI_16types_used.csv", mime="text/csv")

    st.markdown("---")
    st.caption("앱을 더 확장하고 싶으시면 대시보드 구성, 대륙 컬럼 추가, 시계열(있을 경우) 분석, 더 정교한 클러스터링(예: GaussianMixture) 등을 추가할 수 있습니다.")
