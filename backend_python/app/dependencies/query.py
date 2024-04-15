from fastapi import HTTPException, Request


def get_query_array_int(request: Request, key: str) -> list[int]:
    values = request.query_params.getlist(f"{key}[]")
    if not values:
        return []
    try:
        return [int(value) for value in values]
    except ValueError:
        raise HTTPException(status_code=400, detail=f"All values for {key}[] must be integers.")
