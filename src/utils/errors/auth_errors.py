from fastapi import status, HTTPException

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


only_root_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Only root allowed to do this action!",
    headers={"WWW-Authenticate": "Bearer"},
)