from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()



app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Pydantic model for request body
class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    """Health check endpoint"""
    return {"message": "Grok Chatbot API is live!"}

@app.post("/chat")
async def chat(request: ChatRequest):
    """Chat endpoint - receives message and returns reply"""
    try:
        user_msg = request.message.strip()
        
        # Validate input
        if not user_msg:
            return {"reply": "Please send a message!"}

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
        print(f"Error occurred: {str(e)}")
        return {
            "reply": f"Sorry, I encountered an error. Please try again later.",
            "error": str(e)
        }

# For local testing
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
