import streamlit as st
import pandas as pd
import random
import folium
from folium import plugins
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
from matplotlib import font_manager
from dash_utils import * 
from streamlit_option_menu import option_menu
from st_on_hover_tabs import on_hover_tabs

# Streamlit 애플리케이션 설정
st.set_page_config(
    page_title="AIoFarm 종합 모니터링 DashBoard",
    layout="wide",
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": None
    }
)

# 한글 폰트 설정
font_path = "./fonts/Nanum_Gothic/NanumGothic-Bold.ttf"  # ttf 파일 경로
font_prop = font_manager.FontProperties(fname=font_path)

# 사이드 바 생성
with st.sidebar:
    # 사이드바 제목
    st.header("📊 Dashboard") 
    # 개행 추가 (간격 생성)
    st.markdown("<br>", unsafe_allow_html=True)

    # 사이드바 목록 & 아이콘 설정
    tabs = on_hover_tabs(tabName=['home', '인삼농협 현황', '4년근', '5년근', '6년근'], 
                         iconName=['home','pin_drop', 'bar_chart_4_bars', 'bar_chart_4_bars', 'bar_chart_4_bars'],
                         styles = {'navtab': {'background-color':'#E5F0D4', # 메뉴 선택 색
                                              'color': '#414141', #아이콘 및 페이지명 색
                                              'font-size': '16px',
                                              'transition': '.3s',
                                              'white-space': 'nowrap',
                                              'text-transform': 'uppercase'},
                                   'tabOptionsStyle': {':hover :hover': {'color': '#F4F4F4',
                                                                  'cursor': 'pointer'}},
                                   'iconStyle':{'position':'fixed',
                                                'left':'17.5px',
                                                'text-align': 'left'},
                                   'tabStyle' : {'list-style-type': 'none',
                                                 'margin-bottom': '30px',
                                                 'padding-left': '30px'}},
                         key="1", default_choice=0)

# 색상 변경 
green_colors = ["#184A2F", "#1A7043", "#198049"]
# ["#A9C46C", "#809D3C", "#5D8736", "#5D8736"]
# ["#327e54", "#0e7560", "#006a68", "#065f68", "#215363", "#2f4858"]

# 탭 전환
if tabs == 'home':
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
    
    # CSV 데이터 로드
    df = pd.read_csv('dangerousginseng_extended_2000_new.csv')
    
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
        animate_number(abnormal, "불량", "#FADA7A")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 농가별 데이터 표시
    farm_summary = df.groupby(['농가 번호', '농가 명', '입고일자']).agg(
        총합=('불량', 'count'), 정상=('불량', lambda x: (x == 0).sum()), 불량=('불량', 'sum')
    ).reset_index()
    
    selected_farm = st.selectbox("세부 데이터를 확인할 농가를 선택하세요", farm_summary['농가 명'].unique())
    st.session_state["selected_farm"] = selected_farm
    st.dataframe(farm_summary, use_container_width=True)

# 탭 전환
elif tabs == '인삼농협 현황':
    # CSV 파일을 pandas로 읽어들임
    locations = pd.read_csv('location.csv')
    
    # column 형 변환
    locations['lat'] = locations['lat'].astype(float)
    locations['lon'] = locations['lon'].astype(float)
    
    # 서울 중심으로 기본 지도 설정
    m = folium.Map(location=[37.514575, 127.0495556], zoom_start=8)
    
    # 마커 클러스터 설정
    marker_cluster = MarkerCluster().add_to(m)
    
    # 각 위치에 마커 추가
    for idx, row in locations.iterrows():
        name, lat, lon = row['name'], row['lat'], row['lon']
        # 팝업에 HTML로 스타일을 추가하여 글자 크기 키우기
        popup_html = f'<div style="font-size: 18px;">{name}</div>'
        
        folium.Marker(
            location=[lat, lon],
            icon=folium.Icon(color='blue', icon='info-sign', icon_size=(40, 40)),
            popup=folium.Popup(popup_html, max_width=200)  # 팝업 크기도 조정 가능
        ).add_to(marker_cluster)

    
    
    # 지도 표시
    st.markdown(f"""
        <h3 style="text-align: center;">전국 인삼농협 분포 현황</h3><br>
    """, unsafe_allow_html=True)
    
    # 열을 사용하여 가로로 가운데 정렬
    col1, col2, col3 = st.columns([1, 4, 1])  # 가운데 열 비율을 4로 설정
    
    # 가운데 열에 지도 삽입
    with col2:
        st_folium(m, width=700, height=600)
    
# 탭 전환
elif tabs == '4년근':
    # 선택된 농가 정보 가져오기
    selected_farm = st.session_state.get("selected_farm", None)

    # Exception Handler: 농가 선택하지 않고 접근할 때
    if selected_farm is None:
        st.warning("메인 페이지에서 농가를 선택해주세요!")
    else:
        st.markdown(f"""
        <h3 style="text-align: center;">{selected_farm} 4년근 데이터</h3>
    """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
    
        # CSV 데이터 로드
        df = pd.read_csv('dangerousginseng_extended_2000_new.csv')
        df = df[df['농가 명'] == selected_farm]
        df = df[df['연근(4,5,6년근)'] == '4년근']
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
            animate_number(abnormal, "불량", "#FADA7A") #  FFC5C5
        
        st.markdown("<br><br>", unsafe_allow_html=True)
    
        # 정보
        farm_number = df['농가 번호'][0]
        farm_name = df['농가 명'][0]
        arrival_date = df['입고일자'][0]
    
        basic_information = f"""
                    <div style="display: flex; flex-direction: column; gap: 8px; padding: 12px; 
                                border: 1px solid gray; border-radius: 8px; background-color: #FFFFFF;">
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
        four_year = [grade_counts.get(f"4년근 {size}", 0) for size in ["소", "중", "대"]]
    
        # 하위 탭 구성
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
                    four_year,
                    labels=["대", "중", "소"],
                    autopct="%.1f%%",
                    startangle=90,
                    textprops={"fontproperties": font_prop},
                    colors=green_colors[:3]
                )
                for autotext in autotexts:
                    autotext.set_color("white")
    
                # 배경색 변경
                fig.set_facecolor('#F4F4F4')  # 배경색을 연한 회색으로 설정
                st.pyplot(fig)
        
            # Bar Chart
            with col3:
                st.subheader('크기 별 선별 현황')
                sizes = ['소', '중', '대']
                df_bar = pd.DataFrame({size: [df['등급 판정 결과'].str.contains(f"4년근 {size}").sum()] for size in sizes})
        
                fig2, ax2 = plt.subplots()
                ax2.barh(sizes, df_bar.iloc[0], color=green_colors[:3])
                ax2.set_yticklabels(["대", "중", "소"], 
                                    fontproperties=font_manager.FontProperties(fname=font_path))
                
                # 축 라벨 및 제목 설정
                ax2.set_xlabel("개수", fontproperties=font_manager.FontProperties(fname=font_path))
                ax2.set_ylabel("크기", fontproperties=font_manager.FontProperties(fname=font_path))
                ax2.set_title("크기 분포", fontproperties=font_manager.FontProperties(fname=font_path))
    
                fig2.set_facecolor('#F4F4F4')  # 배경색을 연한 회색으로 설정
        
                st.pyplot(fig2)

        # 이미지 & 불량 탭탭
        with tab2:
             # 레이아웃 설정
            cols_main = st.columns([1, 0.5, 1.5])
        
            # 이미지 6개를 2x3 형태로 배치
            with cols_main[0]:
                st.write("#### 세부 이미지")
                img_cols = st.columns(3)
                images = ["images/image1.png", "images/image2.png", "images/image3.png", "images/image4.png", "images/image5.png", "images/image6.png"]
                for i in range(6):
                    with img_cols[i % 3]:
                        st.image(images[i], use_container_width=True)
        
            # 분석 결과 이미지
            with cols_main[1]:
                st.write("#### 결과 이미지")
                st.image("images/4years.png", caption="분석 결과 이미지", use_container_width=True)
    
            random_values = [random.uniform(5, 40) for _ in range(6)]
            random_sum = sum(random_values)
            random_values = [value / random_sum * 100 for value in random_values]
            
            # 원형 그래프
            with cols_main[2]:
                st.write("#### 분석 차트")
                pie_cols = st.columns(2)
                with pie_cols[0]:
                    fig1, ax1 = plt.subplots()
                    ax1.pie([normal, abnormal], labels=["정상", "불량"], autopct="%.1f%%", startangle=90, 
                            textprops={"fontproperties": font_manager.FontProperties(fname=font_path)}, 
                            colors=["#327E54", "#F7C708"])
                    ax1.set_title("누적 데이터", fontproperties=font_prop)
                    fig1.set_facecolor('#F4F4F4')  # 배경색을 연한 회색으로 설정
                    st.pyplot(fig1)
                with pie_cols[1]:
                    fig2, ax2 = plt.subplots()
                    ax2.pie(
                        random_values, 
                        labels=["무게 부족", "스크래치", "찍힘", "벌레", "착색", "동외종"],
                        autopct="%.1f%%",
                        startangle=90, 
                        textprops={"fontproperties": font_manager.FontProperties(fname=font_path)},
                        colors=["#F7AA07", "#F7E407", "#F7C707", "#F78B07", "#D5F707", "#F7D85A"],
                    )
                    ax2.set_title("불량 분석", fontproperties=font_prop)
                    fig2.set_facecolor('#F4F4F4')  # 배경색을 연한 회색으로 설정
                    st.pyplot(fig2)

# 탭 전환
elif tabs == '5년근':
    # 선택된 농가 정보 가져오기
    selected_farm = st.session_state.get("selected_farm", None)

    # Exception Handler: 농가 선택하지 않고 접근할 때
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
        
        st.markdown("<br><br>", unsafe_allow_html=True)
    
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
                fig.set_facecolor('#F4F4F4')  # 배경색을 연한 회색으로 설정
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
    
                fig2.set_facecolor('#F4F4F4')  # 배경색을 연한 회색으로 설정
        
                st.pyplot(fig2)
        with tab2:
             # 레이아웃 설정
            cols_main = st.columns([1, 0.5, 1.5])
        
            # 이미지 6개를 2x3 형태로 배치
            with cols_main[0]:
                st.write("#### 세부 이미지")
                img_cols = st.columns(3)
                images = ["images/image1.png", "images/image2.png", "images/image3.png", "images/image4.png", "images/image5.png", "images/image6.png"]
                for i in range(6):
                    with img_cols[i % 3]:
                        st.image(images[i], use_container_width=True)
    
            random_values = [random.uniform(5, 40) for _ in range(6)]
            random_sum = sum(random_values)
            random_values = [value / random_sum * 100 for value in random_values]
            
            # 분석 결과 이미지
            with cols_main[1]:
                st.write("#### 결과 이미지")
                st.image("images/5years_result.png", caption="분석 결과 이미지", use_container_width=True)
        
            # 원형 그래프
            with cols_main[2]:
                st.write("#### 분석 차트")
                pie_cols = st.columns(2)
                with pie_cols[0]:
                    fig1, ax1 = plt.subplots()
                    ax1.pie([normal, abnormal], labels=["정상", "불량"], autopct="%.1f%%", startangle=90, 
                            textprops={"fontproperties": font_manager.FontProperties(fname=font_path)}, 
                            colors=["#327E54", "#F7C708"])
                    ax1.set_title("누적 데이터", fontproperties=font_prop)
                    fig1.set_facecolor('#F4F4F4')  # 배경색을 연한 회색으로 설정
                    st.pyplot(fig1)
                with pie_cols[1]:
                    fig2, ax2 = plt.subplots()
                    ax2.pie(
                        random_values, 
                        labels=["무게 부족", "스크래치", "찍힘", "벌레", "착색", "동외종"],
                        autopct="%.1f%%",
                        startangle=90, 
                        textprops={"fontproperties": font_manager.FontProperties(fname=font_path)},
                        colors=["#F7AA07", "#F7E407", "#F7C707", "#F78B07", "#D5F707", "#F7D85A"],
                    )
                    ax2.set_title("불량 분석", fontproperties=font_prop)
                    fig2.set_facecolor('#F4F4F4')  # 배경색을 연한 회색으로 설정
                    st.pyplot(fig2)

# 탭 전환
elif tabs == '6년근':
    # 선택된 농가 정보 가져오기
    selected_farm = st.session_state.get("selected_farm", None)
    
    # Exception Handler: 농가 선택하지 않고 접근할 때
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
            animate_number(abnormal, "불량", "#FADA7A")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
    
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
    
        # 6년근 데이터 필터링
        grade_counts = df['등급 판정 결과'].value_counts()
        six_year = [grade_counts.get(f"6년근 {size}", 0) for size in ["소", "중", "대"]]
    
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
                    six_year,
                    labels=["대", "중", "소"],
                    autopct="%.1f%%",
                    startangle=90,
                    textprops={"fontproperties": font_prop},
                    colors=green_colors[:3]
                )
                for autotext in autotexts:
                    autotext.set_color("white")
                    
                fig.set_facecolor('#F4F4F4')  # 배경색을 연한 회색으로 설정
                
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
    
                fig2.set_facecolor('#F4F4F4')  # 배경색을 연한 회색으로 설정
        
                st.pyplot(fig2)
        with tab2:
             # 레이아웃 설정
            cols_main = st.columns([1, 0.5, 1.5])
        
            # 이미지 6개를 2x3 형태로 배치
            with cols_main[0]:
                st.write("#### 세부 이미지")
                img_cols = st.columns(3)
                images = ["images/image1.png", "images/image2.png", "images/image3.png", "images/image4.png", "images/image5.png", "images/image6.png"]
                for i in range(6):
                    with img_cols[i % 3]:
                        st.image(images[i], use_container_width=True)
        
            # 분석 결과 이미지
            with cols_main[1]:
                st.write("#### 결과 이미지")
                st.image("images/6years.png", caption="분석 결과 이미지", use_container_width=True)
    
            random_values = [random.uniform(5, 40) for _ in range(6)]
            random_sum = sum(random_values)
            random_values = [value / random_sum * 100 for value in random_values]
            
            # 원형 그래프
            with cols_main[2]:
                st.write("#### 분석 차트")
                pie_cols = st.columns(2)
                with pie_cols[0]:
                    fig1, ax1 = plt.subplots()
                    ax1.pie([normal, abnormal], labels=["정상", "불량"], autopct="%.1f%%", startangle=90, 
                            textprops={"fontproperties": font_manager.FontProperties(fname=font_path)}, 
                            colors=["#327E54", "#F7C708"])
                    ax1.set_title("누적 데이터", fontproperties=font_prop)
                    
                    fig1.set_facecolor('#F4F4F4')  # 배경색을 연한 회색으로 설정
                    
                    st.pyplot(fig1)
                with pie_cols[1]:
                    fig2, ax2 = plt.subplots()
                    ax2.pie(
                        random_values, 
                        labels=["무게 부족", "스크래치", "찍힘", "벌레", "착색", "동외종"],
                        autopct="%.1f%%",
                        startangle=90, 
                        textprops={"fontproperties": font_manager.FontProperties(fname=font_path)},
                        colors=["#F7AA07", "#F7E407", "#F7C707", "#F78B07", "#D5F707", "#F7D85A"],
                    )
                    ax2.set_title("불량 분석", fontproperties=font_prop)
                    
                    fig2.set_facecolor('#F4F4F4')  # 배경색을 연한 회색으로 설정
                    
                    st.pyplot(fig2)

