from fastapi import HTTPException, status

class SuccessefulResponse:
    def __init__(self, detail="Task successefuly completed"):
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

class ForbiddenException(Exception):
    def __init__(self, detail="You are not allowed to use this"):
        self.exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class NotFoundException(Exception):
    def __init__(self, detail="The object you are trying to access not found"):
        self.exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class ConflictException(Exception):
    def __init__(self, detail="The data you provided conflicts with already existing"):
        self.exception = HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )

class GoneException(Exception):
    def __init__(self, detail="The object you are trying to access was deleted"):
        self.exception = HTTPException(
            status_code=status.HTTP_410_GONE,
            detail=detail
        )

class ValidationException(Exception):
    def __init__(self, detail="The data you provided is not correct"):
        self.exception = HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )