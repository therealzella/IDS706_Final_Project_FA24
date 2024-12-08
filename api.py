import json
import logging
import os
from io import BytesIO
from typing import Optional

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from configs import OPENAI_GPT3  # Add this import
# Import existing analysis modules
from services.analyze import generate_prompt, gpt_stream_completion
from services.filereader import FileReader

# Load OpenAI API key from streamlit secrets
try:
    with open(".streamlit/secrets.toml", "r") as f:
        secrets = f.read()
        os.environ["OPENAI_API_KEY"] = secrets.split("=")[1].strip().strip('"')
except Exception as e:
    logging.error(f"Error loading OpenAI API key: {str(e)}")
    raise

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Review Analysis Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalysisRequest(BaseModel):
    prod_info: str
    user_position: str = "Not Selected"
    analysis_focus: str = "Not Selected"
    input_question: Optional[str] = None


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/analyze")
async def analyze_reviews(
    file: UploadFile = File(...),
    prod_info: str = None,
    user_position: str = "Not Selected",
    analysis_focus: str = "Not Selected",
    input_question: Optional[str] = None,
    model: str = OPENAI_GPT3,
):
    """Process review analysis requests"""
    try:
        logger.info(f"Received analysis request for product: {prod_info}")

        # Read uploaded file
        contents = await file.read()
        file_object = BytesIO(contents)
        file_object.name = file.filename

        # Use existing FileReader to process file
        file_reader = FileReader(file_object)
        if not file_reader.check_file():
            raise HTTPException(status_code=400, detail="Invalid file format")

        # Get review texts
        review_texts, num_of_reviews = file_reader.df_to_text()

        # Generate analysis prompt
        prompt = generate_prompt(
            prod_info,
            num_of_reviews,
            review_texts,
            user_position,
            analysis_focus,
            input_question,
        )

        # Execute analysis
        result = gpt_stream_completion(prompt, model=model)

        logger.info("Analysis completed successfully")
        return {"status": "success", "result": result}

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """Provide basic service metrics"""
    return {"service": "review_analyzer", "status": "running", "version": "1.0.0"}
