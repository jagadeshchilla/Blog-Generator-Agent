import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM

import os
from dotenv import load_dotenv

# Load .env file if it exists (for local development)
# In Vercel, environment variables are set automatically
try:
    load_dotenv()
except Exception:
    pass

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok", "message": "Blog Generator API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "routes": ["/blogs/topic", "/blogs/youtube"]}

# Configure CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "")
cors_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "https://blog-generator-agent-five.vercel.app",
]
if FRONTEND_URL:
    cors_origins.append(FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

class TopicBlogRequest(BaseModel):
    topic: str
    language: Optional[str] = None

class YouTubeBlogRequest(BaseModel):
    youtube_url: str
    language: Optional[str] = None

os.environ["LANGSMITH_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

## API's

@app.post("/blogs/topic")
async def create_blogs_from_topic(request: TopicBlogRequest):
    """
    Create a blog post from a topic.
    """
    topic = request.topic
    language = request.language or 'english'

    try:
        ## get the llm object
        groqllm=GroqLLM()
        llm=groqllm.get_llm()

        ## get the graph
        graph_builder=GraphBuilder(llm)
        graph=graph_builder.setup_graph(usecase="topic")
        state=graph.invoke({
            "topic": topic,
            "current_language": language.lower()
        })

        # Include video_id in response if available
        result = {"data": state}
        if "video_id" in state:
            result["video_id"] = state["video_id"]
        return result
    except ValueError as e:
        print(f"ValueError in /blogs/topic: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in /blogs/topic: {str(e)}")
        print(f"Traceback: {error_trace}")
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/blogs/youtube")
async def create_blogs_from_youtube(request: YouTubeBlogRequest):
    """
    Create a blog post from YouTube video transcript.
    """
    youtube_url = request.youtube_url
    language = request.language or 'english'

    try:
        ## get the llm object
        groqllm=GroqLLM()
        llm=groqllm.get_llm()

        ## get the graph
        graph_builder=GraphBuilder(llm)
        graph=graph_builder.setup_graph(usecase="youtube")
        state=graph.invoke({
            "youtube_url": youtube_url,
            "current_language": language.lower()
        })

        # Include video_id in response if available
        result = {"data": state}
        if "video_id" in state:
            result["video_id"] = state["video_id"]
        return result
    except ValueError as e:
        print(f"ValueError in /blogs/youtube: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in /blogs/youtube: {str(e)}")
        print(f"Traceback: {error_trace}")
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

if __name__=="__main__":
    uvicorn.run("app:app",host="0.0.0.0",port=8000,reload=True)

