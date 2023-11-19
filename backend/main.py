# uvicorn main:app --reload
# http://127.0.0.1:8000/docs
# https://api.elevenlabs.io/docs#/

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

# custom function imports
from functions.database import store_messages, reset_messages
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.text_to_speech import convert_text_to_speech

# Init app
app = FastAPI()

# CORS - Origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
]

# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health")
async def check_health():
    return {"message": "Healthy"}


@app.get("/text_to_speech")
async def speech(message):
    audio_output = convert_text_to_speech(message)

    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get Eleven Labs audio response.")

    def iterfile():
        yield audio_output

    return StreamingResponse(iterfile(), media_type="audio/mpeg")


@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "Conversation reset"}


@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):

    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")  # open("voice.mp3", "rb")

    message_decoded = convert_audio_to_text(audio_input)

    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode audio.")

    chat_response = get_chat_response(message_decoded)

    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to get chatGPT response.")

    store_messages(message_decoded, chat_response)

    audio_output = convert_text_to_speech(chat_response)

    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get Eleven Labs audio response.")

    def iterfile():
        yield audio_output

    return StreamingResponse(iterfile(), media_type="application/octet-stream")
