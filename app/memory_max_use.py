from fastapi import APIRouter

router = APIRouter()

data = []

@router.get("/eat-memory")
def eat_memory():
    """
        demo func for eating memory TEST

    """
    while True:
        data.append("X" * 10_000_000)  # ~10MB per iteration

