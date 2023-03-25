from fastapi import HTTPException, status

class SuccessefulResponse:
    def __init__(self, detail):
        self.json = {
            'status_code': status.HTTP_200_OK,
            'detail': detail,
        }


class AuthException(Exception):
    def __init__(self, detail="Registration or Authorization Error"):
        self.exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )

class ValidationException(Exception):
    def __init__(self, detail):
        self.exception = HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )