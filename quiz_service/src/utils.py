from fastapi import Depends, HTTPException

from src.clients.users import UserClient


def role_required(*roles):
    def dependency(current_user=Depends(UserClient().get_user_by_token)):
        print(roles)
        print(current_user)
        if current_user["role"] not in roles:
            raise HTTPException(403, "Not enough permissions")
        return current_user
    return dependency


# def role_required(current_user: dict = Depends(UserClient().get_user_by_token)):
#     if current_user["role"] != "admin":
#         raise HTTPException(status_code=403, detail="Admin privileges required")
#     return current_user
