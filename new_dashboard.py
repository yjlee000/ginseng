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

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

# 데이터 읽기
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 데이터 계산
    df['불량'] = df[['등외품', '재투입', '불량']].max(axis=1)

    # 주요 통계
    total = len(df)
    abnormal = df['불량'].sum()
    normal = total - abnormal
    abnormal_rate = (abnormal / total) * 100

    weight = df['중량 (g)'].sum()
    df_normal = df[df['불량']==0]
    weight_normal = df_normal['중량 (g)'].sum()

    # 정보
    farm_number = df['농가 번호'][0]
    farm_name = df['농가 명'][0]
    arrival_date = df['입고일자'][0]


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
        animate_number(round(weight / 1000), "투입 중량", suffix="kg")
    with col6:
        animate_number(round(weight_normal / 1000), "선별 완료 중량", suffix="kg")
    with col7:
        animate_number(67, "선별 속도", suffix="개/분")
    
    # 탭 구성
    tab1, tab2 = st.tabs(["기본 정보 및 차트", "이미지 분석 및 결과"])
    
    basic_information = f"""
                <div style="display: flex; flex-direction: column; gap: 8px; padding: 12px; 
                            border: 1px solid gray; border-radius: 8px; background-color: #f9f9f9;">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>농가 번호:</strong>
                        <span>{farm_number}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <strong>농가명:</strong>
                        <span>{farm_name}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <strong>입고일:</strong>
                        <span>{arrival_date}</span>
                    </div>
                </div>
                """
    # 첫 번째 탭
    with tab1:
        st.subheader("기본 정보 및 차트")
    
        # 기본 정보
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1.5])
        with col1:
            st.subheader("기본 정보")
            st.markdown(
                basic_information,
                unsafe_allow_html=True
            )

    # 원형 차트
    grade_counts = df['등급 판정 결과'].value_counts()

    # 4년근, 5년근, 6년근 데이터 추출 및 집계
    four_year = [grade_counts.get(f"4년근 {size}", 0) for size in ["소", "중", "대"]]
    five_year = [grade_counts.get(f"5년근 {size}", 0) for size in ["소", "중", "대"]]
    six_year = [grade_counts.get(f"6년근 {size}", 0) for size in ["소", "중", "대"]]

    with col2:
        # Streamlit 제목 출력 (HTML 방식으로 폰트 적용)
        st.markdown(
            f"<h3 style='font-family: \"Noto Sans KR\";'>4년근</h3>",
            unsafe_allow_html=True,
        )
        fig, ax = plt.subplots()
        ax.pie(
            four_year,
            labels=["대", "중", "소"],
            autopct="%1.1f%%",
            startangle=90,
            textprops={"fontproperties": font_manager.FontProperties(fname=font_path)},
        )
        ax.axis("equal")
        st.pyplot(fig)

    with col3:
        st.markdown(
            f"<h3 style='font-family: \"Noto Sans KR\";'>5년근</h3>",
            unsafe_allow_html=True,
        )
        fig, ax = plt.subplots()
        ax.pie(
            five_year,
            labels=["대", "중", "소"],
            autopct="%1.1f%%",
            startangle=90,
            textprops={"fontproperties": font_manager.FontProperties(fname=font_path)},
        )
        ax.axis("equal")
        st.pyplot(fig)

    with col4:
        st.markdown(
            f"<h3 style='font-family: \"Noto Sans KR\";'>6년근</h3>",
            unsafe_allow_html=True,
        )
        fig, ax = plt.subplots()
        ax.pie(
            six_year,
            labels=["대", "중", "소"],
            autopct="%1.1f%%",
            startangle=90,
            textprops={"fontproperties": font_manager.FontProperties(fname=font_path)},
        )
        ax.axis("equal")
        st.pyplot(fig)

    # 가로 막대 그래프
    with col5:
        st.markdown(
            f"<h3 style='font-family: \"Noto Sans KR\";'>연근 별 크기 선별 현황</h3>",
            unsafe_allow_html=True,
        )
        years = ['4년근', '5년근', '6년근']
        sizes = ['소', '중', '대']

        # 데이터를 집계하여 DataFrame 생성
        grouped_data = {size: [df['등급 판정 결과'].str.contains(f"{year} {size}").sum() for year in years] for size in sizes}
        df_bar = pd.DataFrame(grouped_data, index=years)
        
        fig2, ax2 = plt.subplots()
        df_bar.plot(kind="barh", stacked=True, ax=ax2, color=["#4CAF50", "#FFC107", "#9E9E9E"])
    
        # 축 라벨 및 제목 설정
        ax2.set_xlabel("개수", fontproperties=font_manager.FontProperties(fname=font_path))
        ax2.set_ylabel("연근", fontproperties=font_manager.FontProperties(fname=font_path))
        ax2.set_title("연근 별 크기 분포", fontproperties=font_manager.FontProperties(fname=font_path))
    
        # y축 한글 폰트 설정
        ax2.set_yticks(range(len(years)))
        ax2.set_yticklabels(years, fontproperties=font_manager.FontProperties(fname=font_path))
    
        # 범례(legend) 설정
        legend = ax2.legend(
            title="크기",
            prop=font_manager.FontProperties(fname=font_path),
            title_fontproperties=font_manager.FontProperties(fname=font_path),
        )
    
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
                    st.image(images[i], use_column_width=True)
    
        # 분석 결과 이미지
        with cols_main[1]:
            st.write("### 결과 이미지")
            st.image("images/result_image.png", caption="분석 결과 이미지", use_column_width=True)  # use_column_width, use_container_width
    
        # 원형 그래프
        with cols_main[2]:
            st.write("### 원형 그래프")
            pie_cols = st.columns(2)
            with pie_cols[0]:
                fig1, ax1 = plt.subplots()
                # 상태별 합계 계산
                status_counts = {
                    "등외품": df["등외품"].sum(),
                    "재투입": df["재투입"].sum(),
                    "불량": df["불량"].sum(),
                }
                labels = list(status_counts.keys())
                sizes = list(status_counts.values())

                fig1, ax1 = plt.subplots()
                ax1.pie(
                    sizes,
                    labels=labels,
                    autopct="%.1f%%",
                    startangle=90,
                    textprops={"fontproperties": font_manager.FontProperties(fname=font_path)},
                    colors=["#fdae6b", "#fd8d3c", "#e6550d"],
                )
                ax1.set_title("누적 데이터", fontproperties=font_prop)
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
                ax2.set_title("농장 분석", fontproperties=font_prop)
                st.pyplot(fig2)

# ###################################################################################################
# import pandas as pd
# import streamlit as st
# import matplotlib.pyplot as plt

# # Streamlit 페이지 설정
# st.set_page_config(
#     page_title="AIoFarm 종합 모니터링 DashBoard",
#     layout="wide",
# )

# # CSV 파일 업로드
# uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

# if uploaded_file is not None:
#     # CSV 파일 읽기
#     df = pd.read_csv(uploaded_file)
    
#     # '불량' 컬럼 계산: '등외품', '재투입', '불량' 중 하나라도 1인 경우
#     df["불량"] = df[["등외품", "재투입", "불량"]].max(axis=1)

#     # 주요 통계 계산
#     total = len(df)  # 총 데이터 개수
#     abnormal = df["불량"].sum()  # 불량 개수
#     normal = total - abnormal  # 정상 개수
#     abnormal_rate = (abnormal / total) * 100  # 불량률

#     # 통계 데이터 출력
#     st.subheader("통계 정보")
#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("총 데이터", total)
#     col2.metric("정상 데이터", normal)
#     col3.metric("불량 데이터", abnormal)
#     col4.metric("불량률 (%)", round(abnormal_rate, 2))

#     # 데이터 테이블 출력
#     st.subheader("업로드된 데이터")
#     st.dataframe(df)

#     # 불량 데이터를 시각화 (원형 그래프)
#     st.subheader("불량 데이터 비율")
#     fig, ax = plt.subplots()
#     ax.pie(
#         [normal, abnormal],
#         labels=["정상", "불량"],
#         autopct="%1.1f%%",
#         startangle=90,
#         colors=["#4CAF50", "#F44336"],
#     )
#     ax.axis("equal")
#     st.pyplot(fig)

# else:
#     st.info("CSV 파일을 업로드해주세요.")

