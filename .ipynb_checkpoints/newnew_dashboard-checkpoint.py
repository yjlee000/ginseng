import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import time

# 한글 폰트 설정
font_path = "./fonts/Nanum_Gothic/NanumGothic-Bold.ttf"  # ttf 파일 경로
font_prop = font_manager.FontProperties(fname=font_path)

# Streamlit 애플리케이션 시작
st.set_page_config(
    page_title="AIoFarm 종합 모니터링 DashBoard",
    layout="wide",
)

# 색상 변경 
green_colors = ["#00286E", "#679AD9", "#8EB4E1", "#A6C4E8"]
# ["#327e54", "#0e7560", "#006a68", "#065f68", "#215363", "#2f4858"]

# 상단 주요 통계 데이터
st.markdown(
"""
<div style="display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 10px; margin-bottom: 20px;">
<img src="https://file.albamon.com/Albamon/Recruit/Photo/C-Photo-View?FN=2024/9/04/JK_CO_kflchq24090413552144.png" alt="AIoFarm" style="width: 60px; height: auto;">
<h3 style="text-align: center; margin: 0;">AIoFarm 종합 모니터링</h3>
</div>
<br>
""",
unsafe_allow_html=True
)

def custom_autopct(pct):
    return f"{pct:.1f}%" if pct > 0 else ""

def animate_number(value, key, background_color, duration=2, suffix="", decimal_places=0):
    value = float(value)  # float로 변환하여 소수점 처리 가능하게 함
    step = max(1, int(value) // (duration * 10))
    placeholder = st.empty()
    
    # 소수점 자리수 처리
    for i in range(0, int(value) + step, step):
        formatted_value = f"{i:,.{decimal_places}f}"  # 소수점 자리수를 적용
        placeholder.markdown(
            f"""
            <div style="border: 2px solid #ccc; border-radius: 10px; padding: 20px; text-align: center; background-color: {background_color};">
                <div style="font-size: 18px; font-weight: bold; color: #666;">{key}</div>
                <div style="font-size: 32px; font-weight: bold; color: #333;">{formatted_value}{suffix}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        time.sleep(0.02)
        
    # 마지막 값 표시
    formatted_value = f"{value:,.{decimal_places}f}"
    placeholder.markdown(
        f"""
        <div style="border: 2px solid #ccc; border-radius: 10px; padding: 20px; text-align: center; background-color: {background_color};">
            <div style="font-size: 18px; font-weight: bold; color: #666;">{key}</div>
            <div style="font-size: 32px; font-weight: bold; color: #333;">{formatted_value}{suffix}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.session_state.total_animated = True  # 애니메이션이 한 번만 실행되도록 설정

# 사이드바 페이지 선택
page = st.sidebar.radio("페이지 선택", ("전체 데이터", "4년근", "5년근", "6년근"))

# CSV 파일 업로드
# uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

# if uploaded_file is not None:
df = pd.read_csv('dangerousginseng_extended_2000_new.csv')

# 불량 계산
df['불량'] = df[['등외품', '재투입', '불량']].max(axis=1)

# 주요 통계 계산
total = len(df)
abnormal = df['불량'].sum()
normal = total - abnormal
abnormal_rate = (abnormal / total) * 100

# 전체 데이터 페이지
if page == "전체 데이터":
    # 메인 화면 수치 출력
    col1, col2, space1, col3, space2, col4, col5 = st.columns([0.6, 1, 0.2, 1, 0.2, 1, 0.6])
    with col2:
        animate_number(total, "총합", "#f9f9f9")
    with col3:
        animate_number(normal, "정상", "#D2E0FB")
    with col4:
        animate_number(abnormal, "불량", "#FFC5C5")

    st.markdown("<br>", unsafe_allow_html=True)

    # 농가별 데이터프레임 생성
    farm_summary = df.groupby(['농가 번호', '농가 명', '입고일자']).agg(
        총합=('불량', 'count'), 정상=('불량', lambda x: (x == 0).sum()), 불량=('불량', 'sum')
    ).reset_index()

    # 농가 명 클릭 시 세부 페이지 이동
    selected_farm = st.selectbox("세부 데이터를 확인할 농가를 선택하세요", farm_summary['농가 명'].unique())

    # 농가별 데이터프레임 표시
    st.dataframe(farm_summary, use_container_width=True)

# 4년근 페이지
elif page == "4년근":
    # st.subheader("4년근 파이 차트")
    grade_counts = df['등급 판정 결과'].value_counts()
    four_year = [grade_counts.get(f"4년근 {size}", 0) for size in ["소", "중", "대"]]

    col1, col2 = st.columns([1,1])

    # Pie Chart
    with col1:
        st.subheader("4년근 파이 차트")
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(
            four_year,
            labels=["대", "중", "소"],
            autopct=custom_autopct,
            startangle=90,
            textprops={"fontproperties": font_manager.FontProperties(fname=font_path)},
            colors=green_colors[:3],
        )

        # 숫자 글씨 색상 변경
        for autotext in autotexts:
            autotext.set_color("white")  # 원하는 색상 설정
        
        st.pyplot(fig)
            
        years = ['4년근']
        sizes = ['소', '중', '대']

        # fig2, ax2 = plt.subplots()
    
    # Bar Chart
    with col2:
        fig2, ax2 = plt.subplots()
        
        st.subheader('연근 별 크기 선별 현황')
        # 막대 간 y축 위치 설정 (간격 0.5)
        grouped_data = {size: [df['등급 판정 결과'].str.contains(f"{year} {size}").sum() for year in years] for size in sizes}
        df_bar = pd.DataFrame(grouped_data, index=years)

        bar_width = 0.3
        y_base = 0
        y_positions = [y_base, y_base + 0.5, y_base + 1]  # 막대 위치 리스트
        
        # 각 크기별로 개별 막대 그리기
        for i, size in enumerate(sizes):
            ax2.barh(
                y_positions[i],
                df_bar.loc["4년근", size],
                height=bar_width,
                color=green_colors[i],
                label=size,
            )
        
        # y축 설정 및 레이블 위치 조정 (각 막대 중심에 라벨 위치)
        ax2.set_yticks([pos for pos in y_positions])
        ax2.set_yticklabels(["소", "중", "대"], fontproperties=font_manager.FontProperties(fname=font_path))
        
        # 축 라벨 및 제목 설정
        ax2.set_xlabel("개수", fontproperties=font_manager.FontProperties(fname=font_path))
        ax2.set_ylabel("크기", fontproperties=font_manager.FontProperties(fname=font_path))
        ax2.set_title("크기 분포", fontproperties=font_manager.FontProperties(fname=font_path))
        
        # 범례 설정
        ax2.legend(
            title="크기",
            prop=font_manager.FontProperties(fname=font_path),
            title_fontproperties=font_manager.FontProperties(fname=font_path),
        )
        
        st.pyplot(fig2)

    

# 5년근 페이지
elif page == "5년근":
    # st.subheader("5년근 파이 차트")
    grade_counts = df['등급 판정 결과'].value_counts()
    five_year = [grade_counts.get(f"5년근 {size}", 0) for size in ["소", "중", "대"]]

    col1, col2 = st.columns([1, 1])

    # Pie Chart
    with col1:
        st.subheader('5년근 Pie Chart')
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(
                five_year,
                labels=["대", "중", "소"],
                autopct=custom_autopct,
                startangle=90,
                textprops={"fontproperties": font_manager.FontProperties(fname=font_path)},
                colors=green_colors[:3],
            )
    
        # 숫자 글씨 색상 변경
        for autotext in autotexts:
            autotext.set_color("white")  # 원하는 색상 설정
        
        st.pyplot(fig)
    
        years = ['5년근']
        sizes = ['소', '중', '대']

        # fig2, ax2 = plt.subplots()
    
    # Bar Chart
    with col2:
        fig2, ax2 = plt.subplots()
        
        st.subheader('연근 별 크기 선별 현황')
        # 막대 간 y축 위치 설정 (간격 0.5)
        grouped_data = {size: [df['등급 판정 결과'].str.contains(f"{year} {size}").sum() for year in years] for size in sizes}
        df_bar = pd.DataFrame(grouped_data, index=years)

        bar_width = 0.3
        y_base = 0
        y_positions = [y_base, y_base + 0.5, y_base + 1]  # 막대 위치 리스트
        
        # 각 크기별로 개별 막대 그리기
        for i, size in enumerate(sizes):
            ax2.barh(
                y_positions[i],
                df_bar.loc["5년근", size],
                height=bar_width,
                color=green_colors[i],
                label=size,
            )
        
        # y축 설정 및 레이블 위치 조정 (각 막대 중심에 라벨 위치)
        ax2.set_yticks([pos for pos in y_positions])
        ax2.set_yticklabels(["소", "중", "대"], fontproperties=font_manager.FontProperties(fname=font_path))
        
        # 축 라벨 및 제목 설정
        ax2.set_xlabel("개수", fontproperties=font_manager.FontProperties(fname=font_path))
        ax2.set_ylabel("크기", fontproperties=font_manager.FontProperties(fname=font_path))
        ax2.set_title("크기 분포", fontproperties=font_manager.FontProperties(fname=font_path))
        
        # 범례 설정
        ax2.legend(
            title="크기",
            prop=font_manager.FontProperties(fname=font_path),
            title_fontproperties=font_manager.FontProperties(fname=font_path),
        )
        
        st.pyplot(fig2)


# 6년근 페이지
elif page == "6년근":
    grade_counts = df['등급 판정 결과'].value_counts()
    six_year = [grade_counts.get(f"6년근 {size}", 0) for size in ["소", "중", "대"]]

    col1, col2 = st.columns([1, 1])

    # Pie Chart
    with col1:
        st.subheader('6년근 Pie Chart')
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(
                six_year,
                labels=["대", "중", "소"],
                autopct=custom_autopct,
                startangle=90,
                textprops={"fontproperties": font_manager.FontProperties(fname=font_path)},
                colors=green_colors[:3],
            )
    
        # 숫자 글씨 색상 변경
        for autotext in autotexts:
            autotext.set_color("white")  # 원하는 색상 설정
        
        st.pyplot(fig)
    
        years = ['6년근']
        sizes = ['소', '중', '대']

        # fig2, ax2 = plt.subplots()
    
    # Bar Chart
    with col2:
        fig2, ax2 = plt.subplots()
        
        st.subheader('연근 별 크기 선별 현황')
        # 막대 간 y축 위치 설정 (간격 0.5)
        grouped_data = {size: [df['등급 판정 결과'].str.contains(f"{year} {size}").sum() for year in years] for size in sizes}
        df_bar = pd.DataFrame(grouped_data, index=years)

        bar_width = 0.3
        y_base = 0
        y_positions = [y_base, y_base + 0.5, y_base + 1]  # 막대 위치 리스트
        
        # 각 크기별로 개별 막대 그리기
        for i, size in enumerate(sizes):
            ax2.barh(
                y_positions[i],
                df_bar.loc["6년근", size],
                height=bar_width,
                color=green_colors[i],
                label=size,
            )
        
        # y축 설정 및 레이블 위치 조정 (각 막대 중심에 라벨 위치)
        ax2.set_yticks([pos for pos in y_positions])
        ax2.set_yticklabels(["소", "중", "대"], fontproperties=font_manager.FontProperties(fname=font_path))
        
        # 축 라벨 및 제목 설정
        ax2.set_xlabel("개수", fontproperties=font_manager.FontProperties(fname=font_path))
        ax2.set_ylabel("크기", fontproperties=font_manager.FontProperties(fname=font_path))
        ax2.set_title("크기 분포", fontproperties=font_manager.FontProperties(fname=font_path))
        
        # 범례 설정
        ax2.legend(
            title="크기",
            prop=font_manager.FontProperties(fname=font_path),
            title_fontproperties=font_manager.FontProperties(fname=font_path),
        )
        
        st.pyplot(fig2)

# else:
#     st.info("CSV 파일을 업로드해주세요.")

