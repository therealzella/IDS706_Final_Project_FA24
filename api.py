import logging
import os
from io import BytesIO
from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from configs import OPENAI_GPT3
from services.analyze import generate_prompt, gpt_stream_completion
from services.filereader import FileReader

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("APIService")

# Load OpenAI API key from secrets
try:
    with open(".streamlit/secrets.toml", "r") as f:
        secrets = f.read()
        os.environ["OPENAI_API_KEY"] = secrets.split("=")[1].strip().strip('"')
    logger.info("OpenAI API key loaded successfully")
except Exception as e:
    logger.error(f"Error loading OpenAI API key: {str(e)}")
    raise

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
    logger.info("Health check endpoint accessed")
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
        logger.info(
            f"Received analysis request: product={prod_info}, user_position={user_position}, "
            f"analysis_focus={analysis_focus}, model={model}"
        )
        logger.info(f"Uploaded file: {file.filename} ({file.content_type})")

        # Read uploaded file
        contents = await file.read()
        file_object = BytesIO(contents)
        file_object.name = file.filename

        # Use existing FileReader to process file
        logger.info("Starting file processing...")
        file_reader = FileReader(file_object)
        if not file_reader.check_file():
            logger.warning("Invalid file format detected")
            raise HTTPException(status_code=400, detail="Invalid file format")

        # Get review texts
        review_texts, num_of_reviews = file_reader.df_to_text()
        logger.info(f"Extracted {num_of_reviews} reviews from file")

        # Generate analysis prompt
        logger.info("Generating analysis prompt...")
        prompt = generate_prompt(
            prod_info,
            num_of_reviews,
            review_texts,
            user_position,
            analysis_focus,
            input_question,
        )

        # Execute analysis
        logger.info("Starting GPT analysis...")
        result = gpt_stream_completion(prompt, model=model)

        logger.info("Analysis completed successfully")
        return {"status": "success", "result": result}

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """Provide basic service metrics"""
    logger.info("Metrics endpoint accessed")
    return {"service": "review_analyzer", "status": "running", "version": "1.0.0"}