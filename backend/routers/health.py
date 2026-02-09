from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["health"],
)

@router.get("/data")
def health():
    return {"status": "ok"}