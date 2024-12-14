import logging
from io import BytesIO
from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from configs import OPENAI_GPT3

# Import existing analysis modules
from services.analyze import generate_prompt, gpt_stream_completion
from services.filereader import FileReader

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("APIService")

app = FastAPI(title="Review Analysis Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        # Read uploaded file
        try:
            contents = await file.read()
            file_object = BytesIO(contents)
            file_object.name = file.filename
        except Exception as e:
            logger.error(f"Error reading file: {str(e)}")
            raise HTTPException(status_code=400, detail="Error reading uploaded file")

        # Use existing FileReader to process file
        file_reader = FileReader(file_object)
        if not file_reader.check_file():
            logger.warning("Invalid file format detected")
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid file format. Please upload an Excel file with the "
                    "required columns."
                ),
            )

        # Get review texts
        try:
            review_texts, num_of_reviews = file_reader.df_to_text()
        except Exception as e:
            logger.error(f"Error processing file content: {str(e)}")
            raise HTTPException(status_code=400, detail="Error processing file content")

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
        try:
            result = gpt_stream_completion(prompt, model=model)
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}")
            raise HTTPException(status_code=500, detail="Error during analysis process")

        logger.info("Analysis completed successfully")
        return {"status": "success", "result": result}

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """Provide basic service metrics"""
    return {"service": "review_analyzer", "status": "running", "version": "1.0.0"}
