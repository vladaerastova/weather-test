from fastapi import HTTPException, Header


async def verify_token(x_token: str = Header(...)):
    if not x_token:
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token
