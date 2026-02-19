from fastapi import APIRouter,Depends
from core.dependencies import get_current_user

router =  APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
async def user(current_user = Depends(get_current_user)):
    return{
        "email":current_user["email"],
        "name":current_user.get("name"),
        "provider":current_user["provider"],
        "id":str(current_user["_id"])
    }
