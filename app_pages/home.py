import streamlit as st

from configs import CONTENT_COL_CONFIG

# --------------------------------------------------------------------------------
# ---- HOME PAGE -----------------------------------------------------------------
# --------------------------------------------------------------------------------


def show_home_page():
    INSIGHTFUL_REVIEWS = "Review Analyzer"
    head_color = "#166088"

    _, center, _ = st.columns(CONTENT_COL_CONFIG)

    with center:
        st.markdown(
            f"<h1 style='color: black; font-size: 90px;'>{INSIGHTFUL_REVIEWS}</h1>",
            unsafe_allow_html=True,
        )
        st.write("---")

    # --- Feature 1: Time Saving ---
    st.markdown(
        f"""<h2 style='text-align: center; color: {head_color};'>
                {"Comprehensive Review Analysis in 30 Seconds"}</h2>
                """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""<h3 style='text-align: center; line-height: 2;'>
                {"Leveraging cutting-edge large language models ", 
                 "</br>Process up to 1000 product reviews in 30 seconds </br> ",
                   "Save 30-60 minutes of operation time daily"}</h3>
                """,
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns(CONTENT_COL_CONFIG)
    with center:
        st.markdown("---")

    # --- Feature 2: Tailored Insights ---
    st.markdown(
        f"""<h2 style='text-align: center; color: {head_color};'>
                {"Provide Customized Analysis Results Tailored to Your Needs"}</h2>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""<h3 style='text-align: center; line-height: 2;'>
            {"No matter you are in any position,"}</h3>
            """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""<h3 style='text-align: center; line-height: 2;'>
            {"or you are interested in any aspect,"}</h3>
            """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""<h3 style='text-align: center; line-height: 2;'>
            {"we provide you with customized analysis"}</h3>
            """,
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns(CONTENT_COL_CONFIG)
    with center:
        st.markdown("---")
