# import streamlit as st
# import pandas as pd
# import time
# from dash_utils import * 

# # Streamlit 애플리케이션 설정
# st.set_page_config(
#     page_title="AIoFarm 종합 모니터링 DashBoard",
#     layout="wide",
# )

# # 색상 변경 
# green_colors = ["#A9C46C", "#809D3C", "#5D8736", "#5D8736"]
# # ["#327e54", "#0e7560", "#006a68", "#065f68", "#215363", "#2f4858"]

# # 상단 주요 통계 데이터
# st.markdown(
# """
# <div style="display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 10px; margin-bottom: 20px;">
# <img src="https://file.albamon.com/Albamon/Recruit/Photo/C-Photo-View?FN=2024/9/04/JK_CO_kflchq24090413552144.png" alt="AIoFarm" style="width: 60px; height: auto;">
# <h3 style="text-align: center; margin: 0;">AIoFarm 종합 모니터링</h3>
# </div>
# <br>
# """,
# unsafe_allow_html=True
# )



# # ✅ 💡 🚀 강제적으로 기본 네비게이션 숨기기 (자동 생성되는 "year year year" 제거)
# st.markdown("""
#     <style>
#         section[data-testid="stSidebarNav"] {display: none !important;}
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # # 사이드바 제목
# # st.sidebar.title("연근 데이터")

# # # 버튼 없이 페이지 링크 추가
# # st.sidebar.page_link("pages/4year.py", label="4년근")
# # st.sidebar.page_link("pages/5year.py", label="5년근")
# # st.sidebar.page_link("pages/6year.py", label="6년근")


# # CSV 데이터 로드
# df = pd.read_csv('dangerousginseng_extended_2000_new.csv')

# # 불량 계산
# df['불량'] = df[['등외품', '재투입', '불량']].max(axis=1)

# # 주요 통계 계산
# total = len(df)
# abnormal = df['불량'].sum()
# normal = total - abnormal
# abnormal_rate = (abnormal / total) * 100

# # 메인 화면 수치 출력
# col1, col2, space1, col3, space2, col4, col5 = st.columns([0.6, 1, 0.2, 1, 0.2, 1, 0.6])
# with col2:
#     animate_number(total, "총합", "#E5F0D4")
# with col3:
#     animate_number(normal, "정상", "#D2E0FB")
# with col4:
#     animate_number(abnormal, "불량", "#FFC5C5")

# st.markdown("<br>", unsafe_allow_html=True)

# # 농가별 데이터 표시
# farm_summary = df.groupby(['농가 번호', '농가 명', '입고일자']).agg(
#     총합=('불량', 'count'), 정상=('불량', lambda x: (x == 0).sum()), 불량=('불량', 'sum')
# ).reset_index()

# selected_farm = st.selectbox("세부 데이터를 확인할 농가를 선택하세요", farm_summary['농가 명'].unique())
# st.session_state["selected_farm"] = selected_farm
# st.dataframe(farm_summary, use_container_width=True)

# import streamlit as st
# import pandas as pd
# import time
# from dash_utils import * 

# # Streamlit 애플리케이션 설정
# st.set_page_config(
#     page_title="AIoFarm 종합 모니터링 DashBoard",
#     layout="wide",
# )

# st.markdown(
#     """
#     <style>
#     .main {
#         background-color: #d14949;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # 색상 변경 
# green_colors = ["#A9C46C", "#809D3C", "#5D8736", "#5D8736"]
# # ["#327e54", "#0e7560", "#006a68", "#065f68", "#215363", "#2f4858"]

# # 상단 주요 통계 데이터
# st.markdown(
# """
# <div style="display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 10px; margin-bottom: 20px;">
# <img src="https://file.albamon.com/Albamon/Recruit/Photo/C-Photo-View?FN=2024/9/04/JK_CO_kflchq24090413552144.png" alt="AIoFarm" style="width: 60px; height: auto;">
# <h3 style="text-align: center; margin: 0;">AIoFarm 종합 모니터링</h3>
# </div>
# <br>
# """,
# unsafe_allow_html=True
# )



# hide_pages_style = """
#     <style>
#         section[data-testid="stSidebarNav"] ul {
#             display: none;
#         }
#     </style>
# """
# st.markdown(hide_pages_style, unsafe_allow_html=True)

# # # 사이드바 제목
# # st.sidebar.title("연근 데이터")




# # CSV 데이터 로드
# df = pd.read_csv('dangerousginseng_extended_2000_new.csv')

# # 불량 계산
# df['불량'] = df[['등외품', '재투입', '불량']].max(axis=1)

# # 주요 통계 계산
# total = len(df)
# abnormal = df['불량'].sum()
# normal = total - abnormal
# abnormal_rate = (abnormal / total) * 100

# # 메인 화면 수치 출력
# col1, col2, space1, col3, space2, col4, col5 = st.columns([0.6, 1, 0.2, 1, 0.2, 1, 0.6])
# with col2:
#     animate_number(total, "총합", "#f9f9f9")
# with col3:
#     animate_number(normal, "정상", "#E5F0D4")
# with col4:
#     animate_number(abnormal, "불량", "#FFC5C5")

# st.markdown("<br>", unsafe_allow_html=True)

# # 농가별 데이터 표시
# farm_summary = df.groupby(['농가 번호', '농가 명', '입고일자']).agg(
#     총합=('불량', 'count'), 정상=('불량', lambda x: (x == 0).sum()), 불량=('불량', 'sum')
# ).reset_index()

# selected_farm = st.selectbox("세부 데이터를 확인할 농가를 선택하세요", farm_summary['농가 명'].unique())
# st.session_state["selected_farm"] = selected_farm
# st.dataframe(farm_summary, use_container_width=True)

import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
from dash_utils import * 

# Streamlit 애플리케이션 설정
st.set_page_config(
    page_title="AIoFarm 종합 모니터링 DashBoard",
    layout="wide",
)

hide_pages_style = """
    <style>
        section[data-testid="stSidebarNav"] ul {
            display: none;
        }
    </style>
"""
st.markdown(hide_pages_style, unsafe_allow_html=True)

st.sidebar.title("📂 페이지 이동")

if st.sidebar.button("4년근 데이터"):
    st.switch_page("pages/1_4_years.py")

if st.sidebar.button("5년근 데이터"):
    st.switch_page("pages/2_5_years.py")

if st.sidebar.button("6년근 데이터"):
    st.switch_page("pages/3_6_years.py")

# 색상 변경 
green_colors = ["#A9C46C", "#809D3C", "#5D8736", "#5D8736"]
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
