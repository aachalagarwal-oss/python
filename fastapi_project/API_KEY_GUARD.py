from fastapi import APIRouter
from fastapi import Header,HTTPException,status,Depends
router=APIRouter()


def verify_token(api_key: str = Header(...)):
    if api_key!="secret-123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    

@router.get("/secret_dashboard",dependencies=[Depends(verify_token)])
def secret_dashboard():
    return{"Message":"Welcome to the dashboard"}

