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
    <h3 style="text-align: center;">{selected_farm} 6년근 데이터</h3>
""", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)

    # CSV 데이터 로드
    df = pd.read_csv('dangerousginseng_extended_2000_new.csv')
    df = df[df['농가 명'] == selected_farm]
    df = df[df['연근(4,5,6년근)'] == '6년근']
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
        animate_number(normal, "정상", "#E5F0D4")
    with col4:
        animate_number(abnormal, "불량", "#FFC5C5")
    
    st.markdown("<br><hr><br>", unsafe_allow_html=True)

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

    # 4년근 데이터 필터링
    grade_counts = df['등급 판정 결과'].value_counts()
    four_year = [grade_counts.get(f"6년근 {size}", 0) for size in ["소", "중", "대"]]

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
            four_year,
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
        df_bar = pd.DataFrame({size: [df['등급 판정 결과'].str.contains(f"6년근 {size}").sum()] for size in sizes})

        fig2, ax2 = plt.subplots()
        ax2.barh(sizes, df_bar.iloc[0], color=green_colors[:3])
        ax2.set_yticklabels(["대", "중", "소"], 
                            fontproperties=font_manager.FontProperties(fname=font_path))
        
        # 축 라벨 및 제목 설정
        ax2.set_xlabel("개수", fontproperties=font_manager.FontProperties(fname=font_path))
        ax2.set_ylabel("크기", fontproperties=font_manager.FontProperties(fname=font_path))
        ax2.set_title("크기 분포", fontproperties=font_manager.FontProperties(fname=font_path))

        st.pyplot(fig2)
