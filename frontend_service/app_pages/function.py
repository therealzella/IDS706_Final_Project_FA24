import json
import streamlit as st
import requests
from configs import ANALYSIS_FOCUS, USER_POSITION, CONTENT_COL_CONFIG, BACKEND_URL

try:
    with open("app_pages/function_lang.json", "r", encoding="utf-8") as f:
        texts = json.load(f)
except FileNotFoundError:
    with open("function_lang.json", "r", encoding="utf-8") as f:
        texts = json.load(f)


def show_function_page():
    head_color = "#166088"
    _, center, _ = st.columns(CONTENT_COL_CONFIG)

    with center:
        st.markdown(
            f"<h2 style='text-align: center; color: {head_color};'>{texts['center_subtitle1']}</h2>",
            unsafe_allow_html=True,
        )
        step1_block = st.container()
        st.write("---")
        step2_block = st.container()
        st.write("---")
        step3_block = st.container()

        # --- STEP1: File Preperation Instruction ---
        with step1_block:
            st.markdown(
                f"<h4 style='color: {head_color};'>{texts['step_one']}</h4>",
                unsafe_allow_html=True,
            )
            st.write(texts["step_one_subtitle"])

            review_download_instruction = st.expander(texts["step_one_instruction"])
            with review_download_instruction:
                st.write(texts["step_one_write1"])
                st.write(texts["step_one_write2"])
                st.write(texts["step_one_write3"])

        # --- STEP2: File Upload and Validation Check ---
        with step2_block:
            st.markdown(
                f"<h4 style='color: {head_color};'>{texts['step_two_markdown']}</h4>",
                unsafe_allow_html=True,
            )

            step2_col2, step2_col1 = st.columns((2, 4))

            with step2_col1:
                uploaded_file = st.file_uploader(
                    label=texts["step_two_uploaded"], type="xlsx"
                )

            with step2_col2:
                st.markdown(texts["step_two_col2_markdown"])
                st.markdown(texts["step_two_col2_markdown2"], unsafe_allow_html=True)

            if uploaded_file is None:
                st.warning(texts["step_two_warning"])

        # --- STEP3: Analysis Options ---
        with step3_block:
            st.markdown(
                f"<h4 style='color: {head_color};'>{texts['step_three_markdown']}</h4>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<h6>{texts['step_three_markdown2']}</h6>", unsafe_allow_html=True
            )

            step3a_col1, step3a_col2, step3a_col3 = st.columns((4, 2, 2))
            with step3a_col1:
                prod_info = st.text_input(
                    texts["step_three_prod_info"],
                    placeholder=texts["step_three_prod_info-placeholder"],
                )
            with step3a_col2:
                selected_focus = st.selectbox(
                    texts["step_three_selected_focus"], ANALYSIS_FOCUS
                )
            with step3a_col3:
                selected_position = st.selectbox(
                    texts["step_three_selected_position"], USER_POSITION
                )

            advanced_options = st.expander(texts["step_three_advanced_options"])
            with advanced_options:
                st.markdown(
                    f"<h6>{texts['step_three_advanced_options_markdown']}</h6>",
                    unsafe_allow_html=True,
                )
                input_question = st.text_input(
                    texts["step_three_input_question"],
                    placeholder=texts["step_three_input_question_placeholder"],
                )

        # --- Analysis Activation and Result ---
        if uploaded_file is not None:
            if st.button(texts["step_three_button"]):
                st.write("---")
                st.header(texts["step_three_header"])

                analyze_result = st.empty()
                with analyze_result:
                    st.markdown(texts["step_three_analyze_result"])

                    try:
                        # Make request to review service
                        files = {
                            "file": (
                                "file.xlsx",
                                uploaded_file.getvalue(),
                                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            )
                        }
                        params = {
                            "prod_info": prod_info,
                            "user_position": selected_position,
                            "analysis_focus": selected_focus,
                            "input_question": input_question,
                        }

                        response = requests.post(
                            f"{BACKEND_URL}/api/analyze",
                            params=params,
                            files=files,
                            timeout=30,
                        )

                        if response.status_code == 200:
                            analysis_result = response.json()
                            st.markdown(analysis_result["analysis"])
                        else:
                            st.error(f"Analysis failed: {response.json()['detail']}")

                    except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to backend service: {str(e)}")
                    except Exception as e:
                        st.error(f"Error occurred: {str(e)}")
