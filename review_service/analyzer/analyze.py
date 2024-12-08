import os
import logging
from typing import List
import json
from pathlib import Path
from openai import OpenAI

# Configure logging
logger = logging.getLogger(__name__)

def get_openai_api_key():
    """Get OpenAI API key from secrets.toml"""
    try:
        root_dir = Path(__file__).resolve().parents[2]
        secrets_path = root_dir / '.streamlit' / 'secrets.toml'
        
        if not secrets_path.exists():
            raise FileNotFoundError(f"Secrets file not found at {secrets_path}")
        
        with open(secrets_path, 'r') as f:
            for line in f:
                if line.startswith('OpenAI_API_KEY'):
                    key = line.split('=')[1].strip().strip('"\'')
                    return key
        
        raise KeyError("OpenAI_API_KEY not found in secrets.toml")
    except Exception as e:
        logger.error(f"Failed to get OpenAI API key: {str(e)}")
        raise

def gpt_stream_completion(prompt: List[str]) -> str:
    """
    Get completion from GPT model using the new OpenAI API
    Returns the full response text
    """
    system_prompt, user_prompt = prompt[0], prompt[1]
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=get_openai_api_key())
            
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in GPT completion: {str(e)}")
        raise

# --- Prompt Generation ---
def generate_prompt(prod_info, num_of_reviews, review_texts, user_position, analysis_focus, input_question):
    common_prompt_part1 = f"""
    You are a senior e-commerce review analyst.
    Your task is to analyze the most recent {num_of_reviews} product reviews for this {prod_info} product on an Ecommerce platform.\n
    Points to follow in the analysis:
    """

    common_prompt_part2 = """
    2. Your analysis should include:
      a. Key findings, concisely listed in a summary paragraph;
      b. Detailed analysis, discussing each key finding in depth;
      c. Recommendations for improvement, based on your findings, to be presented at the end of the analysis.\n
    Only provide specific customer review content as evidence for key findings when necessary, and include the date of the review.\n
    3. Please use markdown syntax to present your analysis results.
    """
    
    focus_to_prompt = {
        "Product Features": "Comments related to product functional features, such as the main functions, practicality of these functions, and customer reactions to them.",
        "Product Quality": "Comments related to product quality issues, such as durability, consistency, and customer feedback on product quality.",
        "Design & Appearance": "Comments related to product design, such as aesthetics, color, shape, size, and customer feedback on the design.",
        "User Experience": "Comments related to the user experience, such as ease of use, comfort, and problems encountered by customers during use.",
        "Pricing": "Comments related to the product's price, such as whether the price is reasonable, how it compares to the product's value, and customer feedback on the price.",
        "Customer Service & Ordering": "Comments related to customer service, such as the responsiveness of online service personnel, service quality, professionalism, and convenience of the ordering process, along with other customer feedback.",
        "Packaging & Logistics": "Comments related to packaging and logistics issues, such as whether the product's packaging is intact, the design of the packaging, delivery speed, and customer feedback on packaging and delivery.",
    }

    position_to_prompt = {
        "E-commerce Operations": "an e-commerce operations manager, focusing on factors that might affect sales volumes and customer satisfaction, such as product popularity, sales strategies, ordering experience, pricing, as well as customer feedback and suggestions.",
        "Customer Service": "a customer service manager, focusing on aspects such as response speed of online customer service personnel, service quality, professionalism, and the convenience of the ordering process, along with other customer feedback. Avoid summarizing any comments unrelated to customer service or the ordering experience.",
        "Product R&D": "a product R&D manager, focusing on customer feedback regarding product functions and design, such as functionality, user experience, and product improvement needs, providing a comprehensive summary. Avoid summarizing any comments unrelated to the product and user experience.",
        "Production/QC": "a production and quality control department manager, with a focus on customer feedback related to product quality, such as quality issues and defects.",
        "Logistics/Supply Chain": "a logistics and supply chain department manager, focusing on customer feedback regarding product packaging and delivery, such as packaging and logistics issues, delivery speed, and overall logistics experience. Avoid summarizing any comments unrelated to logistics or packaging.",
    }

    if input_question: 
        # generate prompt according to the specific question the user has asked
        system_prompt = f"""
        You are a seasoned e-commerce review analyst.
        Your task is to analyze the most recent {num_of_reviews} product reviews for this {prod_info} product on the Taobao platform.\n
        And through the content of customer reviews, answer the following question: {input_question}
        """
    else: 
        # generate prompt according to the user position and area of interest (focus analysis)
        # if both user position and focus analysis are selected by the user, generate prompt based on focus analysis
        if analysis_focus != "Not Selected":
            system_prompt = common_prompt_part1 \
                + """1. The analysis should not be comprehensive but should focus on: a. Firstly, filter out customer comments related to """ + focus_to_prompt[analysis_focus] \
                + "b. Then analyze and summarize the filtered content in detail.\n" + common_prompt_part2
        elif user_position != "Not Selected":
            system_prompt = common_prompt_part1 + "1. The analysis should not be comprehensive, please analyze solely from the perspective of " + position_to_prompt[user_position] + common_prompt_part2
        else:
            system_prompt = common_prompt_part1 + "1. Please categorize and analyze the customer reviews from different perspectives comprehensively, such as the main advantages and disadvantages of the product, its functions, design, user experience, pricing, packaging, customer service, quality of the product, and any other issues raised by customers." + common_prompt_part2

    user_prompt = f"\nList of reviews:\n```{review_texts}```"
    complete_prompt = system_prompt + user_prompt

    return [system_prompt, user_prompt, complete_prompt]
