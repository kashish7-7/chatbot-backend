from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify your domain)
    allow_credentials=True,
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
    
    if not user_msg:
        return {"reply": "Please send a message!"}

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": user_msg}
            ]
        )
        reply = response.choices[0].message.content
        return {"reply": reply}
    except Exception as e:
        return {"reply": f"Error: {str(e)}"}

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)