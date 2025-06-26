from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

from whisper_utils import transcribe_audio
from llama3_utils import generate_report
from txt_utils import generate_pretty_txt
import uuid
import shutil

app = FastAPI(
    max_upload_size=50 * 1024 * 1024  # 50 MB
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend domain instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        # Check file size
        file_size = len(await file.read())
        if file_size > 50 * 1024 * 1024:  # 50 MB
            raise HTTPException(status_code=400, detail="File size exceeds the 50MB limit.")

        # Create temporary audio file
        temp_audio_path = f"temp_{uuid.uuid4().hex}.mp3"
        with open(temp_audio_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logging.info(f"✅ Step 1: Transcribing audio from {temp_audio_path}...")
        transcription = transcribe_audio(temp_audio_path)
        
        # Log transcription result
        logging.info(f"Transcription result: {transcription}")
        
        # Check if transcription failed or returned invalid data
        if not transcription:
            raise HTTPException(status_code=400, detail="Transcription returned empty or invalid data.")
        
        logging.info("✅ Step 2: Generating report from transcription...")
        json_report = generate_report(transcription, "few_shot_data.jsonl")

        # Log generated report data
        logging.info(f"Generated report data: {json_report}")

        # Check if report generation failed
        if not json_report:
            raise HTTPException(status_code=400, detail="Report generation failed.")

        # Create output text file
        output_txt = f"report_{uuid.uuid4().hex}.txt"
        logging.info("✅ Step 3: Creating text file...")
        generate_pretty_txt(json_report, output_path=output_txt)

        # Clean up temporary audio file
        os.remove(temp_audio_path)

        logging.info("✅ Step 4: Returning FileResponse")
        return FileResponse(
            output_txt,
            media_type="text/plain",
            filename="relatorio_clinico.txt"
        )
    
    except HTTPException as http_error:
        logging.error(f"HTTP Error occurred: {http_error.detail}")
        raise http_error
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

