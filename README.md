# IDS706 Fianl Project: Using Streamlit for E-commerce Review Analysis

## Description
The Review Analyzer is an **AI-powered** application designed to analyze e-commerce product reviews. Built using Streamlit, the app integrates OpenAI's GPT and Anthropic's Claude models to provide comprehensive insights, summaries, and actionable recommendations for product improvements. The tool is tailored for professionals in roles such as Product R&D, Customer Service, and E-commerce Operations, helping them better understand customer feedback and make informed decisions.

## Features

- **AI-Powered Analysis**:
  - Uses OpenAI and Anthropic APIs for natural language processing.
  - Analyzes and summarizes customer reviews into actionable insights.
- **Customizable Analysis**:
  - Users can specify focus areas, such as Product Quality, User Experience, Pricing, or ask specific questions.
- **Interactive User Interface**:
  - Built with Streamlit for ease of use and accessibility.
  - Includes a navigation menu for seamless exploration of features.
- **Dynamic Prompt Generation**:
  - Generates AI prompts based on user inputs, ensuring tailored and relevant results.

## Project Structure

```
.
├── app_pages
│   ├── home.py              # Home page logic
│   ├── function.py          # Main analysis page logic
│   ├── function_lang.json   # Language configurations for prompts
├── imgs                     # Image assets
├── services
│   ├── analyze.py           # AI analysis utility
│   ├── filereader.py        # File reading and preprocessing
├── app.py                   # Main application script
├── configs.py               # Configuration settings
├── requirements.txt         # List of dependencies
├── README.md                # Project documentation
└── .gitignore               # Git ignore file
```

## Installation

### Prerequisites
Python 3.8 or higher
API keys for OpenAI and Anthropic services

### Setup Instructions
1. Clone this repository:
```
git clone https://github.com/therealzella/IDS706_Final_Project_FA24.git
cd IDS706_Final_Project_FA24
```
2. Install required dependencies:
```
pip install -r requirements.txt
```
3. Create a .streamlit folder and add the secrets.toml file:
```
mkdir .streamlit
```
4. Add your API keys to the secrets.toml file:
```
[secrets]
OpenAI_API_KEY = "your_openai_api_key"
Anthropic_API_KEY = "your_anthropic_api_key"
```
### Usage
1. Run the following:
```
streamlit run app.py
```
2. Open the app in your browser at ```http://localhost:8501.```

3. Navigate through the application:
- **Home Page**: Explore introductory content.
- **Try Page**: Input product information, select focus areas, and analyze customer reviews.

### AI Pair Programming Tool Usage

The Review Analyzer relies heavily on AI tools for text analysis and insight generation:
- **OpenAI GPT Models**:
Used to process customer review data and generate human-like summaries, key findings, and recommendations.
- **Anthropic Claude Models**:
Provides additional natural language understanding capabilities for analyzing complex review datasets.
- **Custom Prompt Generation**:
Tailored prompts are generated dynamically to focus on specific user-defined aspects like Product Quality or User Experience.

These tools are integrated seamlessly into the backend of the application, with results displayed in markdown format for clarity.
