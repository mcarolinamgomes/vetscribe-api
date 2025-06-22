from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from whisper_utils import transcribe_audio
from llama3_utils import generate_report
from txt_utils import generate_pretty_txt
import uuid
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend domain instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    temp_audio_path = f"temp_{uuid.uuid4().hex}.mp3"
    with open(temp_audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("✅ Step 1: Transcribing audio...")
    transcription = transcribe_audio(temp_audio_path)

    print("✅ Step 2: Generating report from transcription...")
    json_report = generate_report(transcription, "few_shot_data.jsonl")

    output_txt = f"report_{uuid.uuid4().hex}.txt"
    print("✅ Step 3: Creating text file...")
    generate_pretty_txt(json_report, output_path=output_txt)

    os.remove(temp_audio_path)

    print("✅ Step 4: Returning FileResponse")
    return FileResponse(
        output_txt,
        media_type="text/plain",
        filename="relatorio_clinico.txt"
    )
