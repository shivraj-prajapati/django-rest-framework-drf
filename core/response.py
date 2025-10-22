from rest_framework import status
from rest_framework.response import Response

def success_response(data=None, message="Success Request", code=status.HTTP_200_OK):
    return Response({
        'success': True,
        'message': message,
        'data': data or {}
    }, status=code)
    
def error_response(message='Somethig went wrong', errors=None, code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "success": False,
        "message": message,
        "errors": errors or []
    }, status=code)