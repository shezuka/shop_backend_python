from fastapi import Request, HTTPException


async def get_access_token(request: Request):
    header = request.headers.get("Authorization", None)
    if not header:
        return None

    access_token = header.split(" ")[-1]
    return access_token


async def require_access_token(request: Request):
    access_token = await get_access_token(request)
    if access_token is None:
        raise HTTPException(
            status_code=401,
            detail="Access token is missing or invalid",
        )

    return access_token
