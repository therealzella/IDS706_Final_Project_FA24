import os
import openai
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import streamlit as st
from configs import OPENAI_GPT3, OPENAI_GPT4

# --- OpenAI Stream Completion ---
openai.api_key = st.secrets["OpenAI_API_KEY"]

def gpt_stream_completion(prompt, model=OPENAI_GPT3):
    system_prompt, user_prompt = prompt[0], prompt[1]
    messages = [
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": user_prompt}, 
        ]
    
    stream = openai.ChatCompletion.create(
        model=model, 
        messages=messages, 
        temperature=0,
        stream=True)
    
    completing_content = ""
    for chunk in stream:
        chunk_content = chunk["choices"][0].get("delta", {}).get("content")
        if chunk_content: 
            completing_content += chunk_content
            st.markdown(completing_content)
    
    return


# --- Prompt Generation ---
def generate_prompt(prod_info, num_of_reviews, review_texts, user_position, analysis_focus, input_question):
    common_prompt_part1 = f"""
    As a senior e-commerce review analyst, your role is to evaluate the latest {num_of_reviews} reviews for the {prod_info} product on an e-commerce platform.\n
    Please focus on the following aspects in your analysis:
    """

    common_prompt_part2 = """
    2. Your analysis should cover the following points:
      a. A concise summary paragraph highlighting the key findings;
      b. A detailed discussion of each key finding, with in-depth analysis;
      c. Actionable recommendations for improvement based on your findings, to be included at the conclusion.\n
    Only refer to specific customer reviews as evidence for key findings when necessary, and ensure to include the review date.\n
    3. Please present your analysis using markdown syntax.
    """

    focus_to_prompt = {
        "Product Features": "Reviews focusing on the product's key functions, the practicality of those functions, and customer reactions to them.",
        "Product Quality": "Reviews addressing product quality aspects, such as durability, consistency, and overall customer feedback regarding its quality.",
        "Design & Appearance": "Reviews about the product's design elements, including aesthetics, color, shape, size, and customer opinions on its visual appeal.",
        "User Experience": "Reviews detailing the user experience, covering ease of use, comfort, and any issues faced by customers during usage.",
        "Pricing": "Reviews discussing the product's pricing, including whether the price is justified, comparisons to the product’s value, and customer opinions on the cost.",
        "Customer Service & Ordering": "Reviews concerning customer service, such as responsiveness, professionalism, service quality, and the ease of the ordering process, alongside other related feedback.",
        "Packaging & Logistics": "Reviews focused on packaging and logistics, including packaging integrity, design, delivery speed, and customer feedback on these aspects.",
    }

    position_to_prompt = {
        "E-commerce Operations": "As an e-commerce operations manager, focus on factors influencing sales and customer satisfaction, such as product popularity, sales strategies, pricing, the ordering experience, and customer feedback.",
        "Customer Service": "As a customer service manager, concentrate on aspects like the response time of online support, service quality, professionalism, and ease of the ordering process, excluding any comments unrelated to customer service or the ordering experience.",
        "Product R&D": "As a product R&D manager, focus on customer feedback related to product functionality, design, user experience, and areas for product improvement, providing a comprehensive summary. Exclude comments unrelated to the product or user experience.",
        "Production/QC": "As a production and quality control manager, focus on customer feedback related to product quality, including quality issues, defects, and other relevant concerns.",
        "Logistics/Supply Chain": "As a logistics and supply chain manager, focus on customer feedback related to packaging and delivery, such as packaging integrity, delivery speed, and overall logistics experience. Exclude any comments unrelated to logistics or packaging."
    }

    if input_question: 
        # Generate prompt based on the specific question the user has asked
        system_prompt = f"""
        You are an experienced e-commerce review analyst.
        Your task is to evaluate the most recent {num_of_reviews} reviews for the {prod_info} product on the Taobao platform.\n
        Using the content of customer reviews, please answer the following question: {input_question}
        """
    else: 
        # Generate prompt based on the user’s position and area of interest (focus analysis)
        # If both position and focus analysis are selected, prioritize the focus analysis
        if analysis_focus != "Not Selected":
            system_prompt = common_prompt_part1 + \
                """1. The analysis should focus specifically on: a. Filtering out customer comments related to """ + focus_to_prompt[analysis_focus] + \
                """ b. Analyzing and summarizing the filtered content in detail.\n""" + common_prompt_part2
        elif user_position != "Not Selected":
            system_prompt = common_prompt_part1 + "1. The analysis should be focused solely on the perspective of " + position_to_prompt[user_position] + common_prompt_part2
        else:
            system_prompt = common_prompt_part1 + """1. Please categorize and analyze the customer reviews from various perspectives, including the main strengths and weaknesses of the product, its functionality, design, user experience, pricing, packaging, customer service, product quality, and any other customer concerns.""" + common_prompt_part2

    user_prompt = f"\nList of reviews:\n```{review_texts}```"
    complete_prompt = system_prompt + user_prompt

    return [system_prompt, user_prompt, complete_prompt]
