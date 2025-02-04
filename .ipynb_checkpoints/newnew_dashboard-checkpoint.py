# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib import font_manager

# # 한글 폰트 설정
# font_path = "./fonts/Nanum_Gothic/NanumGothic-Bold.ttf"  # ttf 파일 경로
# font_prop = font_manager.FontProperties(fname=font_path)

# # Streamlit 애플리케이션 시작
# st.title("인삼 데이터 통합 대시보드")

# # CSV 파일 업로드
# uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file)

#     # 불량 계산
#     df['불량'] = df[['등외품', '재투입', '불량']].max(axis=1)
    
#     # 주요 통계 계산
#     total = len(df)
#     abnormal = df['불량'].sum()
#     normal = total - abnormal
#     abnormal_rate = (abnormal / total) * 100
    
#     # 메인 화면 수치 출력
#     st.metric(label="총합", value=total)
#     st.metric(label="정상", value=normal)
#     st.metric(label="불량", value=abnormal)
    
#     # 농가별 데이터프레임 생성
#     farm_summary = df.groupby(['농가 번호', '농가 명']).agg(
#         총합=('불량', 'count'), 정상=('불량', lambda x: (x == 0).sum()), 불량=('불량', 'sum')
#     ).reset_index()
    
#     # 농가 명 클릭 시 세부 페이지 이동
#     selected_farm = st.selectbox("세부 데이터를 확인할 농가를 선택하세요", farm_summary['농가 명'].unique())
    
#     if selected_farm:
#         farm_data = df[df['농가 명'] == selected_farm]
#         tab1, tab2 = st.tabs(["기본 정보 및 차트", "이미지 분석 및 결과"])
        
#         # 첫 번째 탭: 기본 정보 및 차트
#         with tab1:
#             st.subheader("기본 정보 및 차트")
#             st.write(f"농가 번호: {farm_data['농가 번호'].iloc[0]}")
#             st.write(f"입고일: {farm_data['입고일자'].iloc[0]}")
            
#             grade_counts = farm_data['등급 판정 결과'].value_counts()
            
#             four_year = [grade_counts.get(f"4년근 {size}", 0) for size in ["소", "중", "대"]]
#             five_year = [grade_counts.get(f"5년근 {size}", 0) for size in ["소", "중", "대"]]
#             six_year = [grade_counts.get(f"6년근 {size}", 0) for size in ["소", "중", "대"]]
            
#             col1, col2, col3 = st.columns(3)
            
#             for col, year, data in zip([col1, col2, col3], ["4년근", "5년근", "6년근"], [four_year, five_year, six_year]):
#                 with col:
#                     fig, ax = plt.subplots()
#                     ax.pie(
#                         data,
#                         labels=["대", "중", "소"],
#                         autopct="%1.1f%%",
#                         startangle=90,
#                         textprops={"fontproperties": font_manager.FontProperties(fname=font_path)}
#                     )
#                     ax.set_title(year, fontproperties=font_manager.FontProperties(fname=font_path))
#                     st.pyplot(fig)
            
#             # 가로 막대 그래프
#             years = ['4년근', '5년근', '6년근']
#             sizes = ['소', '중', '대']
#             grouped_data = {size: [farm_data['등급 판정 결과'].str.contains(f"{year} {size}").sum() for year in years] for size in sizes}
#             df_bar = pd.DataFrame(grouped_data, index=years)
            
#             fig2, ax2 = plt.subplots()
#             df_bar.plot(kind="barh", stacked=True, ax=ax2)
#             ax2.set_xlabel("개수", fontproperties=font_manager.FontProperties(fname=font_path))
#             ax2.set_ylabel("연근", fontproperties=font_manager.FontProperties(fname=font_path))
#             ax2.set_title("연근 별 크기 분포", fontproperties=font_manager.FontProperties(fname=font_path))
#             ax2.legend(title="크기", prop=font_manager.FontProperties(fname=font_path))
#             st.pyplot(fig2)
        
#         # 두 번째 탭: 이미지 분석 및 결과
#         with tab2:
#             st.subheader("이미지 분석 및 결과")
#             cols_main = st.columns([1, 0.5, 1.5])
            
#             with cols_main[0]:
#                 st.write("### 모든 이미지")
#                 img_cols = st.columns(3)
#                 images = ["images/image1.png", "images/image2.png", "images/image3.png", "images/image4.png", "images/image5.png", "images/image6.png"]
#                 for i in range(6):
#                     with img_cols[i % 3]:
#                         st.image(images[i], use_container_width=True)
            
#             with cols_main[1]:
#                 st.write("### 결과 이미지")
#                 st.image("images/result_image.png", caption="분석 결과 이미지", use_container_width=True)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import time

# 한글 폰트 설정
font_path = "./fonts/Nanum_Gothic/NanumGothic-Bold.ttf"  # ttf 파일 경로
font_prop = font_manager.FontProperties(fname=font_path)

# Streamlit 애플리케이션 시작
# st.title("인삼 데이터 통합 대시보드")

st.set_page_config(
    page_title="AIoFarm 종합 모니터링 DashBoard",
    layout="wide",
)

# 색상 변경 (연보라색 계열 적용)
purple_colors = ["#D8BFD8", "#DDA0DD", "#BA55D3", "#9370DB", "#8A2BE2", "#6A5ACD"]

def animate_number(value, key, duration=2, suffix="", decimal_places=0):
    value = float(value)  # float로 변환하여 소수점 처리 가능하게 함
    step = max(1, int(value) // (duration * 10))
    placeholder = st.empty()
    
    # 소수점 자리수 처리
    for i in range(0, int(value) + step, step):
        formatted_value = f"{i:,.{decimal_places}f}"  # 소수점 자리수를 적용
        placeholder.markdown(
            f"""
            <div style="border: 2px solid #ccc; border-radius: 10px; padding: 20px; text-align: center; background-color: #f9f9f9;">
                <div style="font-size: 18px; font-weight: bold; color: #666;">{key}</div>
                <div style="font-size: 32px; font-weight: bold; color: #333;">{formatted_value}{suffix}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        time.sleep(0.05)
        
    # 마지막 값 표시
    formatted_value = f"{value:,.{decimal_places}f}"
    placeholder.markdown(
        f"""
        <div style="border: 2px solid #ccc; border-radius: 10px; padding: 20px; text-align: center; background-color: #f9f9f9;">
            <div style="font-size: 18px; font-weight: bold; color: #666;">{key}</div>
            <div style="font-size: 32px; font-weight: bold; color: #333;">{formatted_value}{suffix}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.session_state.total_animated = True  # 애니메이션이 한 번만 실행되도록 설정


# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 불량 계산
    df['불량'] = df[['등외품', '재투입', '불량']].max(axis=1)
    
    # 주요 통계 계산
    total = len(df)
    abnormal = df['불량'].sum()
    normal = total - abnormal
    abnormal_rate = (abnormal / total) * 100

    # 상단 주요 통계 데이터
    st.markdown(
    """
    <div style="display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 10px; margin-bottom: 20px;">
    <img src="https://file.albamon.com/Albamon/Recruit/Photo/C-Photo-View?FN=2024/9/04/JK_CO_kflchq24090413552144.png" alt="AIoFarm" style="width: 60px; height: auto;">
    <h3 style="text-align: center; margin: 0;">AIoFarm 종합 모니터링</h3>
    </div>
    """,
    unsafe_allow_html=True
    )
    
    # 메인 화면 수치 출력
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        animate_number(total, "총합")
    with col2:
        animate_number(normal, "정상")
    with col3:
        animate_number(abnormal, "불량")
        
    st.markdown(
        f"<br>",
        unsafe_allow_html=True,
    )

    # 농가별 데이터프레임 생성
    farm_summary = df.groupby(['농가 번호', '농가 명', '입고일자']).agg(
        총합=('불량', 'count'), 정상=('불량', lambda x: (x == 0).sum()), 불량=('불량', 'sum')
    ).reset_index()
    
    # 농가 명 클릭 시 세부 페이지 이동
    selected_farm = st.selectbox("세부 데이터를 확인할 농가를 선택하세요", farm_summary['농가 명'].unique())
    
    
    
    # 농가별 데이터프레임 표시
    st.dataframe(farm_summary, use_container_width=True)
    
    
    
    if selected_farm:
        farm_data = df[df['농가 명'] == selected_farm]
        tab1, tab2 = st.tabs(["기본 정보 및 차트", "이미지 분석 및 결과"])

        basic_information = f"""
                <div style="display: flex; flex-direction: column; gap: 8px; padding: 12px; 
                            border: 1px solid gray; border-radius: 8px; background-color: #f9f9f9;">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>농가 번호:</strong>
                        <span>{farm_data['농가 번호'].iloc[0]}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <strong>농가명:</strong>
                        <span>{farm_data['농가 명'].iloc[0]}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <strong>입고일:</strong>
                        <span>{farm_data['입고일자'].iloc[0]}</span>
                    </div>
                </div>
                """
        
        # 첫 번째 탭: 기본 정보 및 차트
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
            grade_counts = farm_data['등급 판정 결과'].value_counts()

            # 4, 5, 6년근 데이터 추출 및 집계
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
                    colors = purple_colors[:3],
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
                    colors = purple_colors[:3],
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
                    colors = purple_colors[:3],
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
                df_bar.plot(kind="barh", stacked=True, ax=ax2, color=["#D8BFD8", "#DDA0DD", "#BA55D3"])
            
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
            st.write("### 모든 이미지")
            img_cols = st.columns(3)
            images = ["images/image1.png", "images/image2.png", "images/image3.png", "images/image4.png", "images/image5.png", "images/image6.png"]
            for i in range(6):
                with img_cols[i % 3]:
                    st.image(images[i], use_container_width=True)
    
        # 분석 결과 이미지
        with cols_main[1]:
            st.write("### 결과 이미지")
            st.image("images/result_image.png", caption="분석 결과 이미지", use_container_width=True)  # use_column_width, use_container_width
    
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
                    colors=purple_colors[:3],
                )
                ax1.set_title("불량 데이터", fontproperties=font_prop)
                st.pyplot(fig1)
            with pie_cols[1]:
                fig2, ax2 = plt.subplots()
                ax2.pie(
                    [39.4, 18.8, 14.5, 10.7, 9.09, 7.49],
                    labels=["무게 부족", "스크래치", "찍힘", "벌레", "작색", "등외품"],
                    autopct="%.1f%%",
                    startangle=90, 
                    textprops={"fontproperties": font_manager.FontProperties(fname=font_path)},
                    colors=purple_colors,
                )
                ax2.set_title("파삼 분석", fontproperties=font_prop)
                st.pyplot(fig2)

else:
    st.info("CSV 파일을 업로드해주세요.")
