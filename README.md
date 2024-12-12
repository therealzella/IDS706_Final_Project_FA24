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

## Architecture Diagram
Below is the architecture diagram of the app in this repository
![Screenshot](Screenshot%202024-12-11%20at%2002.25.27.png)

## Quantitative Assessment: Load Testing Report
### Objective
This project aims to evaluate the performance, reliability, and scalability of the target system under varying loads using two different load-testing approaches:

- Python-Based Load Testing: Simulating 1,000 and 10,000 requests.
- k6 Load Testing: Simulating up to 10,000 virtual users (VUs) in a staged test.

### Methodology
### Python-Based Load Testing

- **Tool Used**: Python script with `ThreadPoolExecutor` for concurrency.
- **Test Scenarios**:
  - 1,000 Requests Test
  - 10,000 Requests Test
- **Metrics Collected**:
  - Success Rate
  - Total Time Elapsed
  - Requests per Second
  - Average Latency (Response Time)


### `k6` Load Testing

- **Tool Used**: `k6` load testing framework.
- **Test Scenarios**:
  - Load simulated across four stages:
    1. Ramp-up to 1,000 VUs in 1 minute.
    2. Sustained load with 5,000 VUs for 2 minutes.
    3. High load with 10,000 VUs for 2 minutes.
    4. Ramp-down to 0 VUs in 1 minute.
- **Metrics Collected**:
  - HTTP Timing Metrics (e.g., request duration, waiting, sending, receiving times)
  - Data Transferred
  - Virtual User Utilization
  - Percentile-Based Latency Analysis (P90, P95)

## Results

### Python-Based Load Testing

#### **1,000 Requests Test**
- **Success Rate:** 100.0%
- **Requests per Second:** 195.08
- **Average Latency:** 0.05 seconds

This test demonstrated strong reliability and efficiency, showing the system's ability to handle a moderate load with minimal latency.

#### **10,000 Requests Test**
- **Success Rate:** 99.2%
- **Requests per Second:** 76.65
- **Average Latency:** 0.05 seconds

Under this heavier load, the system exhibited slight scalability limitations, with 82 failed requests and reduced throughput.

### `k6` Load Testing

#### **Key Metrics at Peak Load (10,000 VUs):**

- **HTTP Request Duration**:
  - **Average:** 174ms
  - **Maximum:** 607ms
  - **P95:** 389ms
- **Success Rate:** 100% (all responses returned status code 200)
- **Data Transferred**:
  - **Received:** 1.1GB
  - **Sent:** 102MB

The system handled up to 10,000 VUs without any request failures. However, increased latency during high loads indicates areas for optimization.

## Insights

1. **Performance Consistency**
   - Both tests demonstrated high success rates at moderate loads, confirming the system's reliability.
   - Under higher loads, Python-based testing highlighted a few failures, while `k6` metrics revealed increased latencies.

2. **Scalability**
   - Python-based testing showed slight performance degradation with 10,000 requests, while `k6` testing demonstrated the system's ability to handle up to 10,000 VUs with increased response times.

3. **Bottleneck Identification**
   - Increased latency and reduced throughput under higher loads indicate potential resource constraints, particularly in handling concurrent requests.

## Recommendations

1. **Optimize Latency**:
   - Address high-latency outliers by optimizing database queries, API response payloads, or server-side processing.
   - Implement caching for frequently requested data.

2. **Improve Scalability**:
   - Use load balancing to distribute traffic across multiple servers.
   - Scale horizontally by adding more instances during peak loads.

3. **Enable TLS**:
   - Integrate HTTPS to enhance security, as `k6` metrics showed no TLS handshaking.

4. **Monitor Resource Usage**:
   - Employ server-side monitoring tools to identify bottlenecks (CPU, memory, I/O) during high load tests.


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
