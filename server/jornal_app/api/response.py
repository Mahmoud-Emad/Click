"""Custom response handling file"""

from typing import Optional, OrderedDict
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND


class CustomResponse:
    """Custom response methods"""

    @staticmethod
    def success(data: list = [], message: Optional[str] = None, status_code: Optional[int] = None) -> Response:
        """Http success response method"""

        if not message:
            message = 'Success Response'
        if not status_code: 
            status_code = HTTP_200_OK

        return Response({
            'Message' : message,
            'Data':data,
            'Error' : False,
            'Http Status':status_code
        }, status = status_code)

    @staticmethod
    def not_found(message: Optional[str] = None, status_code: Optional[int] = None) -> Response:
        """Http not found response method"""

        if not message: 
            message = 'Response Not Found'
        if not status_code: 
            status_code = HTTP_404_NOT_FOUND

        return Response({
            'Message' : message,
            'Error' : True,
            'Http Status':status_code
        }, status = status_code)

    @staticmethod
    def bad_request(error: list = [], message: Optional[str] = None, data: list = [], status_code: Optional[int] = None) -> Response:
        """Http bad request method"""
        if not message:
            message = 'Server Bad Request'
        if not status_code: 
            status_code = HTTP_400_BAD_REQUEST

        return Response({
            'Message' : message,
            'Data' : data,
            'Error' : True,
            'Error Details' : error,
            'Http Status':status_code
        }, status = status_code)