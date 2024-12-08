# --- System Config ---

# --- Model Selection ---
OPENAI_GPT3 = "gpt-3.5-turbo"
OPENAI_GPT4 = "gpt-4"

# 单次读取评价条数上限
REVIEW_NUM_CAP = 300
OPENAI_CAP = 75

USER_POSITION = {
    "Not Selected", 
    "E-commerce Operations", 
    "Customer Service", 
    "Product R&D", 
    "Production/QC", 
    "Logistics/Supply Chain"
}
ANALYSIS_FOCUS = {
    "Not Selected", 
    "Product Features", 
    "Product Quality", 
    "Design & Appearance", 
    "User Experience", 
    "Pricing", 
    "Customer Service & Ordering", 
    "Packaging & Logistics"
}

# --- Container Config ---
CONTENT_COL_CONFIG = [1, 6, 1]