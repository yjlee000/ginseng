import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from dash_utils import * 
from matplotlib import font_manager

# 한글 폰트 설정
font_path = "./fonts/Nanum_Gothic/NanumGothic-Bold.ttf"  # ttf 파일 경로
font_prop = font_manager.FontProperties(fname=font_path)

green_colors = ["#184A2F", "#1A7043", "#198049"]
# ["#A9C46C", "#809D3C", "#5D8736", "#5D8736"]

# 선택된 농가 정보 가져오기
selected_farm = st.session_state.get("selected_farm", None)

# # 버튼 없이 페이지 링크 추가
# st.sidebar.page_link("pages/4year.py", label="4년근")
# st.sidebar.page_link("pages/5year.py", label="5년근")
# st.sidebar.page_link("pages/6year.py", label="6년근")

if selected_farm is None:
    st.warning("메인 페이지에서 농가를 선택해주세요!")
else:
    st.markdown(f"""
    <h3 style="text-align: center;">{selected_farm} 5년근 데이터</h3>
""", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)

    # CSV 데이터 로드
    df = pd.read_csv('dangerousginseng_extended_2000_new.csv')
    df = df[df['농가 명'] == selected_farm]
    df = df[df['연근(4,5,6년근)'] == '5년근']
    df = df.reset_index(drop=True)  # 기존 인덱스를 제거하고 0부터 다시 부여


    # 불량 계산
    df['불량'] = df[['등외품', '재투입', '불량']].max(axis=1)
    
    # 주요 통계 계산
    total = len(df)
    abnormal = df['불량'].sum()
    normal = total - abnormal
    abnormal_rate = (abnormal / total) * 100
    
    # 메인 화면 수치 출력
    col1, col2, space1, col3, space2, col4, col5 = st.columns([0.6, 1, 0.2, 1, 0.2, 1, 0.6])
    with col2:
        animate_number(total, "총합", "#f9f9f9")
    with col3:
        animate_number(normal, "정상", "#E5F0D4")  # D2E0FB
    with col4:
        animate_number(abnormal, "불량", "#FADA7A")
    
    # st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # 정보
    farm_number = df['농가 번호'][0]
    farm_name = df['농가 명'][0]
    arrival_date = df['입고일자'][0]

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

    # 5년근 데이터 필터링
    grade_counts = df['등급 판정 결과'].value_counts()
    five_year = [grade_counts.get(f"5년근 {size}", 0) for size in ["소", "중", "대"]]

    # 탭 구성
    tab1, tab2 = st.tabs(['기본 정보', '이미지'])

    with tab1:
        col1, space2, col2, space3, col3, space4 = st.columns([1, 0.3, 1, 0.3, 1, 0.3])

        # Basic Information
        with col1:
            st.subheader('기본 정보')
            st.markdown(
                    basic_information,
                    unsafe_allow_html=True
                )
    
        # Pie Chart
        with col2:
            st.subheader("크기 분포")
            fig, ax = plt.subplots()
            wedges, texts, autotexts = ax.pie(
                five_year,
                labels=["대", "중", "소"],
                autopct="%.1f%%",
                startangle=90,
                textprops={"fontproperties": font_prop},
                colors=green_colors[:3]
            )
            for autotext in autotexts:
                autotext.set_color("white")
            st.pyplot(fig)
    
        # Bar Chart
        with col3:
            st.subheader('크기 별 선별 현황')
            sizes = ['소', '중', '대']
            df_bar = pd.DataFrame({size: [df['등급 판정 결과'].str.contains(f"5년근 {size}").sum()] for size in sizes})
    
            fig2, ax2 = plt.subplots()
            ax2.barh(sizes, df_bar.iloc[0], color=green_colors[:3])
            ax2.set_yticklabels(["대", "중", "소"], 
                                fontproperties=font_manager.FontProperties(fname=font_path))
            
            # 축 라벨 및 제목 설정
            ax2.set_xlabel("개수", fontproperties=font_manager.FontProperties(fname=font_path))
            ax2.set_ylabel("크기", fontproperties=font_manager.FontProperties(fname=font_path))
            ax2.set_title("크기 분포", fontproperties=font_manager.FontProperties(fname=font_path))
    
            st.pyplot(fig2)
    with tab2:
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
                ax1.pie([75.6, 24.4], labels=["정상", "불량"], autopct="%.1f%%", startangle=90, 
                        textprops={"fontproperties": font_manager.FontProperties(fname=font_path)}, 
                        colors=["green", "orange"])
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


    
    # col1, space2, col2, space3, col3, space4 = st.columns([1, 0.3, 1, 0.3, 1, 0.3])

    # # Basic Information
    # with col1:
    #     st.subheader('기본 정보')
    #     st.markdown(
    #             basic_information,
    #             unsafe_allow_html=True
    #         )

    # # Pie Chart
    # with col2:
    #     st.subheader("크기 분포")
    #     fig, ax = plt.subplots()
    #     wedges, texts, autotexts = ax.pie(
    #         four_year,
    #         labels=["대", "중", "소"],
    #         autopct="%.1f%%",
    #         startangle=90,
    #         textprops={"fontproperties": font_prop},
    #         colors=green_colors[:3]
    #     )
    #     for autotext in autotexts:
    #         autotext.set_color("white")
    #     st.pyplot(fig)

    # # Bar Chart
    # with col3:
    #     st.subheader('크기 별 선별 현황')
    #     sizes = ['소', '중', '대']
    #     df_bar = pd.DataFrame({size: [df['등급 판정 결과'].str.contains(f"5년근 {size}").sum()] for size in sizes})

    #     fig2, ax2 = plt.subplots()
    #     ax2.barh(sizes, df_bar.iloc[0], color=green_colors[:3])
    #     ax2.set_yticklabels(["대", "중", "소"], 
    #                         fontproperties=font_manager.FontProperties(fname=font_path))
        
    #     # 축 라벨 및 제목 설정
    #     ax2.set_xlabel("개수", fontproperties=font_manager.FontProperties(fname=font_path))
    #     ax2.set_ylabel("크기", fontproperties=font_manager.FontProperties(fname=font_path))
    #     ax2.set_title("크기 분포", fontproperties=font_manager.FontProperties(fname=font_path))

    #     st.pyplot(fig2)
