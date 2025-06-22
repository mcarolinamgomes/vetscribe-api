from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from whisper_utils import transcribe_audio
from llama3_utils import generate_report
from txt_utils import generate_pretty_txt  # changed from docx_utils
import uuid
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or use specific domains like ["https://preview--scribe-vet-report.lovable.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    # Step 1: Save audio file
    temp_audio_path = f"temp_{uuid.uuid4().hex}.mp3"
    with open(temp_audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"🔊 Transcribing: {temp_audio_path}")
    transcription = transcribe_audio(temp_audio_path)
    print("🔍 Generating report for input transcription...")

    # Step 2: Generate report as JSON string
    json_report = generate_report(transcription, "few_shot_data.jsonl")

    # Step 3: Generate TXT file
    output_txt = f"report_{uuid.uuid4().hex}.txt"
    generate_pretty_txt(json_report, output_path=output_txt)

    # Step 4: Clean up audio file
    os.remove(temp_audio_path)

    # Step 5: Return TXT as proper file response
    return FileResponse(
        output_txt,
        media_type="text/plain",
        filename="relatorio_clinico.txt"
    )

@app.get("/download/{filename}")
def download_txt(filename: str):
    return FileResponse(path=filename, filename=filename)
