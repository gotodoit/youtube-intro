from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# 加载环境变量（从根目录或当前目录）
load_dotenv(dotenv_path="../.env")
load_dotenv() # Fallback to local .env

app = FastAPI()

# 配置 CORS，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有来源，生产环境需指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}

# --- Business Logic ---
from pydantic import BaseModel
from backend.services.youtube import YouTubeService
from backend.services.deepseek import DeepSeekService

class ProcessRequest(BaseModel):
    url: str
    language: str = "zh-CN"

# Create API Router
api_router = APIRouter(prefix="/api")

@api_router.get("/health")
def health_check():
    return {"status": "ok", "version": "0.1.0"}

@api_router.post("/process")
async def process_video(request: ProcessRequest):
    """
    Process YouTube video: fetch info, get transcript, generate summary.
    Note: For MVP, this is a synchronous blocking call. In production, use background tasks.
    """
    print(f"Received process request for URL: {request.url}")
    try:
        # 1. Fetch Video Info
        print("Step 1: Fetching video info...")
        yt_service = YouTubeService()
        video_info = yt_service.get_video_info(request.url)
        print(f"Video info fetched: {video_info.get('title')}")
        
        # 2. Get Transcript
        print("Step 2: Fetching transcript...")
        transcript = yt_service.get_transcript(request.url)
        if not transcript or len(transcript) < 50:
             print("Transcript too short or empty.")
             return {"status": "error", "message": "Could not retrieve valid transcript for this video."}
        print(f"Transcript fetched, length: {len(transcript)}")

        # 3. Generate Summary
        print("Step 3: Generating summary with LLM...")
        llm_service = DeepSeekService()
        summary_result = llm_service.summarize_video(transcript, request.language)
        print("Summary generated successfully.")
        
        # 4. Return Combined Result
        return {
            "status": "success",
            "video_info": {
                "title": video_info.get("title"),
                "channel": video_info.get("channel"),
                "duration": video_info.get("duration"),
                "thumbnail": video_info.get("thumbnail")
            },
            "summary": summary_result
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error processing video: {str(e)}")
        return {"status": "error", "message": f"Processing failed: {str(e)}"}

# Include the router
app.include_router(api_router)
