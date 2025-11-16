from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS - Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.get("/")
def home():
    """Health check endpoint"""
    return {"message": "Grok Chatbot API is live!"}

@app.post("/chat")
async def chat(data: dict):
    """Chat endpoint - receives message and returns reply"""
    user_msg = data.get("message", "").strip()
    
    # Validate input
    if not user_msg:
        return {"reply": "Please send a message!"}

    try:
        # Call Groq API
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": user_msg}
            ],
            max_tokens=1024,
            temperature=0.7
        )
        
        # Extract reply
        reply = response.choices[0].message.content
        return {"reply": reply}
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"reply": f"Sorry, I encountered an error: {str(e)}"}

# For local testing with: python api/index.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)