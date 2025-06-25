import whisper
import os

def transcribe_audio(file_path: str) -> str:
    try:
        # Check if the file exists before proceeding
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file at {file_path} does not exist.")
        
        # Load the model (ensure it's the right model for the task)
        print(f"🔊 Loading Whisper model...")
        model = whisper.load_model("base")  # or "medium", "large" as needed
        print(f"🔊 Transcribing: {file_path}")
        
        # Attempt transcription and handle possible memory issues
        result = model.transcribe(file_path, language='pt')
        
        return result["text"]
    
    except FileNotFoundError as fnf_error:
        print(f"❌ Error: {fnf_error}")
        return f"Error: {fnf_error}"
    
    except MemoryError:
        print("❌ Error: Memory allocation failed. Try reducing the model size or free up memory.")
        return "Error: Memory allocation failed."
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return f"Error: An unexpected error occurred: {e}"

# Example usage
if __name__ == "__main__":
    file_path = "luvvoice.com-20250430-s8YXYW.mp3"
    transcript = transcribe_audio(file_path)
    
    if "Error" not in transcript:
        print("\n📝 Transcription Result:\n")
        print(transcript)
    else:
        print("\n❌ Transcription failed.")
