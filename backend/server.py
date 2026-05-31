"""
FastAPI server for MathTutor coaching service.
Provides both static (original) and AI-powered coaching.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Literal
import os
from pathlib import Path
from dotenv import load_dotenv

from coaching_service import CoachingService, CoachingContext, CoachingResponse

# Load environment variables
load_dotenv()

app = FastAPI(
    title="MathTutor Coaching API",
    description="Provides coaching feedback for math problems using various teaching strategies",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative React port
        "https://deepak-mukunthu.github.io",  # Your GitHub Pages
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize coaching service
api_key = os.getenv("ANTHROPIC_API_KEY")
coaching_service = CoachingService(api_key)


class CoachRequest(BaseModel):
    """Request for coaching feedback."""
    mode: Literal["static", "ai"] = "static"
    harness: str = "socratic"
    context: CoachingContext


class HarnessInfo(BaseModel):
    """Information about available harnesses."""
    name: str
    description: str
    strategy: str


@app.get("/")
async def serve_frontend():
    """Serve the web UI."""
    frontend_path = Path(__file__).parent.parent / "frontend" / "index.html"
    if frontend_path.exists():
        return FileResponse(frontend_path)
    else:
        # Fallback to API info
        return {
            "status": "healthy",
            "service": "MathTutor Coaching API",
            "version": "1.0.0",
            "ai_enabled": bool(api_key),
            "note": "Web UI not found. API docs at /docs"
        }


@app.get("/api/harnesses", response_model=list[HarnessInfo])
async def get_harnesses():
    """Get list of available coaching harnesses."""
    return [
        HarnessInfo(
            name="socratic",
            description="Guides through questioning",
            strategy="Socratic Method"
        ),
        HarnessInfo(
            name="direct",
            description="Clear explanations with examples",
            strategy="Direct Instruction"
        ),
        HarnessInfo(
            name="step-by-step",
            description="Breaks problems into manageable steps",
            strategy="Step-by-Step Guidance"
        ),
        HarnessInfo(
            name="discovery",
            description="Encourages pattern exploration",
            strategy="Discovery Learning"
        ),
        HarnessInfo(
            name="adaptive",
            description="Adjusts to student level",
            strategy="Adaptive Learning"
        ),
    ]


@app.post("/api/coach", response_model=CoachingResponse)
async def get_coaching(request: CoachRequest):
    """
    Get coaching feedback for a student's answer.

    Args:
        request: Contains mode (static/ai), harness type, and context

    Returns:
        CoachingResponse with message, hints, and guidance
    """
    try:
        if request.mode == "ai" and not api_key:
            raise HTTPException(
                status_code=503,
                detail="AI mode requires ANTHROPIC_API_KEY to be configured"
            )

        response = coaching_service.coach(
            mode=request.mode,
            context=request.context,
            harness=request.harness
        )

        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/api/reset/{harness}")
async def reset_harness(harness: str):
    """Reset conversation history for a specific harness."""
    try:
        coaching_service.reset_harness(harness)
        return {"status": "success", "message": f"Reset {harness} harness"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "ai_available": bool(api_key),
        "harnesses_loaded": len(coaching_service.harnesses),
        "modes": ["static", "ai"]
    }


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🎓 MathTutor Coaching API Server")
    print("="*60)
    print(f"AI Mode: {'✅ Enabled' if api_key else '❌ Disabled (add ANTHROPIC_API_KEY)'}")
    print(f"")
    print(f"🌐 Web UI:    http://localhost:8000")
    print(f"📚 API Docs:  http://localhost:8000/docs")
    print(f"🔧 Health:    http://localhost:8000/api/health")
    print("="*60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
