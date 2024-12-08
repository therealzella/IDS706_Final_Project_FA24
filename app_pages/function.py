import json
import streamlit as st
from services import analyze
from configs import OPENAI_GPT3, OPENAI_GPT4, REVIEW_NUM_CAP, OPENAI_CAP, ANALYSIS_FOCUS, USER_POSITION, CONTENT_COL_CONFIG
from services.filereader import FileReader

# --------------------------------------------------------------------------------
# ---- FUNCTION PAGE -------------------------------------------------------------
# --------------------------------------------------------------------------------

# multi-lingual JSON dictionary
with open('app_pages/function_lang.json', 'r', encoding='utf-8') as f:
    texts = json.load(f)

def show_function_page():
    head_color = "#166088"
    _, center, _ = st.columns(CONTENT_COL_CONFIG)

    with center:
        st.markdown(f"<h2 style='text-align: center; color: {head_color};'>{texts['center_subtitle1']}</h2>", unsafe_allow_html=True)
        step1_block = st.container()
        st.write("---")
        step2_block = st.container()
        st.write("---")
        step3_block = st.container()
        
        # --- STEP1: File Preperation Instruction ---
        with step1_block:
            
            st.markdown(f"<h4 style='color: {head_color};'>{texts['step_one']}</h4>", unsafe_allow_html=True)
            st.write(texts['step_one_subtitle'])

            review_download_instruction = st.expander(texts['step_one_instruction'])

            with review_download_instruction: 
                st.write(texts['step_one_write1'])
                st.image(image="assets/Compatible_Browswer_Extensions.png")
                st.write(texts['step_one_write2'])
                st.write(texts['step_one_write3'])

        # --- STEP2: File Upload and Validation Check ---
        with step2_block:
            st.markdown(f"<h4 style='color: {head_color};'>{texts['step_two_markdown']}</h4>", unsafe_allow_html=True)

            step2_col2, step2_col1 = st.columns((2, 4))

            with step2_col1: 
                uploaded_file = st.file_uploader(label=texts['step_two_uploaded'], type="xlsx")
                file = FileReader(uploaded_file)
                file_valid = file.check_file()

            with step2_col2: 
                st.markdown(texts['step_two_col2_markdown'])
                st.markdown(f"""<h6 style='color: grey; line-height: 2;'>
                    {texts['step_two_col2_markdown2']}</h6>
                    """, unsafe_allow_html=True)

            if uploaded_file is None:
                st.warning(texts['step_two_warning'])
            else:
                if file_valid:
                    review_texts, num_of_valid_reviews = file.df_to_text(num_of_reviews=REVIEW_NUM_CAP)
                    if num_of_valid_reviews > REVIEW_NUM_CAP: 
                        st.success(f"{texts['step_two_success1'].format(num_of_valid_reviews, REVIEW_NUM_CAP)}")
                    else: 
                        st.success(f"{texts['step_two_success2'].format(num_of_valid_reviews)}")

                    with st.expander(texts['step_two_expander']):
                        st.markdown(texts['step_two_with_markdown'])
                        st.markdown(review_texts)
                else:
                    st.error(texts['step_two_error'])

        # --- STEP3: Analysis Options ---
        with step3_block:
            st.markdown(f"<h4 style='color: {head_color};'>{texts['step_three_markdown']}</h4>", unsafe_allow_html=True)

            st.markdown(f"<h6>{texts['step_three_markdown2']}</h6>", unsafe_allow_html=True)
            step3a_col1, step3a_col2, step3a_col3 = st.columns((4, 2, 2))
            with step3a_col1:
                prod_info = st.text_input(texts['step_three_prod_info'], placeholder=texts['step_three_prod_info-placeholder'])
            with step3a_col2: 
                selected_focus = st.selectbox(texts['step_three_selected_focus'], ANALYSIS_FOCUS)
            with step3a_col3:
               selected_position = st.selectbox(texts['step_three_selected_position'], USER_POSITION)

            advanced_options = st.expander(texts['step_three_advanced_options'])

            with advanced_options: 
                st.markdown(f"<h6>{texts['step_three_advanced_options_markdown']}</h6>", unsafe_allow_html=True)
                input_question = st.text_input(texts['step_three_input_question'], placeholder=texts['step_three_input_question_placeholder'])
                
                step3b_col1, step3b_col2 = st.columns((1, 1))
                with step3b_col1: 
                    st.markdown(f"<h6>{texts['step_three_step3b_col1']}</h6>", unsafe_allow_html=True)
                step3c_col1, step3c_col2 = st.columns((1, 1))
                with step3c_col1: 
                    selected_model = st.selectbox(texts['step_three_selected_model'], [texts['step_three_selected_model2'], OPENAI_GPT3, OPENAI_GPT4])
            
        # --- Analysis Activation and Result ---
        if uploaded_file is not None and file_valid:
            if st.button(texts['step_three_button']):
                st.write("---")
                st.header(texts['step_three_header'])

                analyze_result = st.empty()
                
                with analyze_result:
                    st.markdown(texts['step_three_analyze_result'])

                    if selected_model == OPENAI_GPT3 or selected_model == OPENAI_GPT4: 
                        num_of_reviews_to_analyze = min(OPENAI_CAP, num_of_valid_reviews)
                        review_texts, _ = file.df_to_text(num_of_reviews=num_of_reviews_to_analyze)
                    else: 
                        num_of_reviews_to_analyze = min(REVIEW_NUM_CAP, num_of_valid_reviews)

                    prompt = analyze.generate_prompt(
                        prod_info, 
                        num_of_reviews_to_analyze, 
                        review_texts, 
                        selected_position, 
                        selected_focus,
                        input_question,
                        )
                    analyze.gpt_stream_completion(prompt, model=OPENAI_GPT3)
                        
                st.markdown(f"</br></br></br></br><p style='text-align: center; color: #BFBFBF; font-size: 16px;'> Powered by OpenAI {selected_model}</p>", unsafe_allow_html=True)