from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import os
from dotenv import load_dotenv
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.get("/")
def home():
    return {"message": "Grok Chatbot API is live!"}

@app.post("/chat")
async def chat(data: dict):
    user_msg = data.get("message", "")

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": user_msg}
        ]
    )

    reply = response.choices[0].message.content
    return {"reply": reply}
