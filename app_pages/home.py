import random
import time
import json
import streamlit as st
from configs import ANALYSIS_FOCUS, CONTENT_COL_CONFIG, USER_POSITION
from style.color_theme import html_header_color_1
from utils.image_loader import img_to_bytes, img_to_html

# --------------------------------------------------------------------------------
# ---- HOME PAGE -----------------------------------------------------------------
# --------------------------------------------------------------------------------

# multi-lingual JSON dictionary
with open('app_pages/home_lang.json', 'r', encoding='utf-8') as f:
    texts = json.load(f)
 
def show_home_page(language):

    INSIGHTFUL_REVIEWS = texts['insightful_reviews']
    INSIGHTFUL_REVIEWS = "Review Analyzer"

    _, center, _ = st.columns(CONTENT_COL_CONFIG)

    with center: 
        st.markdown(f"<h1 style='color: black; font-size: 90px;'>{INSIGHTFUL_REVIEWS}</h1>", 
                         unsafe_allow_html=True)
        st.write("---")


    # --- Feature 1: Time Saving ---
    st.markdown(f"""<h2 style='text-align: center; color: {html_header_color_1};'>
                {texts['time_saving_subtitle'][language]}</h2>
                """, unsafe_allow_html=True)
    st.markdown(f"""<h3 style='text-align: center; line-height: 2;'>
                {texts['time_saving_description'][language]}</h3>
                """, unsafe_allow_html=True)

    _, center, _ = st.columns(CONTENT_COL_CONFIG)
    with center: 
        st.markdown("---")


    # --- Feature 2: Tailored Insights ---
    st.markdown(f"""<h2 style='text-align: center; color: {html_header_color_1};'>
                {texts['tailored_insights_subtitle'][language]}</h2>""", 
                unsafe_allow_html=True)
    rolling_content = st.empty()
    with rolling_content: 
        for i in range(8): 
            random_position = USER_POSITION[language][random.randint(1, len(USER_POSITION[language]) - 1)]
            random_focus = ANALYSIS_FOCUS[language][random.randint(1, len(ANALYSIS_FOCUS[language]) - 1)]
            position_focus_message = texts['position_and_focus'][language].format(random_position, random_focus)
            tailored_insights_final_message = {
                "en": texts['position_and_focus'][language].format("👩🏻‍🚀any position", "🌟any aspect")
            }
            st.markdown(f"""<h3 style='text-align: center; line-height: 2;'>
                        {position_focus_message}
                        </h3>""", unsafe_allow_html=True)
            time.sleep(0.4)
        st.markdown(f"""<h3 style='text-align: center; line-height: 2;'>
                    {tailored_insights_final_message[language]}
                    </h3>""", unsafe_allow_html=True)

    _, center, _ = st.columns(CONTENT_COL_CONFIG)
    with center: 
        st.markdown("---")


    # --- Feature 3: Compatible with All Major EC Platforms ---
    st.markdown(f"""<h2 style='text-align: center; color: {html_header_color_1};'>
                {texts['ecommerce_compatibility_subtitle'][language]}</h2>
                """, unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: grey;'>Development in Progress</h6>", unsafe_allow_html=True)
    _, center, _ = st.columns(CONTENT_COL_CONFIG)
    with center: 
        supported_ec_sites = img_to_bytes('assets/Supported_EC_Sites.png')
        st.markdown(f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{supported_ec_sites}" style="width: 80%; max-width: 1500px;">
            </div>
            """, unsafe_allow_html=True)