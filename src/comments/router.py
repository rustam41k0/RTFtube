from fastapi import APIRouter

router = APIRouter(
    tags=["Comments"]
)


@router.get("/comments")
def first_rout():
    return {"status": "success"}
