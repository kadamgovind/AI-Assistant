import os
import uuid
import whisper
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

# ✅ Load Whisper model once (fast performance)
model = whisper.load_model("base")

# -----------------------------
# 🎤 Speech to Text API
# -----------------------------
@router.post("/speech-to-text")
async def speech_to_text(file: UploadFile = File(...)):
    try:
        # ✅ Validate file type
        if not file.filename.endswith((".wav", ".mp3", ".m4a", ".webm")):
            raise HTTPException(status_code=400, detail="Invalid audio format ❌")

        # ✅ Unique filename (important for multiple users)
        file_id = str(uuid.uuid4())
        file_path = f"temp_{file_id}.wav"

        # ✅ Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # ✅ Check file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="File not saved properly ❌")

        # ✅ Transcribe
        result = model.transcribe(file_path)

        text = result.get("text", "").strip()

        # ✅ Delete temp file (cleanup)
        os.remove(file_path)

        return {
            "success": True,
            "text": text
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }