from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# ✅ Correct imports (VERY IMPORTANT)
from utils.extractor import extract_text
from backend.utils.summarizer import generate_summary
from backend.utils.notes_generator import generate_notes
from backend.utils.flashcard_generator import generate_flashcards
from backend.utils.question_bank import generate_questions

# ✅ Correct app initialization
app = FastAPI()

# ✅ CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Test route
@app.get("/")
def home():
    return {"message": "Backend is running!"}

# ✅ File processing route
@app.post("/process-file/")
async def process_file(file: UploadFile = File(...)):
    print("Filename:", file.filename)

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Empty file")

    text = extract_text(file_bytes)

    return {
        "summary": generate_summary(text),
        "notes": generate_notes(text),
        "flashcards": generate_flashcards(text),
        "questions": generate_questions(text),
    }
