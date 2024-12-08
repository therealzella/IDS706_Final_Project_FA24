from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from typing import Optional
import io

from analyzer.analyze import generate_prompt, gpt_stream_completion
from utils.file_reader import FileReader
from configs import REVIEW_NUM_CAP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    prod_info: str
    user_position: str
    analysis_focus: str
    input_question: Optional[str] = None

@app.post("/api/analyze")
async def analyze_reviews(
    prod_info: str,
    user_position: str,
    analysis_focus: str,
    input_question: Optional[str] = None,
    file: UploadFile = File(...)
):
    logger.info(f"Received analysis request for product: {prod_info}")
    
    try:
        # Convert UploadFile to BytesIO
        contents = await file.read()
        file_obj = io.BytesIO(contents)
        file_obj.name = file.filename  # Add name attribute for pandas
        
        # Read and validate file
        file_reader = FileReader(file_obj)
        if not file_reader.check_file():
            raise HTTPException(status_code=400, detail="Invalid file format")
            
        # Process reviews
        review_texts, num_of_valid_reviews = file_reader.df_to_text(num_of_reviews=REVIEW_NUM_CAP)
        logger.info(f"Successfully processed {num_of_valid_reviews} reviews")
        
        # Generate analysis
        prompt = generate_prompt(
            prod_info,
            num_of_valid_reviews,
            review_texts,
            user_position,
            analysis_focus,
            input_question
        )
        
        # Get GPT analysis
        analysis = gpt_stream_completion(prompt)
        
        return {"status": "success", "analysis": analysis}
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)