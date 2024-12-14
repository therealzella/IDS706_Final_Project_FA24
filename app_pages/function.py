import json
import requests
import streamlit as st
from configs import (
    ANALYSIS_FOCUS,
    CONTENT_COL_CONFIG,
    OPENAI_GPT3,
    OPENAI_GPT4,
    REVIEW_NUM_CAP,
    USER_POSITION,
)
from services.filereader import FileReader

# API endpoint configuration
API_BASE_URL = "http://localhost:8000"  # Configure based on your deployment

# Load multi-lingual JSON dictionary
with open("app_pages/function_lang.json", "r", encoding="utf-8") as f:
    texts = json.load(f)


def show_function_page():
    """Display the main function page"""
    head_color = "#166088"
    _, center, _ = st.columns(CONTENT_COL_CONFIG)

    with center:
        title_html = (
            f"<h2 style='text-align: center; color: {head_color};'>"
            f"{texts['center_subtitle1']}</h2>"
        )
        st.markdown(title_html, unsafe_allow_html=True)

        step1_block = st.container()
        st.write("---")
        step2_block = st.container()
        st.write("---")
        step3_block = st.container()

        # --- STEP1: File Preparation Instruction ---
        with step1_block:
            step1_title = f"<h4 style='color: {head_color};'>{texts['step_one']}</h4>"
            st.markdown(step1_title, unsafe_allow_html=True)
            st.write(texts["step_one_subtitle"])

            review_download_instruction = st.expander(texts["step_one_instruction"])
            with review_download_instruction:
                st.write(texts["step_one_write1"])
                st.image(image="imgs/Compatible_Browswer_Extensions.png")
                st.write(texts["step_one_write2"])
                st.write(texts["step_one_write3"])

        # --- STEP2: File Upload and Validation Check ---
        with step2_block:
            step2_title = (
                f"<h4 style='color: {head_color};'>"
                f"{texts['step_two_markdown']}</h4>"
            )
            st.markdown(step2_title, unsafe_allow_html=True)

            step2_col2, step2_col1 = st.columns((2, 4))

            with step2_col1:
                uploaded_file = st.file_uploader(
                    label=texts["step_two_uploaded"], type="xlsx"
                )
                file = FileReader(uploaded_file)
                file_valid = file.check_file() if uploaded_file else False

            with step2_col2:
                st.markdown(texts["step_two_col2_markdown"])
                markdown2_style = """<h6 style='color: grey; line-height: 2;'>
                    {}</h6>""".format(
                    texts["step_two_col2_markdown2"]
                )
                st.markdown(markdown2_style, unsafe_allow_html=True)

            if uploaded_file is None:
                st.warning(texts["step_two_warning"])
            else:
                if file_valid:
                    review_texts, num_of_valid_reviews = file.df_to_text(
                        num_of_reviews=REVIEW_NUM_CAP
                    )
                    if num_of_valid_reviews > REVIEW_NUM_CAP:
                        success_msg = texts["step_two_success1"].format(
                            num_of_valid_reviews, REVIEW_NUM_CAP
                        )
                        st.success(success_msg)
                    else:
                        success_msg = texts["step_two_success2"].format(
                            num_of_valid_reviews
                        )
                        st.success(success_msg)

                    with st.expander(texts["step_two_expander"]):
                        st.markdown(texts["step_two_with_markdown"])
                        st.markdown(review_texts)
                else:
                    st.error(texts["step_two_error"])

        # --- STEP3: Analysis Options ---
        with step3_block:
            step3_title = (
                f"<h4 style='color: {head_color};'>"
                f"{texts['step_three_markdown']}</h4>"
            )
            st.markdown(step3_title, unsafe_allow_html=True)
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

                step3b_col1, step3b_col2 = st.columns((1, 1))
                with step3b_col1:
                    st.markdown(
                        f"<h6>{texts['step_three_step3b_col1']}</h6>",
                        unsafe_allow_html=True,
                    )
                step3c_col1, step3c_col2 = st.columns((1, 1))
                with step3c_col1:
                    model_options = [
                        texts["step_three_selected_model2"],
                        OPENAI_GPT3,
                        OPENAI_GPT4,
                    ]
                    selected_model = st.selectbox(
                        texts["step_three_selected_model"], model_options
                    )

        # --- Analysis Activation and Result ---
        if uploaded_file is not None and file_valid:
            if st.button(texts["step_three_button"]):
                st.write("---")
                st.header(texts["step_three_header"])

                analyze_result = st.empty()

                with analyze_result:
                    st.markdown(texts["step_three_analyze_result"])

                    try:
                        # Make API request
                        file_data = {
                            "file": (
                                "file.xlsx",
                                uploaded_file.getvalue(),
                                "application/vnd.openxmlformats-officedocument."
                                "spreadsheetml.sheet",
                            )
                        }
                        request_data = {
                            "prod_info": prod_info,
                            "user_position": selected_position,
                            "analysis_focus": selected_focus,
                            "input_question": input_question,
                            "model": selected_model,
                        }

                        response = requests.post(
                            f"{API_BASE_URL}/analyze",
                            files=file_data,
                            data=request_data,
                        )

                        if response.status_code == 200:
                            st.markdown(response.json()["result"])
                        else:
                            error_msg = response.json().get(
                                "detail", "Unknown error occurred"
                            )
                            st.error(f"Error: {error_msg}")

                    except Exception as e:
                        error_msg = f"Error connecting to analysis service: {str(e)}"
                        st.error(error_msg)

                if selected_model in [OPENAI_GPT3, OPENAI_GPT4]:
                    footer = (
                        f"</br></br></br></br><p style='text-align: center; "
                        f"color: #BFBFBF; font-size: 16px;'> "
                        f"Powered by OpenAI {selected_model}</p>"
                    )
                    st.markdown(footer, unsafe_allow_html=True)
