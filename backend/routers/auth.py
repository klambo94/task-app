from fastapi import APIRouter

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register")
def register():
    return None

@router.post("/login")
def login():
    return None

@router.post("/logout")
def logout():
    return None