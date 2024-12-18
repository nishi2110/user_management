from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    Confirms the application is running.
    """
    return {"status": "healthy"}
