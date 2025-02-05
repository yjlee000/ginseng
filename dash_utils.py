import time
import streamlit as st

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

###################################################
    
# def animate_number(value, key, background_color, duration=2, suffix="", decimal_places=0, link=None):
#     value = float(value)  # float로 변환하여 소수점 처리 가능하게 함
#     step = max(1, int(value) // (duration * 10))
#     placeholder = st.empty()
    
#     for i in range(0, int(value) + step, step):
#         formatted_value = f"{i:,.{decimal_places}f}"  # 소수점 자리수를 적용
#         placeholder.markdown(
#             f"""
#             <a href="{link}" target="_self" style="text-decoration: none;">
#                 <div style="border: none; border-radius: 10px; padding: 20px; text-align: center; background-color: {background_color};">
#                     <div style="font-size: 18px; font-weight: bold; color: #666;">{key}</div>
#                     <div style="font-size: 32px; font-weight: bold; color: #333;">{formatted_value}{suffix}</div>
#                 </div>
#             </a>
#             """,
#             unsafe_allow_html=True,
#         )
#         time.sleep(0.02)
        
#     formatted_value = f"{value:,.{decimal_places}f}"
#     placeholder.markdown(
#         f"""
#         <a href="{link}" target="_self" style="text-decoration: none;">
#             <div style="border: 2px solid #ccc; border-radius: 10px; padding: 20px; text-align: center; background-color: {background_color};">
#                 <div style="font-size: 18px; font-weight: bold; color: #666;">{key}</div>
#                 <div style="font-size: 32px; font-weight: bold; color: #333;">{formatted_value}{suffix}</div>
#             </div>
#         </a>
#         """,
#         unsafe_allow_html=True,
#     )
#     st.session_state.total_animated = True  # 애니메이션이 한 번만 실행되도록 설정

###############################################

# import time
# import streamlit as st

# def animate_number(value, key, background_color, duration=2, suffix="", decimal_places=0, link=None):
#     value = float(value)  # float로 변환하여 소수점 처리 가능하게 함
#     step = max(1, int(value) // (duration * 10))
#     placeholder = st.empty()

#     for i in range(0, int(value) + step, step):
#         formatted_value = f"{i:,.{decimal_places}f}"  # 소수점 자리수를 적용
#         placeholder.markdown(
#             f"""
#             <div style="border: none; border-radius: 10px; padding: 20px; text-align: center; background-color: {background_color}; cursor: pointer;"
#                  onclick="window.location.href='{link}'">
#                 <div style="font-size: 18px; font-weight: bold; color: #666;">{key}</div>
#                 <div style="font-size: 32px; font-weight: bold; color: #333;">{formatted_value}{suffix}</div>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )
#         time.sleep(0.02)

#     # 애니메이션이 끝난 후, 링크를 다시 생성하지 않도록 처리
#     if link:
#         formatted_value = f"{value:,.{decimal_places}f}"
#         placeholder.markdown(
#             f"""
#             <a href="{link}" target="_self" style="text-decoration: none;">
#                 <div style="border: 2px solid #ccc; border-radius: 10px; padding: 20px; text-align: center; background-color: {background_color}; cursor: pointer;">
#                     <div style="font-size: 18px; font-weight: bold; color: #666;">{key}</div>
#                     <div style="font-size: 32px; font-weight: bold; color: #333;">{formatted_value}{suffix}</div>
#                 </div>
#             </a>
#             """,
#             unsafe_allow_html=True,
#         )

#     st.session_state.total_animated = True  # 애니메이션이 한 번만 실행되도록 설정
