from fastapi import HTTPException, status

def require_scope(user: dict, required_scope: str):
    scopes = user.get("scopes", [])

    if required_scope not in scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing required scope: {required_scope}",
        )
