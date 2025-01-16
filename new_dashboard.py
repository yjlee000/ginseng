import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib import font_manager, rc
import time  # 애니메이션을 위한 time 모듈 import

# 한글 폰트 설정
font_path = "./fonts/Nanum_Gothic/NanumGothic-Bold.ttf"  # ttf 파일 경로
font_prop = font_manager.FontProperties(fname=font_path)

print("폰트 이름:", font_prop.get_name())

if os.path.exists(font_path):
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)
st.set_page_config(
    page_title="AIoFarm 종합 모니터링 DashBoard",
    layout="wide",
)

# 데이터 입력
normal = 1948  # 정상
abnormal = 628  # 불량
total = normal + abnormal
abnormal_rate = (abnormal / total) * 100

def animate_number(value, key, duration=2, suffix=""):
    value = int(value)
    step = max(1, value // (duration * 10))
    placeholder = st.empty()
    for i in range(0, value + step, step):
        placeholder.markdown(
            f"""
            <div style="border: 2px solid #ccc; border-radius: 10px; padding: 20px; text-align: center; background-color: #f9f9f9;">
                <div style="font-size: 18px; font-weight: bold; color: #666;">{key}</div>
                <div style="font-size: 32px; font-weight: bold; color: #333;">{i:,}{suffix}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        time.sleep(0.05)
    placeholder.markdown(
        f"""
        <div style="border: 2px solid #ccc; border-radius: 10px; padding: 20px; text-align: center; background-color: #f9f9f9;">
            <div style="font-size: 18px; font-weight: bold; color: #666;">{key}</div>
            <div style="font-size: 32px; font-weight: bold; color: #333;">{value:,}{suffix}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# 상단 주요 통계 데이터
st.markdown(
    """
    <div style="display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 10px; margin-bottom: 20px;">
        <img src="https://s3.ap-northeast-2.amazonaws.com/inno.bucket.live/corp/logo/CP00013024_20221223161501.png" alt="AIoFarm" style="width: 100px; height: auto;">
        <h3 style="text-align: center; margin: 0;">AIoFarm 종합 모니터링</h3>
    </div>
    """,
    unsafe_allow_html=True
)
col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 1.5, 1.5, 1.5])
with col1:
    animate_number(total, "총합")
with col2:
    animate_number(normal, "정상")
with col3:
    animate_number(abnormal, "불량")
with col4:
    animate_number(round(abnormal_rate, 2), "불량률", suffix="%")
with col5:
    animate_number(3200, "투입 중량", suffix="kg")
with col6:
    animate_number(3120, "선별 완료 중량", suffix="kg")
with col7:
    animate_number(67, "선별 속도", suffix="개/분")

# 탭 구성
tab1, tab2 = st.tabs(["기본 정보 및 차트", "이미지 분석 및 결과"])

# 첫 번째 탭
with tab1:
    st.subheader("기본 정보 및 차트")

    # 기본 정보
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    with col1:
        st.subheader("기본 정보")
        st.markdown(
            """
            <div style="display: flex; flex-direction: column; gap: 8px; padding: 12px; 
                        border: 1px solid gray; border-radius: 8px; background-color: #f9f9f9;">
                <div style="display: flex; justify-content: space-between;">
                    <strong>번호:</strong>
                    <span>2025010608</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <strong>농가명:</strong>
                    <span>응가네 인삼</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <strong>입고일:</strong>
                    <span>2025-01-16</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 원형 차트
    with col2:
        st.subheader("4년근")
        fig, ax = plt.subplots()
        ax.pie([40, 35, 25], labels=["대", "중", "소"], autopct="%1.1f%%", startangle=90, 
              textprops={"fontproperties": font_manager.FontProperties(fname=font_path)})
        ax.axis("equal")
        st.pyplot(fig)

    with col3:
        st.subheader("5년근")
        fig, ax = plt.subplots()
        ax.pie([50, 30, 20], labels=["대", "중", "소"], autopct="%1.1f%%", startangle=90, 
              textprops={"fontproperties": font_manager.FontProperties(fname=font_path)})
        ax.axis("equal")
        st.pyplot(fig)

    with col3:
        st.subheader("6년근")
        fig, ax = plt.subplots()
        ax.pie([60, 25, 15], labels=["대", "중", "소"], autopct="%1.1f%%", startangle=90, 
              textprops={"fontproperties": font_manager.FontProperties(fname=font_path)})
        ax.axis("equal")
        st.pyplot(fig)

    # 가로 막대 그래프
    with col4:
        st.subheader("연근 별 크기 선별 현황")
        years = ["4년근", "5년근", "6년근"]
        data = {"대": [4, 5, 6], "중": [3, 3, 4], "소": [3, 2, 3]}
        df = pd.DataFrame(data, index=years)
        fig2, ax2 = plt.subplots()
        df.plot(kind="barh", stacked=True, ax=ax2, color=["#4CAF50", "#FFC107", "#9E9E9E"])
        ax2.set_xlabel("개수", fontproperties=font_prop)
        ax2.set_ylabel("연근", fontproperties=font_prop)
        ax2.set_title("연근 별 크기 분포", fontproperties=font_prop)
        st.pyplot(fig2)

# 두 번째 탭
with tab2:
    st.subheader("이미지 분석 및 결과")

    # 레이아웃 설정
    cols_main = st.columns([1, 0.5, 1.5])

    # 이미지 6개를 2x3 형태로 배치
    with cols_main[0]:
        st.write("### 2x3 이미지")
        img_cols = st.columns(3)
        images = ["images/image1.png", "images/image2.png", "images/image3.png", "images/image4.png", "images/image5.png", "images/image6.png"]
        for i in range(6):
            with img_cols[i % 3]:
                st.image(images[i], use_container_width=True)

    # 분석 결과 이미지
    with cols_main[1]:
        st.write("### 결과 이미지")
        st.image("images/result_image.png", caption="분석 결과 이미지", use_container_width=True)

    # 원형 그래프
    with cols_main[2]:
        st.write("### 원형 그래프")
        pie_cols = st.columns(2)
        with pie_cols[0]:
            fig1, ax1 = plt.subplots()
            ax1.pie([75.6, 24.4], labels=["정상", "불량"], autopct="%.1f%%", startangle=90, colors=["green", "orange"])
            ax1.set_title("누적 데이터")
            st.pyplot(fig1)
        with pie_cols[1]:
            fig2, ax2 = plt.subplots()
            ax2.pie(
                [39.4, 18.8, 14.5, 10.7, 9.09, 7.49],
                labels=["무게 부족", "스크래치", "찍힘", "벌레", "작색", "동외종"],
                autopct="%.1f%%",
                startangle=90, 
                textprops={"fontproperties": font_manager.FontProperties(fname=font_path)},
                colors=["#fde0dd", "#fa9fb5", "#c51b8a", "#fdae6b", "#fd8d3c", "#e6550d"],
            )
            ax2.set_title("농장 분석")
            st.pyplot(fig2)
