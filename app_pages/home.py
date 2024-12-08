import random
import time
import streamlit as st
from configs import ANALYSIS_FOCUS, CONTENT_COL_CONFIG, USER_POSITION
from style.color_theme import html_header_color_1
from utils.image_loader import img_to_bytes, img_to_html

# --------------------------------------------------------------------------------
# ---- HOME PAGE -----------------------------------------------------------------
# --------------------------------------------------------------------------------
 
def show_home_page():
    INSIGHTFUL_REVIEWS = "Review Analyzer"

    _, center, _ = st.columns(CONTENT_COL_CONFIG)

    with center: 
        st.markdown(f"<h1 style='color: black; font-size: 90px;'>{INSIGHTFUL_REVIEWS}</h1>", 
                         unsafe_allow_html=True)
        st.write("---")


    # --- Feature 1: Time Saving ---
    st.markdown(f"""<h2 style='text-align: center; color: {html_header_color_1};'>
                {"Comprehensive Review Analysis in 30 Seconds"}</h2>
                """, unsafe_allow_html=True)
    st.markdown(f"""<h3 style='text-align: center; line-height: 2;'>
                {"Leveraging cutting-edge large language models </br>Process up to 1000 product reviews in 30 seconds </br>Save 30-60 minutes of operation time daily"}</h3>
                """, unsafe_allow_html=True)

    _, center, _ = st.columns(CONTENT_COL_CONFIG)
    with center: 
        st.markdown("---")


    # --- Feature 2: Tailored Insights ---
    st.markdown(f"""<h2 style='text-align: center; color: {html_header_color_1};'>
                {"Provide Customized Analysis Results Tailored to Your Needs"}</h2>""", 
                unsafe_allow_html=True)
    st.markdown(f"""<h3 style='text-align: center; line-height: 2;'>
            {"No matter you are in any position,"}</h3>
            """, unsafe_allow_html=True)
    st.markdown(f"""<h3 style='text-align: center; line-height: 2;'>
            {"or you are interested in any aspect,"}</h3>
            """, unsafe_allow_html=True)
    st.markdown(f"""<h3 style='text-align: center; line-height: 2;'>
            {"we provide you with customized analysis"}</h3>
            """, unsafe_allow_html=True)
    # rolling_content = st.empty()
    # with rolling_content: 
    #     for i in range(8): 
    #         random_position = list(USER_POSITION)[random.randint(1, len(USER_POSITION) - 1)]
    #         random_focus = list(ANALYSIS_FOCUS)[random.randint(1, len(ANALYSIS_FOCUS) - 1)]
    #         position_focus_message = texts['position_and_focus'].format(random_position, random_focus)
    #         tailored_insights_final_message = texts['position_and_focus'].format("any position", "any aspect")
    #         st.markdown(f"""<h3 style='text-align: center; line-height: 2;'>
    #                     {position_focus_message}
    #                     </h3>""", unsafe_allow_html=True)
    #         time.sleep(0.4)
    #     st.markdown(f"""<h3 style='text-align: center; line-height: 2;'>
    #                 {tailored_insights_final_message}
    #                 </h3>""", unsafe_allow_html=True)

    _, center, _ = st.columns(CONTENT_COL_CONFIG)
    with center: 
        st.markdown("---")


    # --- Feature 3: Compatible with All Major EC Platforms ---
    # st.markdown(f"""<h2 style='text-align: center; color: {html_header_color_1};'>
    #             {texts['ecommerce_compatibility_subtitle']}</h2>
    #             """, unsafe_allow_html=True)
    # _, center, _ = st.columns(CONTENT_COL_CONFIG)
    # with center: 
    #     supported_ec_sites = img_to_bytes('assets/Supported_EC_Sites.png')
    #     st.markdown(f"""
    #         <div style="text-align: center;">
    #             <img src="data:image/png;base64,{supported_ec_sites}" style="width: 80%; max-width: 1500px;">
    #         </div>
    #         """, unsafe_allow_html=True)